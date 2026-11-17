// Browser verification of the actual static bundle, locally or after deployment.
const {chromium} = require('../../../analyses/unattended-demo/web-tools/node_modules/playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const root = path.resolve(process.argv[2]), output = path.resolve(process.argv[3]);
fs.mkdirSync(output, {recursive:true});
const types = {'.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.json':'application/json', '.png':'image/png', '.gz':'application/gzip'};
const server = http.createServer((req,res) => {
  const file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url,'http://localhost').pathname).replace(/\/$/, '/index.html'));
  if (!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {res.writeHead(404);res.end();return;}
  res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});
const completed = [];
async function reveal(locator) {
  await locator.evaluate(el => {
    const ancestors=[];
    for (let p=el.parentElement;p;p=p.parentElement) ancestors.push(p);
    ancestors.reverse().forEach(p => {
      if (p.tagName==='DETAILS') p.open=true;
      if (p.getAttribute('role')==='tabpanel' && p.hidden) document.getElementById(p.getAttribute('aria-labelledby')).click();
    });
  });
}
async function ready(view) {
  await view.page().waitForFunction(el => ['ready','error'].includes(el.dataset.state), await view.elementHandle(), {timeout:120000});
  assert.equal(await view.getAttribute('data-state'),'ready',await view.locator('.viewer-status').textContent());
}
async function main() {
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  const browser = await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const base = process.env.CALMAR_VERIFY_URL || `http://127.0.0.1:${server.address().port}/`;
  try {
    const page = await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
    const errors=[], requests=[];
    page.on('pageerror', e=>errors.push(e.message));
    page.on('console', m=>{if(m.type()==='error'||m.text().includes('No color map named'))errors.push(m.text());});
    page.on('response', r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`);});
    page.on('request',r=>requests.push(r.url()));
    await page.addInitScript(() => {
      const original = HTMLCanvasElement.prototype.getContext;
      window.webglCanvases = new Set();
      HTMLCanvasElement.prototype.getContext = function(type,...args) {
        const context=original.call(this,type,...args);
        if(type.startsWith('webgl')&&context)window.webglCanvases.add(this);
        return context;
      };
    });
    await page.goto(base,{waitUntil:'networkidle'});
    assert.equal(await page.locator('canvas').count(),0);
    assert.equal(requests.filter(r=>r.includes('/volumes/')||r.includes('/vendor/niivue')).length,0,'Images must not load before opening a viewer');
    const build = await (await page.request.get(base+'build.json')).json();
    assert.equal(await page.locator('article.nb img').count(),build.figures);
    assert(build.figures>30,'HTML embedded figures must be counted');
    assert.equal(await page.locator('.project-nav').count(),1);
    assert.equal(await page.locator('script[type="application/vnd.jupyter.widget-state+json"]').count(),0);
    await page.screenshot({path:path.join(output,'desktop-top.png')});
    const manifest=await (await page.request.get(base+'inline-viewers.json')).json();
    const loaded=new Set();
    const views=page.locator('.inline-viewer');
    const count=await views.count();
    assert(count>=20,'All saved views and four report viewers should be inline');
    for(let i=0;i<count;i++) {
      const view=views.nth(i), id=await view.getAttribute('data-viewer');
      await reveal(view);
      await view.locator('.open-viewer').click();
      await ready(view);
      assert.equal(await page.locator('canvas').count(),1);
      assert.equal(await page.evaluate(()=>window.webglCanvases.size),1,'Only one WebGL canvas may be allocated');
      manifest[id].layers.filter((l,k)=>!k||l.opacity>0).forEach(l=>loaded.add(l.url));
      // Exercise every distinct saved layer, including ones hidden in the snapshot.
      for(let j=1;j<manifest[id].layers.length;j++) {
        const layer=manifest[id].layers[j];
        if(loaded.has(layer.url)) continue;
        const check=view.locator('.layer-row input[type="checkbox"]').nth(j-1);
        await check.check(); await ready(view); loaded.add(layer.url);
        assert((await view.locator('canvas').getAttribute('data-loaded')).includes(layer.label));
        await check.uncheck(); await ready(view);
      }
      if(i===0) {
        await view.locator('select[aria-label="Slice view"]').selectOption('0');
        const brain=view.locator('canvas');
        await view.screenshot({path:path.join(output,'inline-before-interaction.png')});
        const before=await brain.getAttribute('data-crosshair');
        const size=await brain.boundingBox();
        await brain.click({position:{x:size.width*.55,y:size.height*.4}});
        await page.waitForFunction(old=>document.querySelector('canvas').dataset.crosshair!==old,before);
        const clicked=await brain.getAttribute('data-crosshair');
        await page.mouse.wheel(0,100);
        await page.waitForFunction(old=>document.querySelector('canvas').dataset.crosshair!==old,clicked);
        await view.locator('.layer-row input[type="range"]').first().fill('0');
        const zero=await brain.screenshot();
        await view.locator('.layer-row input[type="range"]').first().fill('80');
        const opaque=await brain.screenshot();
        assert(!zero.equals(opaque),'Changing overlay opacity must change the actual rendered image');
        await view.screenshot({path:path.join(output,'inline-native.png')});
        await view.locator('select[aria-label="Slice view"]').selectOption('4');
        await brain.dragTo(brain,{sourcePosition:{x:220,y:180},targetPosition:{x:300,y:220}});
        await view.screenshot({path:path.join(output,'inline-3d.png')});
        await view.getByRole('button',{name:'Reset view',exact:true}).click();
        await view.locator('select[aria-label="Slice view"]').selectOption('3');
      }
      if(id.startsWith('report-')) {
        await view.screenshot({path:path.join(output,id+'.png')});
        assert((await view.locator('.viewer-heading').textContent()).includes(manifest[id].subject));
      }
      completed.push({id,layers:manifest[id].layers.length});
      console.log('Verified',id,manifest[id].layers.length,'layers');
    }
    assert.equal(Object.keys(manifest).filter(id=>id.startsWith('report-')).length,4);
    // A real saved tab and accordion, with keyboard navigation.
    const reportTab=page.getByRole('tab',{name:'Report',exact:true}).first();
    await reveal(reportTab); await reportTab.click();
    await reportTab.press('ArrowRight');
    assert.equal(await page.getByRole('tab',{name:'Brain viewer',exact:true}).first().getAttribute('aria-selected'),'true');
    await reportTab.click();
    const overview=page.locator('details.saved-accordion').filter({has:page.locator('summary').filter({hasText:'Participant context and lesion overview'})}).first();
    await overview.locator(':scope > summary').click();
    await overview.locator(':scope > summary').click();
    assert(await overview.getAttribute('open')!==null);
    await overview.screenshot({path:path.join(output,'saved-report-figure.png')});
    await page.getByLabel('Colour theme').selectOption('dark');
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.screenshot({path:path.join(output,'desktop-dark.png')});
    await page.getByLabel('Colour theme').selectOption('light');
    await page.setViewportSize({width:390,height:844});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.screenshot({path:path.join(output,'mobile-top.png')});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Mobile horizontal overflow');
    const mobileView=views.first();
    await mobileView.locator('.open-viewer').click(); await ready(mobileView);
    await mobileView.locator('select').selectOption('0');
    await mobileView.locator('canvas').click({position:{x:180,y:120}});
    await mobileView.screenshot({path:path.join(output,'mobile-viewer.png')});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'Viewer causes mobile overflow');
    await page.goto(base+'notebook.html#single-subject-test',{waitUntil:'networkidle'});
    assert.equal(await page.locator('.inline-viewer').count(),count);
    assert(await page.locator('#single-subject-test').isVisible());
    assert.deepEqual(errors,[]);
    const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});
    await nojs.goto(base,{waitUntil:'networkidle'});
    assert.equal(await nojs.locator('article.nb img').count(),build.figures);
    assert.equal(await nojs.locator('.saved-tab-panel[hidden]').count(),0);
    assert.equal(await nojs.locator('.open-viewer:visible').count(),0);
    await nojs.close();
    const fallback=await browser.newPage();
    await fallback.route('**/vendor/niivue.js',r=>r.abort());
    await fallback.goto(base,{waitUntil:'networkidle'});
    await fallback.locator('.open-viewer').first().click();
    await fallback.waitForFunction(()=>document.querySelector('.inline-viewer').dataset.state==='error');
    assert(await fallback.locator('.open-viewer').first().isEnabled());
    assert(await fallback.locator('.saved-accordion').count()>0);
    await fallback.locator('.inline-viewer').first().screenshot({path:path.join(output,'viewer-unavailable.png')});
    await fallback.close();
    const missing=await browser.newPage();
    await missing.route('**/volumes/*',r=>r.fulfill({status:404,body:'Missing test image'}));
    await missing.goto(base,{waitUntil:'networkidle'});
    await missing.locator('.open-viewer').first().click();
    await missing.waitForFunction(()=>document.querySelector('.inline-viewer').dataset.state==='error',null,{timeout:90000});
    assert(await missing.locator('.viewer-status').first().textContent().then(s=>s.includes('could not load')));
    assert.equal(await missing.locator('.canvas-frame').isVisible(),false);
    await missing.unroute('**/volumes/*');
    await missing.locator('.open-viewer').first().click(); await ready(missing.locator('.inline-viewer').first());
    await missing.route('**/volumes/*',r=>r.fulfill({status:404,body:'Missing next participant'}));
    const nextParticipant=missing.locator('[data-viewer="report-sub-M2004"]');
    await reveal(nextParticipant); await nextParticipant.locator('.open-viewer').click();
    await missing.waitForFunction(()=>document.querySelector('[data-viewer="report-sub-M2004"]').dataset.state==='error',null,{timeout:90000});
    assert.equal(await nextParticipant.locator('.canvas-frame').isVisible(),false,'A failed switch must never show the previous participant image');
    await missing.close();
    const attach=await browser.newPage();
    await attach.addInitScript(()=>{
      const original=HTMLCanvasElement.prototype.getContext;let reject=true;
      HTMLCanvasElement.prototype.getContext=function(type,...args){if(type==='webgl2'&&reject){reject=false;return null;}return original.call(this,type,...args);};
    });
    await attach.goto(base,{waitUntil:'networkidle'});
    await attach.locator('.open-viewer').first().click();
    await attach.waitForFunction(()=>document.querySelector('.inline-viewer').dataset.state==='error');
    await attach.locator('.open-viewer').first().click(); await ready(attach.locator('.inline-viewer').first());
    await attach.close();
    const touch=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:1});
    await touch.goto(base,{waitUntil:'networkidle'});
    assert.equal(await touch.locator('.nb-toc details').getAttribute('open'),null);
    await touch.screenshot({path:path.join(output,'mobile-fresh.png')});
    await touch.locator('.open-viewer').first().tap(); await ready(touch.locator('.inline-viewer').first());
    await touch.locator('.inline-viewer').first().locator('select').selectOption('0');
    const touchCanvas=touch.locator('canvas');
    await touchCanvas.scrollIntoViewIfNeeded();
    const touchBox=await touchCanvas.boundingBox();
    const oldTouch=await touchCanvas.getAttribute('data-crosshair');
    // Niivue defers single-touch handling to distinguish multi-touch. Hold a
    // realistic 60 ms tap rather than Playwright's zero-duration tap shortcut.
    const touchSession=await touch.context().newCDPSession(touch);
    await touchSession.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:touchBox.x+touchBox.width*.55,y:touchBox.y+touchBox.height*.4}]});
    await touch.waitForTimeout(60);
    await touchSession.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
    await touch.waitForFunction(old=>document.querySelector('canvas').dataset.crosshair!==old,oldTouch);
    assert(await touch.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
    await touch.locator('.inline-viewer').first().screenshot({path:path.join(output,'mobile-touch-viewer.png')});
    await touch.close();
    fs.writeFileSync(path.join(output,'verification.json'),JSON.stringify({state:'passed',base,revision:build.notebook_commit,figures:build.figures,viewers:completed,uniqueVolumesLoaded:loaded.size,webglCanvases:1,desktop:true,mobile:true,touchInteraction:true,themes:true,tabs:true,accordions:true,mouseSlices:true,opacity:true,noJavaScript:true,missingVolume:true,failedSwitchHidesPriorImage:true,webglAttachRetry:true,missingViewerModule:true,errors},null,2)+'\n');
  } finally {await browser.close();server.close();}
}
main().catch(error=>{fs.writeFileSync(path.join(output,'failure.json'),JSON.stringify({error:String(error),stack:error.stack,completed},null,2));console.error(error);server.close();process.exitCode=1;});
