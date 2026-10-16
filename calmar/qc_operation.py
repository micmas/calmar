"""Execute explicit QC processing on staged copies, retaining previous results."""
from contextlib import ExitStack
import inspect
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from . import qc
from .processing import publish, validate_image
from .scheduled import decode, encode

OUTPUTS = {
    'run_hd_bet': ['out_dir'],
    'run_linda_with_mask': ['linda_out_dir'],
    'run_linda_with_mask_via_R': ['linda_out_dir'],
    'hdbet_then_linda': ['linda_out_dir','work_dir'],
    'restrip_and_rerun': ['linda_out_dir','work_dir'],
    'rerun_subject': ['linda_out_dir'],
    'warp_native_mask_to_mni': ['out_path'],
    'warp_native_lesion_to_mni': ['linda_out_dir'],
    'coregister_t2_mask_to_t1': ['out_mask_path','t2_out_path'],
}
FILES = {'out_path','out_mask_path','t2_out_path'}


def execute(request):
    if not os.environ.get('SLURM_JOB_ID'): raise RuntimeError('Submit the retained Slurm script.')
    name=request['function']
    if name not in OUTPUTS: raise ValueError(f'Unsupported QC operation: {name}')
    function=getattr(qc,name)
    bound=inspect.signature(function).bind(*decode(request['args']),**decode(request['kwargs']))
    bound.apply_defaults()
    # These helpers otherwise derive a sibling work directory *after* staging,
    # which would escape the set of outputs we validate and publish.
    if name in ('hdbet_then_linda', 'restrip_and_rerun') and bound.arguments.get('work_dir') is None:
        bound.arguments['work_dir'] = Path(bound.arguments['linda_out_dir']).absolute().parent/'_hdbet_work'
    directories=[]
    for parameter in OUTPUTS[name]:
        value=bound.arguments.get(parameter)
        if value is None: continue
        path=Path(value).absolute()
        path=path.parent if parameter in FILES else path
        if path==Path.cwd() or path==Path('/'):
            raise ValueError('Choose a dedicated derivative directory for QC output.')
        directories.append(path)
    directories=sorted(set(directories),key=lambda p:len(p.parts))
    directories=[p for i,p in enumerate(directories) if not any(p.is_relative_to(parent) for parent in directories[:i])]
    with ExitStack() as stack:
        mappings=[]
        for final in directories:
            final.parent.mkdir(parents=True,exist_ok=True)
            folder=Path(stack.enter_context(tempfile.TemporaryDirectory(prefix=final.name+'.attempt.',dir=final.parent)))
            tmp=folder/final.name
            # Dereference links: a repair must never write through a staged
            # symlink into an original derivative or a DataLad annex object.
            if final.exists(): shutil.copytree(final,tmp,symlinks=False)
            else: tmp.mkdir()
            mappings.append((final,tmp))
        def relocate(value,reverse=False):
            if isinstance(value,(str,Path)):
                path=Path(value)
                if path.is_absolute():
                    for final,tmp in mappings:
                        source,target=(tmp,final) if reverse else (final,tmp)
                        if path.is_relative_to(source):
                            result=target/path.relative_to(source)
                            return result if isinstance(value,Path) else str(result)
                return value
            if isinstance(value,dict): return {k:relocate(v,reverse) for k,v in value.items()}
            if isinstance(value,(tuple,list)): return [relocate(v,reverse) for v in value]
            return value
        # Normalize file paths before remapping, including relative notebook arguments.
        path_parameters = set(OUTPUTS[name]) | {
            't1w_path', 't1_path', 't2_path', 'mask_path', 'brain_mask',
            'native_mask', 'native_lesion', 'linda_out_dir', 'manual_mask',
            'mask_path_or_img', 'manual_seed', 'work_dir', 'brain_mask_path',
        }
        for key,value in list(bound.arguments.items()):
            if isinstance(value,Path) or (key in path_parameters and isinstance(value,str)):
                normalized = Path(value).absolute()
                bound.arguments[key] = normalized if isinstance(value,Path) else str(normalized)
        for key,value in list(bound.arguments.items()): bound.arguments[key]=relocate(value)
        result=function(*bound.args,**bound.kwargs)
        codes=[result] if isinstance(result,int) else [v for k,v in result.items() if k.endswith('returncode')] if isinstance(result,dict) else []
        if any(code for code in codes): raise RuntimeError(f'{name} failed: {result}')
        for _,tmp in mappings:
            for image in tmp.rglob('*.nii.gz'): validate_image(image)
        backups=[]
        try:
            for final,tmp in mappings:
                backup=final.with_name(final.name+'.previous.'+os.environ['SLURM_JOB_ID'])
                if backup.exists(): raise FileExistsError(backup)
                existed=final.exists()
                if existed: os.replace(final,backup)
                sidecar=Path(str(final)+'.prov.json')
                old_sidecar=Path(str(backup)+'.prov.json')
                if sidecar.exists(): os.replace(sidecar,old_sidecar)
                backups.append((final,backup,existed,sidecar,old_sidecar))
                publish(tmp,final,'qc_operation')
        except Exception:
            for final,backup,existed,sidecar,old_sidecar in reversed(backups):
                if final.exists(): shutil.rmtree(final)
                sidecar.unlink(missing_ok=True)
                if existed: os.replace(backup,final)
                if old_sidecar.exists(): os.replace(old_sidecar,sidecar)
            raise
        return relocate(result,reverse=True)


def main():
    request_path,output=map(Path,sys.argv[1:])
    if output.exists(): raise FileExistsError(output)
    request=json.loads(request_path.read_text())
    value=execute(request)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=output.name+'.attempt.',dir=output.parent) as d:
        tmp=Path(d)/'receipt'; tmp.mkdir()
        (tmp/'summary.json').write_text(json.dumps({'request':request,'value':encode(value),'results':[],
            'job':os.environ['SLURM_JOB_ID'],'stage':'qc_operation'},indent=2))
        publish(tmp,output,'qc_operation')


if __name__=='__main__': main()
