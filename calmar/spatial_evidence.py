"""Experimental spatial evidence appendix for CALMaR; no automatic clinical conclusions."""
from __future__ import annotations
import argparse
import hashlib
from html import escape
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import nibabel as nib
import numpy as np
from .kb_paths import load_kb_modules

DEFAULT_KB = Path(__file__).resolve().parents[1] / 'stroke-aphasia-kb'


def interpretation_context(record):
    """Keep anatomical correspondence separate from measurement compatibility."""
    tissue = record.get('tissue_class', 'unspecified')
    method = record.get('measurement_kind', 'unspecified')
    if tissue not in ('grey_matter', 'white_matter', 'mixed', 'unspecified'):
        raise ValueError('Unknown evidence tissue_class')
    if method not in ('direct_lesion_overlap', 'normative_disconnection',
                      'participant_diffusion', 'unspecified'):
        raise ValueError('Unknown evidence measurement_kind')
    return dict(tissue_class=tissue, measurement_kind=method,
                patient_measurement='direct_lesion_overlap',
                comparison_status=('same_measurement_family_requires_review'
                                   if method == 'direct_lesion_overlap' else
                                   'not_established'),
                clinical_inference_permitted=False)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def lesion_measurements(mask, affine, space, atlas):
    """Direct mask intersections; never infer child damage from parent percentages."""
    mask=np.asarray(mask)
    if mask.shape != atlas.data.shape or not np.allclose(affine,atlas.affine,atol=1e-6,rtol=0):
        raise ValueError('Lesion and atlas grids differ; explicit verified registration/alignment is required')
    if space != atlas.metadata['space']:
        raise ValueError('Lesion and atlas template spaces differ')
    if not np.isfinite(mask).all() or not np.isin(mask,[0,1]).all():
        raise ValueError('A binary lesion mask is required; no implicit thresholding')
    selected=mask.astype(bool);total=int(selected.sum())
    if not total:raise ValueError('Empty lesion mask')
    volume=float(abs(np.linalg.det(atlas.affine[:3,:3])))
    rows=[]
    for value in np.unique(atlas.data):
        if value==0:continue
        roi=atlas.data==value;n=int(roi.sum());overlap=int(np.count_nonzero(selected & roi))
        rows.append(dict(roi_id=int(value),label=atlas.labels[value],overlap_voxels=overlap,
                         overlap_mm3=overlap*volume,roi_damage_fraction=overlap/n,
                         lesion_fraction=overlap/total))
    outside=int(np.count_nonzero(selected & (atlas.data==0)))
    return dict(atlas=atlas.identity(),lesion_voxels=total,lesion_mm3=total*volume,
                outside_labelled_atlas_fraction=outside/total,regions=rows,
                method='Direct binary-mask intersections on the matching grid; registration QC is external',
                measurement_kind='direct_lesion_overlap')


def load_lesion(path):
    path=Path(path);spec=json.loads(path.read_text())
    for key in ('space','world_axes','provenance','qc_status'):
        if not spec.get(key):raise ValueError(f'Lesion manifest requires {key}')
    if spec['world_axes']!='RAS+':raise ValueError('Lesion world axes must be explicitly RAS+')
    image_path=path.parent/spec['image'];image=nib.load(image_path)
    q,qc=image.get_qform(coded=True);s,sc=image.get_sform(coded=True)
    if image.header.get_xyzt_units()[0]!='mm' or not (qc or sc):
        raise ValueError('Lesion requires millimetres and a coded spatial transform')
    if qc and sc and not np.allclose(q,s,atol=1e-4,rtol=0):
        raise ValueError('Lesion qform/sform conflict')
    spec={**spec,'manifest_sha256':digest(path),'image_sha256':digest(image_path)}
    return np.asanyarray(image.dataobj),image.affine,spec


def build(source, target, records, lesion=None, kb_root=DEFAULT_KB):
    engine,=load_kb_modules(kb_root,'spatial_harmonisation')
    a,b=engine.load_atlas(source),engine.load_atlas(target)
    mapping=engine.crosswalk(a,b)
    findings=engine.map_evidence(json.loads(Path(records).read_text()),mapping)
    for finding in findings['findings']:
        finding['interpretation_context'] = interpretation_context(finding['original'])
    try:
        commit=subprocess.check_output(['git','-C',str(kb_root),'rev-parse','HEAD'],text=True).strip()
    except (OSError,subprocess.CalledProcessError):commit=None
    result=dict(status='experimental_requires_spatial_and_source_review',approved=False,
                kb_commit=commit,adapter_sha256=digest(__file__),records_sha256=digest(records),
                crosswalk=mapping,evidence=findings,lesion=None,
                runtime={'numpy':np.__version__,'nibabel':nib.__version__},
                warning='Atlas correspondence does not establish patient symptoms, outcome probability or equivalence of study methods.')
    if lesion:
        mask,affine,spec=load_lesion(lesion)
        result['lesion']={'provenance':spec,'source_atlas':lesion_measurements(mask,affine,spec['space'],a),
                          'target_atlas':lesion_measurements(mask,affine,spec['space'],b)}
    return result


def render_appendix(data):
    """Escaped, report-ready HTML kept separate from the clinical interpretation."""
    e=lambda v:escape(str(v))
    html=['<section class="spatial-evidence experimental"><h2>Experimental spatial evidence appendix</h2>',
          '<p>Not approved for clinical interpretation. Spatial correspondence is not functional equivalence.</p>',
          '<p>'+e(data['warning'])+'</p>',
          '<p>White matter: lesion overlap with a labelled tract region is not a measurement of whole-tract disconnection or participant diffusion. These evidence types remain separate. Probabilistic and overlapping tract maps are not supported by this deterministic-label pilot.</p>',
          '<h3>Atlas correspondence</h3><table><thead><tr><th>Study-atlas ROI</th><th>Report-atlas ROI</th><th>Share of study ROI</th><th>Share of report ROI</th></tr></thead><tbody>']
    for edge in data['crosswalk']['edges']:
        html.append(f"<tr><td>{e(edge['source_label'])}</td><td>{e(edge['target_label'])}</td><td>{100*edge['source_fraction']:.2f}%</td><td>{100*edge['target_fraction']:.2f}%</td></tr>")
    html.append('</tbody></table><p>Unmapped study-atlas tissue:</p><ul>')
    for row in data['crosswalk']['source_coverage']:
        html.append(f"<li>{e(row['label'])}: {100*row['unmapped_fraction']:.2f}%</li>")
    html.append('</ul><h3>Original findings</h3><p>Each original finding appears once. Mapped parcels are not independent evidence.</p><ul>')
    for finding in data['evidence']['findings']:
        context = finding['interpretation_context']
        html.append('<li>Evidence context: '+e(context['tissue_class'])+'; '+e(context['measurement_kind'])+'. Measurement comparison: '+e(context['comparison_status'])+'.</li>')
        r=finding['original'];html.append(f"<li>{e(r['evidence_id'])} — {e(r['citation'])}, {e(r['source_location'])}: {e(finding['status'])}; {len(finding['spatial_candidates'])} spatial candidates. {e(finding.get('reason',''))} Cohort: {e(finding['cohort_check'])}<details><summary>Original evidence record</summary><pre>{e(json.dumps(r,indent=2))}</pre></details></li>")
    html.append('</ul>')
    if data.get('lesion'):
        html.append('<h3>Direct lesion measurements</h3><p>QC status supplied by the processing workflow: '+e(data['lesion']['provenance']['qc_status'])+'. This tool has not visually verified registration.</p>')
        for side in ('source_atlas','target_atlas'):
            measured=data['lesion'][side]
            html.append('<h4>'+e(measured['atlas']['atlas_id'])+'</h4><table><tr><th>ROI</th><th>ROI damaged</th><th>Share of lesion</th></tr>')
            for row in measured['regions']:
                if row['overlap_voxels']:
                    html.append(f"<tr><td>{e(row['label'])}</td><td>{100*row['roi_damage_fraction']:.2f}%</td><td>{100*row['lesion_fraction']:.2f}%</td></tr>")
            html.append(f"</table><p>Lesion outside labelled atlas: {100*measured['outside_labelled_atlas_fraction']:.2f}%.</p>")
    html.append('<p>KB revision: '+e(data.get('kb_commit'))+'</p></section>')
    return '\n'.join(html)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','target','records','output-dir'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--lesion',type=Path,help='Manifest for an already processed, aligned binary lesion mask')
    p.add_argument('--kb-root',type=Path,default=DEFAULT_KB)
    a=p.parse_args()
    if a.output_dir.exists():p.error('Output directory exists; preserve it and choose a new destination')
    data=build(a.source,a.target,a.records,a.lesion,a.kb_root)
    a.output_dir.parent.mkdir(parents=True,exist_ok=True)
    temporary=Path(tempfile.mkdtemp(prefix=a.output_dir.name+'.attempt-',dir=a.output_dir.parent))
    try:
        (temporary/'spatial-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
        (temporary/'spatial-evidence.html').write_text('<!doctype html><meta charset="utf-8"><title>Spatial evidence appendix</title>'+render_appendix(data))
        if a.output_dir.exists():raise FileExistsError(a.output_dir)
        temporary.rename(a.output_dir)
    finally:
        if temporary.exists():shutil.rmtree(temporary)
    print(f'Experimental appendix saved to {a.output_dir}; no clinical report or KB approval changed.')


if __name__=='__main__':main()
