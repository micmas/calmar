// Ask the active widget registry to initialize ipylab's frontend exports.
// Its registered factory binds the application before returning the class.
// Do not resolve a child widget: saved/failed models need not carry that app.
export async function getLabApplication(manager) {
  const FrontEnd = await manager.loadClass('JupyterFrontEndModel', 'ipylab', '^1.0.0');
  const app = FrontEnd?.app;
  if (app?.shell && typeof app.shell.widgets === 'function' &&
      typeof app.shell.activateById === 'function' &&
      typeof app.commands?.execute === 'function') return app;
  throw Error('The ipylab extension did not provide notebook navigation.');
}

export default {
  async render({ model, el }) {
    el.style.fontSize = '12px';
    el.textContent = 'Connecting notebook controls…';
    let app, connecting, disposed = false;
    let pending = null;
    let observedCells = null;
    const publishCellOrder = () => {
      const cells = observedCells ? Array.from(observedCells) : [];
      const starts = cells.filter(c => c.getMetadata('calmar')?.role === 'batch-start');
      model.send({event: 'cell-order', ids: cells.map(c => c.id),
        batch_start: starts.length === 1 ? starts[0].id : null});
    };
    const observeCellOrder = () => {
      const panel = owner();
      const cells = panel?.content?.model?.cells;
      if (!cells) return;
      if (observedCells !== cells) {
        observedCells?.changed?.disconnect(publishCellOrder);
        observedCells = cells;
        observedCells.changed?.connect(publishCellOrder);
      }
      publishCellOrder();
    };
    const connect = async () => {
      if (connecting) return connecting;
      connecting = (async () => {
        try {
          app = await getLabApplication(model.widget_manager);
          if (!disposed) {
            model.send({event: 'ready'});
            observeCellOrder();
          }
        } catch (error) {
          app = null;
          el.textContent = `Notebook controls could not connect: ${error.message || error} Click the workflow button to retry.`;
          if (!disposed) model.send({event: 'error', connection: true, message: el.textContent});
        }
      })();
      try { await connecting; } finally { connecting = null; }
    };
    const owner = () => Array.from(app.shell.widgets('main')).find(p => p.node.contains(el));
    const fail = error => model.send({event: 'error', message: String(error.message || error)});
    const receive = async data => {
      try {
        if (data.action === 'connected') {
          el.textContent = '';
          clearTimeout(connectionTimer);
        } else if (data.action === 'connect') {
          await connect();
        } else if (data.action === 'prepare') {
          if (!app) await connect();
          if (!app) return;
          const panel = owner();
          if (!panel?.content?.model?.cells) throw Error('Open this control in its notebook tab.');
          const cells = Array.from(panel.content.model.cells);
          const matches = cells.filter(c => c.getMetadata('calmar')?.role === data.role);
          if (matches.length !== 1) throw Error(`Cannot locate a unique ${data.role} cell. Reload the updated notebook.`);
          if (data.prompt && !window.confirm(data.prompt)) {
            model.send({event: 'cancelled', message: 'Continuation cancelled; no cells were started.'});
            return;
          }
          pending = {panel, cellId: matches[0].id, allBelow: data.all_below};
          model.send({event: 'approved'});
        } else if (data.action === 'execute' && pending) {
          const {panel, cellId, allBelow} = pending;
          pending = null;
          if (panel.isDisposed) throw Error('The notebook was closed.');
          const index = Array.from(panel.content.model.cells).findIndex(c => c.id === cellId);
          if (index < 0) throw Error('The continuation cell was removed.');
          app.shell.activateById(panel.id);
          panel.content.deselectAll();
          panel.content.activeCellIndex = index;
          panel.content.mode = 'command';
          await app.commands.execute(allBelow ? 'notebook:run-all-below' : 'notebook:run-cell');
        }
      } catch (error) { fail(error); }
    };
    model.on('msg:custom', receive);
    const connectionTimer = setTimeout(() => {
      if (app) el.textContent = 'Waiting for the notebook kernel to connect. Click the workflow button to retry.';
    }, 8000);
    await connect();
    return () => {
      disposed = true;
      observedCells?.changed?.disconnect(publishCellOrder);
      clearTimeout(connectionTimer);
      model.off('msg:custom', receive);
    };
  }
};
