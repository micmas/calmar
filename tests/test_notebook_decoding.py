from contextlib import nullcontext
import importlib
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from calmar.guided import source_cell


@pytest.mark.parametrize('success', [True, False])
def test_setup_flag_allows_decode_and_result_status_is_truthful(tmp_path, success):
    mask = tmp_path/'mask.nii.gz'
    mask.write_bytes(b'\x1f\x8bfixture')  # Decoder is mocked; notebook only checks gzip magic.
    result = dict(lesion_voxels=4, region_overlap=pd.DataFrame(),
                  term_decoding=pd.DataFrame([dict(term='language', r=.03, impairment='')]),
                  neurosynth_available=success, warnings=[] if success else ['Offline fixture'])
    decoder = Mock(return_value=result)
    kb = SimpleNamespace(KnowledgeBase=Mock(return_value=SimpleNamespace(decode_lesion=decoder)))
    report = SimpleNamespace(decode_log=nullcontext(), add_decoding=Mock())
    message = SimpleNamespace(value='')
    ns = dict(INTERP_RUN_DECODING=True, _CALMAR_SETUP_READY=True,
              _participant_report_panel=report, SUBJECTS=[dict(subject='sub-fixture', session=None)],
              interp_resolve_idx=lambda: 0, INTERP_MASK_SOURCE='manual',
              _calmar_generated_report_selection=('sub-fixture', '', 'manual'),
              PROJECT_DIR=tmp_path, Path=Path, sys=sys, importlib=importlib,
              INTERP_MASK_LABELS={'manual':'Manual'}, interp_mni_mask_path=lambda e, s: mask,
              _report_inputs=SimpleNamespace(message=message))
    with patch.dict(sys.modules, {'aphasia_kb': kb}), patch.object(importlib, 'reload', lambda m:m):
        exec(''.join(source_cell(85)['source']), ns)
    decoder.assert_called_once_with(str(mask), verbose=True)
    html = report.add_decoding.call_args.args[0]
    assert 'Neurosynth' in html
    assert ('incomplete' in message.value) is (not success)
    if success:
        assert '1 terms tested' in html
    else:
        assert 'Offline fixture' in html
