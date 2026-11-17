const $ = id => document.getElementById(id);
const controls = ['participant','mask','plane','reset','opacity','disconnection'];
let nv, cases, current, busy = false;
const status = message => { $('viewer-status').textContent = message; };
function lock(value) { busy = value; controls.forEach(id => { $(id).disabled = value; }); }
function options(select, items) { select.replaceChildren(...items.map(([value, label]) => new Option(label, value))); }
function selectedCase() { return cases.find(c => c.id === $('participant').value); }
function staticCase(message = 'Interactive viewing is unavailable. Showing the saved report overlay.') {
  $('fallback').hidden = false;
  $('participant').disabled = false;
  ['mask','plane','reset','opacity','disconnection'].forEach(id=>{ $(id).disabled=true; });
  $('map-note').textContent = `Saved ${current.masks[0].label} report overlay for ${current.id}.`;
  status(message);
}
function updateCase() {
  current = selectedCase();
  options($('mask'), current.masks.map((m,i) => [i,m.label]));
  $('fallback').src = current.thumbnail;
  $('fallback').alt = `Saved ${current.masks[0].label} lesion overlay for ${current.id}`;
  $('viewer-report').href = current.report;
  $('case-caption').textContent = `${current.id} · registered ${current.background_label} · MNI152 · neurological view (left is left)`;
  $('disconnection').checked = false;
}
function updateMapNote() {
  const original = current.masks[0].label;
  $('map-note').textContent = `Green: ${current.masks[Number($('mask').value)].label} lesion mask. Warm colours: BCBToolkit disconnection estimate for the ${original} mask, shown from probability 0.5 to 1. Changing the displayed lesion does not recompute this estimate.`;
}
function centerLesion() {
  const mask = nv.volumes[nv.volumes.length-1];
  const dims = mask.hdr.dims, affine = mask.hdr.affine;
  const sums = [0,0,0]; let count = 0;
  // Centre the crosshair on the saved binary mask; this changes the view only.
  for (let i=0; i<mask.img.length; i++) {
    if (mask.img[i] < 0.5) continue;
    sums[0] += i % dims[1];
    sums[1] += Math.floor(i / dims[1]) % dims[2];
    sums[2] += Math.floor(i / (dims[1]*dims[2])); count++;
  }
  if (!count) { nv.scene.crosshairPos=[0.5,0.5,0.5]; return; }
  const voxel = sums.map(v=>v/count);
  const mm = affine.slice(0,3).map(row=>row[0]*voxel[0]+row[1]*voxel[1]+row[2]*voxel[2]+row[3]);
  const frac = nv.mm2frac(mm);
  if (Array.from(frac).every(v=>Number.isFinite(v)&&v>=0&&v<=1)) nv.scene.crosshairPos=frac;
}
async function loadCase() {
  lock(true); status(`Loading ${current.id}…`); $('fallback').hidden = true;
  try {
    const mask = current.masks[Number($('mask').value)];
    const volumes = [{url: current.background, name:`Registered_${current.background_label}.nii.gz`, colormap:'gray'}];
    if ($('disconnection').checked) volumes.push({url:current.disconnectome, name:`BCBToolkit_${current.masks[0].label}.nii.gz`, colormap:'hot', cal_min:0.5, cal_max:1, opacity:0.5});
    volumes.push({url: mask.url, name:mask.label+'.nii.gz', colormap:'green', cal_min:0.5, cal_max:1, opacity:Number($('opacity').value)/100});
    await nv.loadVolumes(volumes);
    if (nv.volumes.length !== volumes.length || nv.volumes.some(v => !v.hdr?.dims || !v.img?.length)) throw new Error('Image volumes could not be decoded.');
    nv.setSliceType(Number($('plane').value));
    centerLesion(); nv.drawScene();
    updateMapNote(); status('');
    $('brain').dataset.ready = current.id;
  } catch (error) {
    $('fallback').hidden = false;
    status(`The interactive image could not load. Showing the saved ${current.masks[0].label} overlay; the full report is available below.`);
    $('brain').dataset.ready = '';
    console.error(error);
  } finally { lock(false); }
}
async function start() {
  try {
    const response = await fetch('cases.json');
    if (!response.ok) throw new Error('Case manifest is unavailable.');
    cases = (await response.json()).cases;
    options($('participant'), cases.map(c => [c.id,c.id]));
    updateCase();
    $('participant').addEventListener('change', () => { updateCase(); nv ? loadCase() : staticCase(); });
    document.querySelectorAll('.explore-case').forEach(button => button.addEventListener('click', async () => {
      if (busy) return;
      $('participant').value=button.dataset.case; updateCase();
      $('explore').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
      nv ? await loadCase() : staticCase();
    }));
    status('Loading the image viewer…');
    const {Niivue} = await import('./vendor/niivue.js');
    const viewer = new Niivue({backColor:[0.063,0.102,0.118,1],show3Dcrosshair:true,isColorbar:false,isRadiologicalConvention:false,dragAndDropEnabled:false});
    await viewer.attachToCanvas($('brain'));
    nv = viewer;
    nv.onLocationChange = data => { $('location').textContent = data.mm ? data.mm.slice(0,3).map(v=>v.toFixed(0)).join(', ')+' mm' : ''; };
    $('mask').addEventListener('change', loadCase);
    $('disconnection').addEventListener('change', loadCase);
    $('plane').addEventListener('change', () => nv.setSliceType(Number($('plane').value)));
    $('opacity').addEventListener('input', () => { $('opacity-value').textContent = $('opacity').value+'%'; nv.setOpacity(nv.volumes.length-1,Number($('opacity').value)/100); });
    $('reset').addEventListener('click', () => { centerLesion(); nv.scene.pan2Dxyzmm=[0,0,0,1]; nv.setRenderAzimuthElevation(110,10); nv.drawScene(); });
    await loadCase();
    // Expose the rendered instance for read-only browser verification.
    window.calmarViewer = nv;
  } catch (error) {
    if (current) staticCase();
    else status('The interactive viewer is unavailable. The saved overlay and participant reports are available below.');
    $('fallback').hidden = false; console.error(error);
  }
}
start();
