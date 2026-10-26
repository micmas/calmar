from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from calmar.guided import source_cell
from calmar.participant_report import ParticipantReportResult


def _namespace(tmp_path, report, message, **extra):
    return dict(INTERP_RUN_DECODING=True, _CALMAR_SETUP_READY=True,
                PARTICIPANT_REPORT=report, SUBJECTS=[dict(subject='sub-fixture', session=None)],
                INTERP_SUBJECT_IDX=0, INTERP_MASK_SOURCE='manual',
                PROJECT_DIR=tmp_path, RAW_DATASET_DIR=tmp_path/'data', APHASIA_KB_ROOT=tmp_path/'stroke-aphasia-kb',
                _report_inputs=SimpleNamespace(message=message), **extra)


@pytest.mark.parametrize('success', [True, False])
def test_setup_flag_allows_decode_and_result_status_is_truthful(tmp_path, success):
    mask = tmp_path/'mask.nii.gz'
    mask.write_bytes(b'\x1f\x8bfixture')
    result = dict(lesion_voxels=4, region_overlap=pd.DataFrame(),
                  term_decoding=pd.DataFrame([dict(term='language', r=.03, impairment='')]),
                  neurosynth_available=success, warnings=[] if success else ['Offline fixture'])
    panel = SimpleNamespace(decode_log=nullcontext(), add_decoding=Mock(), lesion=mask)
    report = ParticipantReportResult(dict(subject='sub-fixture', session=None), 'manual', tmp_path/'r.html', panel)
    message = SimpleNamespace(value='')
    ns = _namespace(tmp_path, report, message)
    with patch('calmar.reporting.run_reporting_task', return_value=result) as submit:
        exec(''.join(source_cell(85)['source']), ns)
    # Decoding runs in Slurm (via run_reporting_task), never in the kernel.
    submit.assert_called_once_with({'PROJECT_DIR': tmp_path}, 'decode', mask=str(mask),
                                   kb_root=str(tmp_path/'stroke-aphasia-kb'), dataset=str(tmp_path/'data'))
    html = panel.add_decoding.call_args.args[0]
    assert 'Neurosynth' in html
    assert ('incomplete' in message.value) is (not success)
    if success:
        assert '1 terms tested' in html
    else:
        assert 'Offline fixture' in html


def test_decoding_refuses_a_report_for_a_different_selection(tmp_path):
    panel = SimpleNamespace(decode_log=nullcontext(), add_decoding=Mock(), lesion=tmp_path/'mask.nii.gz')
    report = ParticipantReportResult(dict(subject='sub-fixture', session=None), 'linda', tmp_path/'r.html', panel)
    ns = _namespace(tmp_path, report, SimpleNamespace(value=''))
    with patch('calmar.reporting.run_reporting_task') as submit, \
            pytest.raises(RuntimeError, match='Report inputs changed'):
        exec(''.join(source_cell(85)['source']), ns)
    submit.assert_not_called()


def test_decoding_without_a_report_explains_the_order(tmp_path):
    ns = _namespace(tmp_path, None, SimpleNamespace(value=''))
    with pytest.raises(RuntimeError, match='Generate the participant report'):
        exec(''.join(source_cell(85)['source']), ns)
