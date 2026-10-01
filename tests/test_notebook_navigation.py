"""Exercise registry connection, recovery, and notebook command dispatch."""
from pathlib import Path
import shutil
import subprocess
import unittest


class NavigationTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "Node.js is needed for the frontend regression")
    def test_registry_connection_and_recovery_without_child_models(self):
        source = Path(__file__).resolve().parents[1]/'calmar/notebook_navigation.js'
        script = r'''
import assert from 'node:assert/strict';
import fs from 'node:fs';
const source = fs.readFileSync(process.argv[2], 'utf8');
const module = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
const calls = [], sent = [], handlers = {};
const el = {style: {}, textContent: ''};
const cells = ['other', 'guided-start'].map((role, i) => ({id: String(i), getMetadata: () => ({role})}));
let changed;
cells.changed = {connect: callback => changed = callback, disconnect: callback => {
  assert.equal(changed, callback); changed = null;
}};
const panel = {id:'own-notebook', node:{contains: node => node === el},
    content:{model:{cells}, deselectAll(){}, activeCellIndex:0}};
const app = {shell:{widgets: () => [panel], activateById: id => calls.push(id)},
             commands:{execute: async command => calls.push(command)}};
let available = true;
const manager = {loadClass: async (...args) => {
  assert.deepEqual(args, ['JupyterFrontEndModel', 'ipylab', '^1.0.0']);
  if (!available) throw Error('Extension is still loading');
  return {app};
}, get_model: () => {throw Error('Must not use stored child models');}};
assert.equal(await module.getLabApplication(manager), app);
await assert.rejects(module.getLabApplication({loadClass:async () => ({})}), /extension did not provide/);
const model = {get: () => {throw Error('Must not read a lab trait');}, widget_manager:manager,
               on:(name, callback) => handlers[name]=callback, off(){}, send:data => sent.push(data)};
const dispose = await module.default.render({model,el});
assert.equal(sent[0].event, 'ready');
assert.deepEqual(sent[1], {event:'cell-order', ids:['0','1'], batch_start:null});
cells.push({id:'batch', getMetadata: () => ({role:'batch-start'})});
changed();
assert.deepEqual(sent.at(-1), {event:'cell-order', ids:['0','1','batch'], batch_start:'batch'});
await handlers['msg:custom']({action:'connected'});
await handlers['msg:custom']({action:'prepare',role:'guided-start',all_below:false});
assert.equal(sent.at(-1).event,'approved');
await handlers['msg:custom']({action:'execute'});
assert.equal(panel.content.activeCellIndex,1);
assert.deepEqual(calls,['own-notebook','notebook:run-cell']);
dispose();
assert.equal(changed, null);
sent.length = 0;
available = false;
const disposeRetry = await module.default.render({model,el});
assert.deepEqual(sent.map(item => item.event), ['error']);
assert.equal(sent[0].connection, true);
assert.match(el.textContent, /Extension is still loading/);
// The handler survives initialization failure and can reconnect without reload.
available = true;
await handlers['msg:custom']({action:'connect'});
assert.equal(sent.at(-2).event, 'ready');
assert.equal(sent.at(-1).event, 'cell-order');
await handlers['msg:custom']({action:'connected'});
await handlers['msg:custom']({action:'prepare',role:'guided-start',all_below:true});
assert.equal(sent.at(-1).event, 'approved');
await handlers['msg:custom']({action:'execute'});
assert.equal(calls.at(-1), 'notebook:run-all-below');
disposeRetry();
'''
        result = subprocess.run(['node','--input-type=module','-',str(source)], input=script,
                                text=True,capture_output=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stderr)
