"""One results panel with shared selection and optional, lazy cohort summaries."""

from html import escape
import json
from pathlib import Path
import textwrap

import ipywidgets as widgets
import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
from nilearn import datasets, image

from . import colors
from .atlas_ui import OverlapSelection, overlap_table
from .masks import MASK_LABELS
from .qc_decisions import report_qc_notice

METRICS = {'Lesion in ROI %': 'lesion_in_roi_percent', 'ROI coverage %': 'roi_coverage_percent'}
NETWORKS = ('Vis', 'SomMot', 'DorsAttn', 'SalVentAttn', 'Limbic', 'Cont', 'Default')


def _label(pair):
    return ' '.join(pair).strip()


def cohort_matrix(df, pairs, metric, limit):
    """Keep the full cohort; distinguish completed zero overlap from missing data."""
    order = df.groupby('region')[metric].max().sort_values(ascending=False).head(limit).index
    selected = df[df.region.isin(order)].copy()
    selected['participant'] = [_label(p) for p in zip(selected.subject, selected.session)]
    matrix = selected.pivot_table(index='region', columns='participant', values=metric, fill_value=0).reindex(order)
    statuses = df.attrs.get('overlap_status', {})
    for pair in pairs:
        label = _label(pair)
        if label not in matrix.columns:
            complete = statuses.get(json.dumps(list(pair)), {}).get('status') == 'complete'
            matrix[label] = 0. if complete else np.nan
    return matrix.reindex(columns=[_label(p) for p in pairs])


def build_results_panel(tables, entries, default_atlas, atlas_objects, helpers, *,
                        deriv_path_for, inventory_for, deriv_dir, atlas_dir,
                        reports_dir, threshold=.5):
    entries = [dict(e) for e in entries]
    by_pair = {(e['subject'], e.get('session') or ''): e for e in entries}
    selection = OverlapSelection(tables, default_atlas, list(by_pair))
    if not selection.tables:
        return None
    table, message, chart = widgets.HTML(), widgets.HTML(), helpers.Output()
    viewer = helpers.fresh_viewer('report_viewer', height=420)
    tabs = widgets.Tab(children=[table, widgets.VBox([message, viewer]), chart])
    for i, title in enumerate(('Atlas table', 'Brain and selected mask', 'Region chart')):
        tabs.set_title(i, title)
    metric = widgets.Dropdown(options=list(METRICS), description='Chart measure:',
                             style={'description_width': 'initial'})
    top_n = widgets.IntSlider(value=20, min=5, max=50, description='Chart top N:',
                             continuous_update=False, style={'description_width': 'initial'})
    chart_controls = widgets.HBox([metric, top_n], layout=widgets.Layout(flex_flow='row wrap', display='none'))
    heatmap, networks, frequency = helpers.Output(), helpers.Output(), widgets.VBox()
    group_tabs = widgets.Tab(children=[heatmap, frequency, networks])
    for i, title in enumerate(('Across participants', 'Lesion frequency', 'Schaefer networks')):
        group_tabs.set_title(i, title)
    group = widgets.Accordion(children=[widgets.VBox([
        widgets.HTML('These summaries combine all configured participants using the mask source selected above. '
                     'They do not change when you select a different individual.'), group_tabs])], selected_index=None)
    group.set_title(0, 'Group summaries (optional)')
    export = widgets.VBox()
    state = dict(brain=True, chart=True, heatmap=True, networks=True, group_panel=None, active=True)

    def current_label():
        return f'{selection.atlas.value} · {selection.source.label}'

    def show_brain():
        _, sub, ses = selection.current()
        entry = by_pair[(sub, ses)]
        background = Path(deriv_path_for(entry)) / 'Subject_in_MNI.nii.gz'
        if not background.exists():
            viewer.load_volumes([])
            message.value = f'Brain viewer needs Subject_in_MNI.nii.gz for {escape(_label((sub, ses)))}. Run the MNI warp first.'
            return
        specs = [dict(path=str(background), colormap='gray', opacity=1.)]
        notes = []
        name = selection.atlas.value
        atlas_path = Path(deriv_dir) / f'{name}_atlas.nii.gz'
        maps = getattr(atlas_objects.get(name), 'maps', None)
        if not atlas_path.exists() and isinstance(maps, (str, Path)):
            atlas_path = Path(maps)
        elif not atlas_path.exists() and hasattr(maps, 'to_bytes'):
            nib.save(maps, str(atlas_path))
        if atlas_path.exists():
            specs.append(dict(path=str(atlas_path), colormap='viridis', opacity=.25))
        else:
            notes.append('Atlas image unavailable; the overlap table is still available.')
        lesion = inventory_for(entry).get(selection.source.value, {}).get('MNI')
        if lesion is not None and Path(lesion).exists():
            specs.append(dict(path=str(lesion), colormap=colors.color(selection.source.value),
                              opacity=.7, cal_min=threshold, cal_max=1.))
        else:
            notes.append(f'{selection.source.label} MNI mask unavailable; run its warp step.')
        helpers.set_volumes(viewer, specs)
        message.value = escape(' '.join(notes))
        state['brain'] = False

    def show_chart():
        df, sub, ses = selection.current()
        key = METRICS[metric.value]
        selected = df[(df.subject == sub) & (df.session == ses)].sort_values(key, ascending=False).head(top_n.value).iloc[::-1]
        chart.outputs = ()
        if selected.empty:
            chart.append_stdout('No positive overlap rows for this participant. See the Atlas table for availability.')
        else:
            fig, ax = plt.subplots(figsize=(9, max(2.5, .42*len(selected)+1)))
            labels = ['\n'.join(textwrap.wrap(str(r), 38)) for r in selected.region]
            ax.barh(labels, selected[key], color='#3b6ea8')
            ax.set_xlabel(metric.value)
            ax.set_title(f'{current_label()} · {_label((sub, ses))} — top {len(selected)} regions')
            ax.grid(axis='x', linestyle=':', alpha=.5)
            fig.tight_layout(); plt.close(fig)
            chart.append_display_data(fig)
        state['chart'] = False

    def show_heatmap():
        df, _, _ = selection.current()
        heatmap.outputs = ()
        matrix = cohort_matrix(df, list(by_pair), METRICS[metric.value], top_n.value)
        if matrix.empty:
            heatmap.append_stdout('No positive atlas-overlap rows for this cohort and mask.')
        else:
            fig, ax = plt.subplots(figsize=(max(6, .4*len(matrix.columns)+4), max(3, .35*len(matrix)+2)))
            cmap = plt.get_cmap('magma').with_extremes(bad='#888888')
            plotted = ax.imshow(matrix.to_numpy(dtype=float), aspect='auto', cmap=cmap)
            ax.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=75, ha='right', fontsize=8)
            ax.set_yticks(range(len(matrix)), ['\n'.join(textwrap.wrap(str(r), 30)) for r in matrix.index], fontsize=8)
            ax.set_title(f'{current_label()} · {metric.value}\nGray = unavailable or not calculated')
            fig.colorbar(plotted, ax=ax, label=metric.value)
            fig.tight_layout(); plt.close(fig)
            heatmap.append_display_data(fig)
        state['heatmap'] = False

    def show_networks():
        networks.outputs = ()
        df = selection.tables.get(f'Schaefer400_{selection.source.value}')
        if df is None or df.empty:
            networks.append_stdout('Schaefer400 overlap is unavailable for the selected mask source.')
        else:
            df = df.copy()
            df['network'] = df.region.astype(str).map(lambda r: next((n for n in NETWORKS if n in r), 'Other'))
            summary = df.groupby(['subject', 'session', 'network']).lesion_in_roi_percent.sum().unstack(fill_value=0)
            # Include missing participants explicitly instead of silently dropping them.
            for pair in by_pair:
                if pair not in summary.index:
                    complete = df.attrs.get('overlap_status', {}).get(json.dumps(list(pair)), {}).get('status') == 'complete'
                    summary.loc[pair, :] = 0. if complete else np.nan
            summary = summary.reindex(list(by_pair))
            columns = [n for n in (*NETWORKS, 'Other') if n in summary]
            fig, ax = plt.subplots(figsize=(max(6, .5*len(summary)+3), 5))
            bottom = np.zeros(len(summary)); x = np.arange(len(summary))
            for name in columns:
                values = summary[name].to_numpy(dtype=float)
                ax.bar(x, values, bottom=bottom, label=name); bottom += values
            for i, missing in enumerate(summary.isna().all(axis=1)):
                if missing: ax.text(i, 0, 'Unavailable', rotation=90, va='bottom', ha='center', fontsize=8)
            ax.set_xticks(x, [_label(p) for p in summary.index], rotation=75, ha='right', fontsize=8)
            ax.set_ylabel('Sum of lesion-in-ROI % (Schaefer regions)')
            ax.set_title(f'Schaefer400 · Yeo 7 networks · {selection.source.label} mask')
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
            fig.tight_layout(); plt.close(fig)
            networks.append_display_data(fig)
        state['networks'] = False

    def draw_visible(*_):
        if not state['active']: return
        chart_controls.layout.display = '' if tabs.selected_index == 2 or (group.selected_index is not None and group_tabs.selected_index == 0) else 'none'
        if tabs.selected_index == 1 and state['brain']: show_brain()
        if tabs.selected_index == 2 and state['chart']: show_chart()
        if group.selected_index is None: return
        if group_tabs.selected_index == 0 and state['heatmap']: show_heatmap()
        elif group_tabs.selected_index == 2 and state['networks']: show_networks()
        elif group_tabs.selected_index == 1 and state['group_panel'] is None:
            panel = build_group_panel(entries, inventory_for, helpers, source=selection.source,
                                      reports_dir=reports_dir, atlas_dir=atlas_dir, threshold=threshold)
            state['group_panel'] = panel
            frequency.children = (panel['widget'],)

    def update(*, subject_only=False):
        if not state['active']: return
        df, sub, ses = selection.current()
        entry = by_pair[(sub, ses)]
        table.value = report_qc_notice(Path(deriv_path_for(entry)), entry) + overlap_table(
            df, sub, ses, selection.atlas.value, selection.source.value)
        state.update(brain=True, chart=True)
        if not subject_only: state.update(heatmap=True, networks=True)
        draw_visible()

    def chart_settings(*_):
        state.update(chart=True, heatmap=True)
        draw_visible()

    def close():
        state['active'] = False
        if state['group_panel']: state['group_panel']['close']()
        viewer.close()
        widget.close()

    selection.observe(update)
    tabs.observe(draw_visible, names='selected_index')
    group.observe(draw_visible, names='selected_index')
    group_tabs.observe(draw_visible, names='selected_index')
    metric.observe(chart_settings, names='value'); top_n.observe(chart_settings, names='value')
    widget = widgets.VBox([widgets.HTML('<h3>Preview and export results</h3>'), selection.widget,
                           chart_controls, tabs, export, group])
    update()
    return dict(selection=selection, atlas=selection.atlas, source=selection.source, subject=selection.subject,
                viewer=viewer, message=message, report=table, tabs=tabs, widget=widget, show_brain=show_brain,
                chart=chart, metric=metric, top_n=top_n, group=group, group_tabs=group_tabs,
                heatmap=heatmap, networks=networks, state=state, export=export, close=close)


def build_group_panel(entries, inventory_for, helpers, *, source, reports_dir, atlas_dir, threshold=.5):
    """Optional frequency calculation; nothing is computed until Build is clicked."""
    build = widgets.Button(description='Build selected group map', button_style='primary', icon='play')
    status, output, preview = widgets.HTML(), helpers.Output(), widgets.VBox()
    state = {'viewer': None, 'active': True}

    def paths():
        return [Path(p) for e in entries if (p := inventory_for(e).get(source.value, {}).get('MNI')) is not None and Path(p).is_file()]

    def select(*_):
        preview.children = ()
        if state['viewer'] is not None: state['viewer'].load_volumes([])
        count = len(paths())
        status.value = (f'<b>{escape(source.label)} group lesion frequency</b> — {count} of {len(entries)} participants. '
                        'Colour shows the fraction with a lesion at each voxel; this is not a disconnectome map. '
                        'Use Build to calculate it for the selected mask source.')
        build.disabled = count == 0 or not state['active']
        output.outputs = ()

    def compute(_=None):
        if not state['active']: return
        build.disabled = True
        output.outputs = ()
        try:
            available = paths()
            if not available:
                output.append_stdout('No usable MNI masks for this source.'); return
            ref = nib.load(available[0]); accum = np.zeros(ref.shape, dtype=np.float32); used = 0
            for path in available:
                try:
                    img = nib.load(path)
                    if img.shape != ref.shape or not np.allclose(img.affine, ref.affine):
                        img = image.resample_to_img(img, ref, interpolation='nearest', force_resample=True, copy_header=True)
                    accum += (img.get_fdata() > threshold).astype(np.float32); used += 1
                except Exception as error:
                    output.append_stdout(f'{path.name}: {error}\n')
            if not used:
                output.append_stdout('No usable lesions — group map not built.'); return
            frequency = nib.Nifti1Image(accum/used, ref.affine, ref.header)
            target = Path(reports_dir) / f'group_lesion_frequency_{source.value}.nii.gz'
            nib.save(frequency, target)
            background = Path(atlas_dir) / 'mni152_t1_2mm.nii.gz'
            if not background.exists(): nib.save(datasets.load_mni152_template(resolution=2), background)
            if state['viewer'] is None:
                state['viewer'] = helpers.fresh_viewer('group_overlap', height=420, colorbar=True, colorbar_height=.05)
            helpers.set_volumes(state['viewer'], [dict(path=str(background), colormap='gray', opacity=1.),
                dict(path=str(target), colormap=colors.color(source.value), opacity=.9, cal_min=.5/used, cal_max=1.)])
            preview.children = (state['viewer'],)
            output.append_stdout(f'Group map mask source: {source.value} ({used} of {len(entries)} participants)\nSaved {target.name}')
        except Exception as error:
            output.append_stdout(f'Could not build group map: {error}')
        finally:
            build.disabled = not state['active'] or not paths()

    def close():
        state['active'] = False
        build.disabled = True
        source.unobserve(select, names='value')
        if state['viewer'] is not None: state['viewer'].close()

    source.observe(select, names='value'); build.on_click(compute); select()
    return dict(widget=widgets.VBox([status, build, output, preview]), build=build, status=status,
                source=source, state=state, compute=compute, close=close)
