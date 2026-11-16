// Saved output only. One Niivue instance and one WebGL canvas for the whole notebook.
const narrow = matchMedia('(max-width: 860px)');
const collapseContents = () => { if (narrow.matches) { const contents = document.querySelector('.nb-toc details'); if (contents) contents.open = false; } };
narrow.addEventListener('change', collapseContents);
collapseContents();
document.querySelectorAll('.saved-tabs').forEach(group => {
  const tabs = [...group.querySelector(':scope > .saved-tab-buttons').children];
  const select = tab => {
    tabs.forEach(t => {
      const selected = t === tab;
      t.setAttribute('aria-selected', selected);
      t.tabIndex = selected ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
    });
  };
  group.classList.add('tabs-ready');
  select(tabs.find(t => t.getAttribute('aria-selected') === 'true') || tabs[0]);
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
      if (event.key === 'ArrowLeft') next = tabs[(i + tabs.length - 1) % tabs.length];
      if (event.key === 'Home') next = tabs[0];
      if (event.key === 'End') next = tabs.at(-1);
      if (next) { event.preventDefault(); select(next); next.focus(); }
    });
  });
});

const make = (tag, className, content) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (content) el.textContent = content;
  return el;
};
let manifest, nv, owner, busy = false, selected = [], config;
const player = make('div', 'inline-player');
const toolbar = make('div', 'viewer-toolbar');
const planeLabel = make('label', '', 'View ');
const plane = make('select');
plane.setAttribute('aria-label', 'Slice view');
[['3', 'All planes'], ['0', 'Axial'], ['1', 'Coronal'], ['2', 'Sagittal'], ['4', '3D']].forEach(([v, l]) => plane.add(new Option(l, v)));
planeLabel.append(plane);
const reset = make('button', '', 'Reset view'); reset.type = 'button';
const close = make('button', '', 'Close viewer'); close.type = 'button';
toolbar.append(planeLabel, reset, close);
const frame = make('div', 'canvas-frame');
const canvas = make('canvas'); canvas.id = 'inline-brain'; canvas.tabIndex = 0;
canvas.setAttribute('aria-label', 'Interactive brain image. Click to move the crosshair, scroll when focused to change slices, or drag in 3D.');
frame.append(canvas);
const coords = make('output', 'viewer-coordinates', 'Coordinates in millimetres');
coords.setAttribute('aria-live', 'off');
const layers = make('div', 'viewer-layers');
const help = make('p', 'viewer-help', 'Click to move the crosshair. Focus the image and scroll to change slices; drag to rotate in 3D. On touchscreens, tap to position and drag to navigate.');
player.append(toolbar, frame, coords, layers, help);
const status = message => { if (owner) owner.querySelector('.viewer-status').textContent = message; };
function lock(value) {
  busy = value;
  document.querySelectorAll('.open-viewer').forEach(b => { b.disabled = value; });
  player.querySelectorAll('button, input, select').forEach(el => { el.disabled = value; });
}
function locationChanged(data) {
  if (data.mm) coords.textContent = Array.from(data.mm).slice(0, 3).map(n => Number(n).toFixed(1)).join(', ') + ' mm';
  if (nv) canvas.dataset.crosshair = JSON.stringify(Array.from(nv.scene.crosshairPos));
}
function release() {
  if (!owner) return;
  player.remove();
  owner.querySelector('.viewer-slot').replaceChildren(make('p', '', 'This viewer is paused. Reopen it here to inspect the saved images.'));
  owner.querySelector('.open-viewer').hidden = false;
  owner.dataset.state = 'paused';
  owner.querySelector('.viewer-status').textContent = 'Paused to share one WebGL canvas across the notebook.';
  owner = null;
}
async function load(preserve = false) {
  lock(true);
  frame.hidden = true;
  const prior = preserve ? Array.from(nv.scene.crosshairPos) : config.crosshair;
  const visible = config.layers.filter((_, i) => i === 0 || selected[i]);
  status('Loading saved images…'); owner.dataset.state = 'loading';
  try {
    await nv.loadVolumes(visible.map(layer => ({url: layer.url, name: layer.name,
      colormap: layer.colormap || 'gray', opacity: layer.opacity ?? (layer === config.layers[0] ? 1 : .5),
      ...(layer.cal_min != null ? {cal_min: layer.cal_min} : {}),
      ...(layer.cal_max != null ? {cal_max: layer.cal_max} : {})})));
    if (nv.volumes.length !== visible.length || nv.volumes.some(v => !v.hdr?.dims || !v.img?.length)) {
      throw new Error('A saved image could not be decoded.');
    }
    nv.scene.crosshairPos = prior || [.5, .5, .5];
    nv.setSliceType(Number(plane.value));
    frame.hidden = false;
    nv.resizeListener(); nv.drawScene();
    locationChanged({mm: nv.frac2mm(nv.scene.crosshairPos)});
    canvas.dataset.loaded = JSON.stringify(visible.map(l => l.label));
    canvas.dataset.crosshair = JSON.stringify(Array.from(nv.scene.crosshairPos));
    owner.dataset.state = 'ready';
    status('Saved images loaded. Display changes are local to this browser; QC remains skipped.');
  } catch (error) {
    frame.hidden = true;
    owner.dataset.state = 'error';
    owner.querySelector('.open-viewer').hidden = false;
    owner.querySelector('.open-viewer').textContent = 'Retry inline viewer';
    status('This image could not load. Retry the viewer, or read the saved figures and tables at this step. No analysis has been run.');
    canvas.dataset.loaded = '[]';
  } finally { lock(false); }
}
function buildLayers() {
  layers.replaceChildren();
  config.layers.forEach((layer, i) => {
    if (!i) return;
    const row = make('div', 'layer-row');
    const label = make('label');
    const toggle = make('input'); toggle.type = 'checkbox'; toggle.checked = selected[i];
    toggle.setAttribute('aria-label', 'Show ' + layer.label);
    const swatch = make('span', 'layer-swatch'); swatch.style.backgroundColor = layer.color || '#888';
    label.append(toggle, swatch, document.createTextNode(layer.label));
    const opacity = make('input'); opacity.type = 'range'; opacity.min = '0'; opacity.max = '100';
    opacity.value = String(Math.round((layer.opacity > 0 ? layer.opacity : layer.saved_opacity ?? .5) * 100));
    opacity.setAttribute('aria-label', layer.label + ' opacity');
    const value = make('output', '', opacity.value + '%');
    const scale = make('small', 'layer-scale', layer.cal_min != null ? `Display range ${layer.cal_min}–${layer.cal_max}` : 'Image intensity');
    toggle.addEventListener('change', async () => {
      if (busy) return;
      selected[i] = toggle.checked;
      layer.opacity = Number(opacity.value) / 100;
      await load(true);
    });
    opacity.addEventListener('input', () => {
      value.textContent = opacity.value + '%'; layer.opacity = Number(opacity.value) / 100;
      const index = config.layers.slice(0, i + 1).filter((_, k) => k === 0 || selected[k]).length - 1;
      if (selected[i] && nv.volumes[index]) nv.setOpacity(index, layer.opacity);
      canvas.dataset.opacity = opacity.value;
    });
    row.append(label, opacity, value, scale); layers.append(row);
  });
}
async function open(element) {
  if (busy) return;
  lock(true);
  release(); owner = element;
  frame.hidden = true;
  owner.dataset.state = 'loading';
  owner.querySelector('.viewer-slot').replaceChildren(player);
  owner.querySelector('.open-viewer').hidden = true;
  status('Opening the image viewer…');
  coords.textContent = 'Coordinates in millimetres';
  try {
    if (!manifest) {
      const response = await fetch('inline-viewers.json');
      if (!response.ok) throw new Error('Viewer manifest unavailable');
      manifest = await response.json();
    }
    config = structuredClone(manifest[owner.dataset.viewer]);
    if (!config) throw new Error('Saved viewer not found');
    selected = config.layers.map(l => l.opacity > 0);
    plane.value = String(config.plane ?? 3);
    buildLayers();
    if (!nv) {
      const {Niivue} = await import('./vendor/niivue.js');
      const viewer = new Niivue({backColor: [0, 0, 0, 1], isRadiologicalConvention: false,
        isColorbar: false, dragAndDropEnabled: false, drawingEnabled: false,
        scrollRequiresFocus: true, show3Dcrosshair: true, multiplanarForceRender: false});
      // These saved CALMaR colour names are not bundled in standalone Niivue.
      // Register their intended RGB ramps rather than falling back to grayscale.
      for (const [name, rgb] of [['yellow', [255,255,0]], ['cyan', [0,255,255]], ['magenta', [255,0,255]]]) {
        viewer.addColormap(name, {R:[0,rgb[0]],G:[0,rgb[1]],B:[0,rgb[2]],A:[0,128],I:[0,255]});
      }
      await viewer.attachToCanvas(canvas);
      nv = viewer;
      nv.onLocationChange = locationChanged;
    }
    await load();
  } catch (error) {
    frame.hidden = true;
    // A failed WebGL import must not affect the saved notebook or other tabs.
    owner.dataset.state = 'error';
    owner.querySelector('.open-viewer').hidden = false;
    status('Interactive viewing needs WebGL2 and JavaScript assets. Saved figures and tables remain available. You can retry here.');
  } finally { lock(false); }
}
document.querySelectorAll('.open-viewer').forEach(button => button.addEventListener('click', () => open(button.closest('.inline-viewer'))));
plane.addEventListener('change', () => { if (nv && !busy) nv.setSliceType(Number(plane.value)); });
reset.addEventListener('click', () => {
  if (!nv || busy) return;
  nv.scene.crosshairPos = config.crosshair || [.5, .5, .5];
  nv.scene.pan2Dxyzmm = [0, 0, 0, 1]; nv.scene.renderAzimuth = 110; nv.scene.renderElevation = 10;
  nv.scene.volScaleMultiplier = 1; nv.drawScene();
  locationChanged({mm: nv.frac2mm(nv.scene.crosshairPos)});
  canvas.dataset.crosshair = JSON.stringify(Array.from(nv.scene.crosshairPos));
});
close.addEventListener('click', () => { if (!busy) release(); });
new ResizeObserver(() => { if (nv && owner && !busy) nv.resizeListener(); }).observe(frame);
document.querySelectorAll('.open-viewer').forEach(b => { b.dataset.enhanced = 'true'; });
