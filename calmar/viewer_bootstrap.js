// Finish anywidget model initialization before loading the imaging bundle.
// anywidget 0.11 rejects model initialization after two seconds; rendering may
// take longer on a cold cache or when restoring several volume viewers.
const viewerSource = __CALMAR_VIEWER_SOURCE__;
// Reuse compressed bytes across viewers in this browser, bounded to 128 MiB.
const fileCache = globalThis.__calmarImageCache ??= new Map();
const cacheLimit = 128 * 1024 * 1024;

export default () => {
  let initializeContext, definition, loading, cleanupModel, disposed = false;
  let model, wrappedModel, viewElement, volumeRevision = 0, kernel;
  let volumeQueue = Promise.resolve();
  const pending = new Map(), hydrated = new WeakMap(), callbacks = new Map();
  const customHandlers = new Set();
  const visibilityWaiters = new Set();
  const guardedRanges = new WeakSet(), rangeCleanups = new Set();
  const preserveAutoRange = volume => {
    if (guardedRanges.has(volume)) return;
    guardedRanges.add(volume);
    // A delayed full widget-state reply can contain the original null range
    // after NiiVue has already calculated contrast. Passing that null through
    // its change handler makes the loaded image's range NaN (a black brain).
    for (const field of ['cal_min', 'cal_max']) {
      let last = volume.get(field);
      const changed = () => {
        const value = volume.get(field);
        if (typeof value === 'number' && Number.isFinite(value)) last = value;
        else if (typeof last === 'number' && Number.isFinite(last)) {
          volume.set(field, last, {silent: true});
          volume.save_changes();
        }
      };
      volume.on(`change:${field}`, changed);
      rangeCleanups.add(() => volume.off(`change:${field}`, changed));
    }
  };
  const whenVisible = el => {
    if (typeof IntersectionObserver === 'undefined') return Promise.resolve();
    return new Promise(resolve => {
      const finish = () => { observer.disconnect(); visibilityWaiters.delete(finish); resolve(); };
      const observer = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting)) finish();
      }, {rootMargin: '150px'});
      visibilityWaiters.add(finish);
      observer.observe(el);
    });
  };
  // These origin colours are absent from the bundled NiiVue built-ins.
  // Register before loading volumes, including after browser restoration.
  const originColors = {cyan: [0, 255, 255], magenta: [255, 0, 255], yellow: [255, 255, 0]};
  const requestId = () => globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`;
  const waiting = () => {
    if (viewElement && !viewElement.querySelector('canvas'))
      viewElement.textContent = 'Waiting for image data; the computation or notebook connection may still be busy…';
  };
  const reconnected = (_sender, status) => {
    if (status === 'connected') {
      for (const task of Array.from(pending.values())) { task.retries = 0; task.retry(); }
    }
  };
  const fail = error => {
    if (viewElement) viewElement.textContent = `Could not load the brain-image viewer: ${error.message || error}`;
    console.error('CALMaR viewer:', error);
  };
  const receive = (message, buffers) => {
    const task = pending.get(message.request);
    if (!task) return;
    if (message.type === 'calmar:volume-chunk') {
      const buffer = buffers?.[0];
      if (!buffer || message.offset !== task.size) {
        task.reject(new Error('Incomplete image transfer. Rerun this viewer cell to retry.'));
        return;
      }
      const bytes = new Uint8Array(buffer.buffer || buffer, buffer.byteOffset || 0, buffer.byteLength);
      task.parts.push(bytes);
      task.size += bytes.byteLength;
      task.touch();
    } else if (message.type === 'calmar:volume-complete') {
      if (task.size !== message.size || !task.size) {
        task.reject(new Error('Incomplete or empty image transfer.'));
      } else {
        const bytes = new Uint8Array(task.size);
        let offset = 0;
        for (const part of task.parts) { bytes.set(part, offset); offset += part.byteLength; }
        task.resolve(new DataView(bytes.buffer));
      }
    } else if (message.type === 'calmar:volume-error') task.reject(new Error(message.message));
  };
  const readHTTP = async descriptor => {
    if (!descriptor.url || typeof window === 'undefined') return null;
    const settings = kernel?.serverSettings;
    const base = new URL(settings?.baseUrl || '/', window.location.href);
    const url = new URL(descriptor.url, base);
    // Never forward Jupyter credentials to another origin or outside its base.
    if (url.origin !== base.origin || !url.pathname.startsWith(base.pathname)) return null;
    const key = url.href;
    if (fileCache.has(key)) {
      const item = fileCache.get(key);
      fileCache.delete(key); fileCache.set(key, item);
      return item;
    }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const headers = new Headers(settings?.init?.headers || {});
      if (settings?.token) headers.set('Authorization', `token ${settings.token}`);
      const response = await fetch(url.href, {headers, credentials: 'same-origin', signal: controller.signal});
      if (!response.ok || /text\/html/i.test(response.headers.get('content-type') || '')) return null;
      const bytes = await response.arrayBuffer();
      if (!bytes.byteLength) return null;
      const data = new DataView(bytes);
      if (bytes.byteLength <= cacheLimit) {
        fileCache.set(key, data);
        let size = Array.from(fileCache.values()).reduce((n, v) => n + v.byteLength, 0);
        for (const [old, value] of fileCache) {
          if (size <= cacheLimit) break;
          fileCache.delete(old); size -= value.byteLength;
        }
      }
      return data;
    } catch { return null; }
    finally { clearTimeout(timer); }
  };
  const readFile = (volume, field, descriptor) => {
    if (!descriptor?.calmar_lazy || descriptor.data) return Promise.resolve();
    if (hydrated.has(descriptor)) return hydrated.get(descriptor);
    const promise = readHTTP(descriptor).then(data => data || new Promise((resolve, reject) => {
      let timer;
      const finish = fn => value => { clearTimeout(timer); pending.delete(task.request); fn(value); };
      const task = {parts: [], size: 0, retries: 0, request: null,
        resolve: finish(resolve), reject: finish(reject),
        retry() {
          pending.delete(task.request);
          task.request = requestId();
          task.parts = []; task.size = 0; task.retries += 1;
          pending.set(task.request, task);
          task.touch();
          model.send({type: 'calmar:read-volume', request: task.request, volume: volume.model_id, field});
        },
        touch() {
          clearTimeout(timer);
          timer = setTimeout(() => {
            // Comm requests queue behind running notebook code. A long
            // segmentation is not a failed transfer: retain the request so
            // its reply can hydrate this viewer as soon as the kernel is free.
            if (kernel?.status === 'busy' ||
                (kernel?.connectionStatus && kernel.connectionStatus !== 'connected')) {
              waiting();
              task.touch();
              return;
            }
            // A reconnect can lose the original custom message. Retry using
            // a new ID so delayed chunks from an older attempt are ignored.
            // Keep the latest request alive even if kernel status is stale.
            waiting();
            if (task.retries < 3) task.retry();
            else task.touch();
          }, 60000);
        }};
      task.retry();
    })).then(data => {
      // Populate the frontend's file descriptor only. Do not sync image bytes
      // back into the kernel's widget state or change the source path.
      descriptor.data = data;
    }).catch(error => { hydrated.delete(descriptor); throw error; });
    hydrated.set(descriptor, promise);
    return promise;
  };
  const hydrate = async () => {
    while (!disposed) {
      const refs = model.get('volumes');
      try {
        const volumes = await Promise.all(refs.map(ref =>
          typeof ref === 'string' ? model.widget_manager.get_model(ref.slice(10)) : ref));
        volumes.forEach(preserveAutoRange);
        await Promise.all(volumes.flatMap(volume => ['path', 'paired_img_path'].map(field =>
          readFile(volume, field, volume.get(field)))));
      } catch (error) {
        if (refs === model.get('volumes')) throw error;
      }
      if (refs === model.get('volumes')) return;
    }
  };
  const readyVolume = volume => new Promise((resolve, reject) => {
    if (volume.get('hdr')) { resolve(); return; }
    const done = () => {
      if (!volume.get('hdr')) return;
      clearTimeout(timer); volume.off('change:hdr', done); resolve();
    };
    const timer = setTimeout(() => {
      volume.off('change:hdr', done);
      reject(new Error('The selected image did not finish loading. Rerun this viewer cell.'));
    }, 30000);
    volume.on('change:hdr', done);
  });
  const nextFrame = () => new Promise(resolve => requestAnimationFrame(resolve));
  const load = () => loading ??= (async () => {
    const url = URL.createObjectURL(new Blob([viewerSource], {type: 'text/javascript'}));
    try {
      const module = await import(url);
      if (disposed) return;
      definition = typeof module.default === 'function' ? await module.default() : module.default;
      cleanupModel = await definition.initialize?.({...initializeContext, model: wrappedModel});
      for (const [name, [r, g, b]] of Object.entries(originColors)) {
        const lut = {I: [0, 255], R: [0, r], G: [0, g], B: [0, b], A: [0, 255]};
        for (const handler of customHandlers)
          await handler({type: 'add_colormap', data: [name, lut]}, []);
      }
      if (disposed) { cleanupModel?.(); cleanupModel = null; }
    } finally { URL.revokeObjectURL(url); }
  })();
  return {
    initialize(context) {
      initializeContext = context;
      model = context.model;
      kernel = model.widget_manager.kernel;
      kernel?.connectionStatusChanged?.connect(reconnected);
      model.on('msg:custom', receive);
      wrappedModel = new Proxy(model, {get(target, key) {
        if (key === 'on') return (event, callback, ...args) => {
          if (event === 'msg:custom') customHandlers.add(callback);
          if (event === 'change:volumes') {
            const wrapped = (...values) => {
              const revision = ++volumeRevision;
              const canvas = viewElement?.querySelector('canvas');
              if (canvas) canvas.style.visibility = 'hidden';
              // NiiVue adds incoming volumes before removing the old ones.
              // Serialize changes and reveal only a complete selection, so QC
              // cannot briefly show native and MNI images on top of each other.
              volumeQueue = volumeQueue.catch(() => {}).then(async () => {
                if (disposed || revision !== volumeRevision) return;
                await hydrate();
                if (disposed || revision !== volumeRevision || !canvas) return;
                const refs = model.get('volumes');
                const volumes = await Promise.all(refs.map(ref =>
                  typeof ref === 'string' ? model.widget_manager.get_model(ref.slice(10)) : ref));
                const ready = Promise.all(volumes.map(readyVolume));
                callback(...values);
                await ready;
                // hdr is published by NiiVue just before the final GPU update.
                await nextFrame(); await nextFrame();
                if (!disposed && revision === volumeRevision) canvas.style.visibility = '';
              }).catch(error => { if (!disposed) fail(error); });
              return volumeQueue;
            };
            callbacks.set(callback, wrapped);
            return target.on(event, wrapped, ...args);
          }
          return target.on(event, callback, ...args);
        };
        if (key === 'off') return (event, callback, ...args) => {
          if (event === 'msg:custom') {
            if (callback) customHandlers.delete(callback); else customHandlers.clear();
          }
          return target.off(event, callbacks.get(callback) || callback, ...args);
        };
        const value = Reflect.get(target, key);
        return typeof value === 'function' ? value.bind(target) : value;
      }});
      return () => {
        disposed = true;
        for (const finish of Array.from(visibilityWaiters)) finish();
        for (const cleanup of rangeCleanups) cleanup();
        rangeCleanups.clear();
        kernel?.connectionStatusChanged?.disconnect(reconnected);
        model.off('msg:custom', receive);
        for (const task of pending.values()) task.reject(new Error('Viewer closed.'));
        cleanupModel?.();
        cleanupModel = null;
      };
    },
    async render(context) {
      viewElement = context.el;
      context.el.textContent = 'Loading brain-image viewer…';
      try {
        // Restoring every off-screen WebGL viewer at once can freeze the page.
        // A collapsed tab needs no image transfer or GPU work until it opens.
        await whenVisible(context.el);
        if (disposed) return;
        await load();
        await hydrate();
        if (disposed) return;
        context.el.replaceChildren();
        return await definition.render({...context, model: wrappedModel});
      } catch (error) {
        fail(error);
      }
    }
  };
};
