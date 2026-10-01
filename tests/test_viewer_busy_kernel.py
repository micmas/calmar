"""Images queued behind long processing must load once the kernel becomes free."""
from pathlib import Path
import shutil
import subprocess

import pytest


@pytest.mark.skipif(not shutil.which("node"), reason="Node.js required")
def test_queued_image_survives_timeout_and_loads_after_kernel_is_idle():
    source = Path(__file__).resolve().parents[1] / "calmar/viewer_bootstrap.js"
    script = r'''
import assert from 'node:assert/strict';
import fs from 'node:fs';
globalThis.registeredColors=[];
const noopViewer = `export default {
  initialize({model}) {model.on('msg:custom', message => globalThis.registeredColors.push(message));},
  render({el}) {el.textContent="IMAGE_RENDERED";}
}`;
const source = fs.readFileSync(process.argv[2], 'utf8')
  .replace('__CALMAR_VIEWER_SOURCE__', JSON.stringify(noopViewer));
const {default: factory} = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
URL.createObjectURL = () => 'data:text/javascript;base64,' + Buffer.from(noopViewer).toString('base64');
URL.revokeObjectURL = () => {};
const timers = new Map(); let nextTimer = 0;
globalThis.setTimeout = callback => {timers.set(++nextTimer, callback); return nextTimer;};
globalThis.clearTimeout = id => timers.delete(id);
const el = {textContent:'', querySelector: () => null, replaceChildren() {this.textContent='';}};
const file = {name:'image.nii.gz', data:null, calmar_lazy:true};
const volumeState = {path:file, cal_min:null, cal_max:null}, volumeEvents = new Map();
const volume = {
 model_id:'volume', get:key=>volumeState[key], save_changes(){},
 on:(event, callback)=>volumeEvents.set(event,callback),
 off:event=>volumeEvents.delete(event),
 set(key,value,options={}) {volumeState[key]=value;if(!options.silent) volumeEvents.get('change:'+key)?.();},
};
const volumes = [volume], sent = [], handlers = {};
let reconnect;
const kernel = {status:'busy', connectionStatus:'connected', connectionStatusChanged:{
  connect(callback) {reconnect=callback;},
  disconnect(callback) {assert.equal(reconnect,callback); reconnect=null;},
}};
const model = {
  widget_manager:{kernel}, get:key => volumes,
  on:(event, cb) => {const previous=handlers[event]; handlers[event]=(...args)=>{previous?.(...args);cb(...args);};},
  off(){}, send:msg => sent.push(msg),
};
const widget = factory();
const dispose = widget.initialize({model});
const render = widget.render({model,el});
await new Promise(resolve => setImmediate(resolve));
assert.equal(sent.length,1);
assert.deepEqual(globalThis.registeredColors.map(m=>m.data[0]),['cyan','magenta','yellow']);
assert.deepEqual(globalThis.registeredColors[0].data[1],{I:[0,255],R:[0,0],G:[0,255],B:[0,255],A:[0,255]});
// Simulate several minutes of computation, then a temporary disconnection.
for (let i=0;i<4;i++) {
  [...timers.values()][0]();
  assert.match(el.textContent,/Waiting for image data/);
}
kernel.status='idle'; kernel.connectionStatus='disconnected';
[...timers.values()][0]();
kernel.connectionStatus='connected';
// Reconnection retries immediately instead of waiting another full minute.
reconnect(kernel,'connected');
assert.equal(sent.length,2);
assert.notEqual(sent[0].request,sent[1].request);
// A late chunk from the old connection must not corrupt the fresh transfer.
handlers['msg:custom']({type:'calmar:volume-chunk',request:sent[0].request,offset:99}, [new Uint8Array([9])]);
const request=sent[1].request;
handlers['msg:custom']({type:'calmar:volume-chunk',request,offset:0}, [new Uint8Array([1,2,3])]);
handlers['msg:custom']({type:'calmar:volume-complete',request,size:3}, []);
await render;
assert.equal(el.textContent,'IMAGE_RENDERED');
assert.equal(file.data.byteLength,3);
assert.equal(timers.size,0);
// NiiVue computes contrast, then a delayed initial-state reply brings nulls.
// Keep the valid range; explicit finite user changes must still take effect.
volume.set('cal_min',0); volume.set('cal_max',392);
volume.set('cal_min',null); volume.set('cal_max',null);
assert.equal(volume.get('cal_min'),0); assert.equal(volume.get('cal_max'),392);
volume.set('cal_max',250);
assert.equal(volume.get('cal_max'),250);
dispose();
assert.equal(volumeEvents.size,0);
assert.equal(reconnect,null);
'''
    result = subprocess.run(["node", "--input-type=module", "-", str(source)],
                            input=script, text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr


@pytest.mark.skipif(not shutil.which("node"), reason="Node.js required")
def test_http_images_load_while_kernel_is_busy_and_are_reused():
    source = Path(__file__).resolve().parents[1] / 'calmar/viewer_bootstrap.js'
    script = r'''
import assert from 'node:assert/strict';
import fs from 'node:fs';
const native = `export default {initialize(){},render({el}){el.textContent='ready';}}`;
const src=fs.readFileSync(process.argv[2],'utf8').replace('__CALMAR_VIEWER_SOURCE__',JSON.stringify(native));
const {default:factory}=await import('data:text/javascript;base64,'+Buffer.from(src).toString('base64'));
URL.createObjectURL=()=> 'data:text/javascript;base64,'+Buffer.from(native).toString('base64');
URL.revokeObjectURL=()=>{};
globalThis.window={location:{href:'http://localhost/user/test/lab'}};
let fetches=0, sends=0, visible;
globalThis.IntersectionObserver=class {constructor(callback){visible=callback;} observe(){} disconnect(){}};
globalThis.fetch=async (url, options)=>{
  fetches++;
  assert.equal(url,'http://localhost/user/test/files/image.nii.gz?v=1');
  assert.equal(options.headers.get('Authorization'),'token fixture');
  return new Response(new Uint8Array([1,2,3]),{headers:{'content-type':'application/gzip'}});
};
async function render(url){
 const descriptor={name:'image.nii.gz',calmar_lazy:true,data:null,url};
 const volume={model_id:'v',get:key=>key==='path'?descriptor:null,on(){},off(){}};
 const volumes=[volume];
 const model={get:()=>volumes,on(){},off(){},send(){sends++;},widget_manager:{kernel:{
   status:'busy',serverSettings:{baseUrl:'http://localhost/user/test/',token:'fixture'}
 }}};
 const widget=factory(),dispose=widget.initialize({model});
 const el={textContent:'',querySelector:()=>null,replaceChildren(){}};
 const before=fetches;
 const rendering=widget.render({model,el});
 await new Promise(resolve=>setImmediate(resolve));
 assert.equal(fetches,before); // Off-screen viewers do not fetch images.
 visible([{isIntersecting:true}]);
 await rendering;
 assert.equal(el.textContent,'ready');assert.equal(descriptor.data.byteLength,3);
 dispose();
}
await render('/user/test/files/image.nii.gz?v=1');
await render('/user/test/files/image.nii.gz?v=1');
assert.equal(fetches,1);assert.equal(sends,0);
'''
    result = subprocess.run(['node', '--input-type=module', '-', str(source)],
                            input=script, text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr
