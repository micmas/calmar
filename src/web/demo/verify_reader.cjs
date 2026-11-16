// Run from the project root; use the pinned Playwright installed by step 62.
const {chromium} = require('../../../analyses/unattended-demo/web-tools/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const root = path.resolve(process.argv[2]);
const output = path.resolve(process.argv[3]);
fs.mkdirSync(output,{recursive:true});
const types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.png':'image/png','.gz':'application/gzip'};
const server = http.createServer((req,res)=>{
  const file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/\/$/,'/index.html'));
  if(!file.startsWith(root+path.sep)||!fs.existsSync(file)||!fs.statSync(file).isFile()){res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type',types[path.extname(file)]||'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});
async function main(){
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  try {
    const page=await browser.newPage({viewport:{width:1440,height:1050},deviceScaleFactor:1});
    const errors=[];
    page.on('pageerror',e=>{errors.push(e.message);console.error(e.message);});
    page.on('console',m=>{if(m.type()==='error'){errors.push(m.text());console.error(m.text());}});
    page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
    const base=process.env.CALMAR_VERIFY_URL || `http://127.0.0.1:${server.address().port}/`;
    await page.goto(base,{waitUntil:'networkidle'});
    await page.waitForFunction(()=>window.calmarViewer && document.getElementById('brain').dataset.ready==='sub-M2001',null,{timeout:90000});
    await page.screenshot({path:path.join(output,'desktop.png'),fullPage:true});
    const cases=await page.locator('#participant option').evaluateAll(options=>options.map(o=>o.value));
    const results=[];
    for(const id of cases){
      await page.selectOption('#participant',id);
      await page.waitForFunction(id=>document.getElementById('brain').dataset.ready===id && !document.getElementById('participant').disabled,id,{timeout:90000});
      const masks=await page.locator('#mask option').count();
      for(let i=0;i<masks;i++){
        await page.selectOption('#mask',String(i));
        await page.waitForFunction(()=>!document.getElementById('mask').disabled && !!document.getElementById('brain').dataset.ready,null,{timeout:90000});
        const images=await page.evaluate(()=>window.calmarViewer.volumes.map(v=>({name:v.name,shape:Array.from(v.hdr.dims),affine:v.hdr.affine,voxels:v.img.length})));
        assert.equal(images.length,2);assert(images.every(v=>v.voxels>100));
        assert.equal(images[1].name,(await page.locator('#mask option:checked').textContent())+'.nii.gz');
        assert.deepEqual(images[0].shape.slice(1,4),images[1].shape.slice(1,4));
        assert(images[0].affine.flat().every((v,j)=>Math.abs(v-images[1].affine.flat()[j])<0.001));
        results.push({id,mask:i,images});
      }
      await page.locator('#disconnection').check();
      await page.waitForFunction(()=>!document.getElementById('disconnection').disabled,null,{timeout:90000});
      assert.equal(await page.evaluate(()=>window.calmarViewer.volumes.length),3);
      const names=await page.evaluate(()=>window.calmarViewer.volumes.map(v=>v.name));
      assert(names[1].startsWith('BCBToolkit_'));assert(!names[2].startsWith('BCBToolkit_'));
      await page.locator('.viewer-shell').screenshot({path:path.join(output,id+'.png')});
    }
    await page.selectOption('#participant','sub-M2001');
    await page.waitForFunction(()=>!document.getElementById('participant').disabled,null,{timeout:90000});
    await page.selectOption('#plane','0');
    await page.locator('#opacity').fill('20');
    assert.equal(await page.evaluate(()=>window.calmarViewer.volumes[1].opacity),0.2);
    await page.selectOption('#plane','4');
    await page.locator('.viewer-shell').screenshot({path:path.join(output,'3d.png')});
    await page.selectOption('#plane','3');
    await page.locator('#reset').click();
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>window.scrollTo({top:0,behavior:'instant'}));
    await page.screenshot({path:path.join(output,'mobile.png'),fullPage:true});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile overflow');
    await page.goto(base+'notebook.html',{waitUntil:'networkidle'});
    assert.equal(await page.locator('script[type="application/vnd.jupyter.widget-state+json"]').count(),0);
    assert(await page.locator('details.saved-cell').count()>0);
    assert.deepEqual(errors,[]);
    const fallback=await browser.newPage({viewport:{width:390,height:844}});
    await fallback.route('**/vendor/niivue.js',route=>route.abort());
    await fallback.goto(base,{waitUntil:'networkidle'});
    await fallback.waitForFunction(()=>document.getElementById('viewer-status').textContent.includes('unavailable'));
    assert(await fallback.locator('#fallback').isVisible());
    assert.equal(await fallback.locator('.case-card').count(),4);
    assert(await fallback.locator('#fallback').evaluate(img=>img.complete && img.naturalWidth>0));
    await fallback.selectOption('#participant','sub-strokecase0002');
    assert((await fallback.locator('#fallback').getAttribute('src')).includes('sub-strokecase0002'));
    await fallback.locator('[data-case="sub-M2004"]').click();
    assert.equal(await fallback.locator('#participant').inputValue(),'sub-M2004');
    await fallback.screenshot({path:path.join(output,'fallback.png'),fullPage:true});
    await fallback.close();
    const missing=await browser.newPage();
    await missing.route('**/volumes/*',route=>route.fulfill({status:404,body:'Missing test volume'}));
    await missing.goto(base,{waitUntil:'networkidle'});
    await missing.waitForFunction(()=>document.getElementById('viewer-status').textContent.includes('could not load'));
    assert(await missing.locator('#fallback').isVisible());
    assert(await missing.locator('#participant').isEnabled());
    await missing.close();
    const nojs=await browser.newPage({javaScriptEnabled:false});
    await nojs.goto(base,{waitUntil:'networkidle'});
    assert.equal(await nojs.locator('.case-card').count(),4);
    assert(await nojs.locator('#fallback').isVisible());
    assert(!(await nojs.locator('.toolbar').isVisible()));
    await nojs.close();
    fs.writeFileSync(path.join(output,'verification.json'),JSON.stringify({passed:true,cases:results,errors},null,2));
    console.log('PASS: all four participants, all ten masks, disconnection, opacity, slice controls, mobile layout and notebook.');
  }finally{await browser.close();server.close();}
}
main().catch(e=>{console.error(e);server.close();process.exitCode=1;});
