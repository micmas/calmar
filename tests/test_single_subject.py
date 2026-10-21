import re
from types import SimpleNamespace
from unittest.mock import Mock

from calmar.single_subject import SingleSubjectInputs
from calmar.overlay import agreement_table


def fixture_namespace(root):
    entries = [dict(subject=f'sub-{i}',session='ses-1') for i in range(3)]
    return dict(SUBJECTS=entries,CONFIG={'TEST_SUBJECT_IDX':0},
        deriv_path_for=lambda e:root/e['subject']/'linda',
        synthstroke_path_for=lambda e:root/e['subject']/'synth',
        hdbet_path_for=lambda e:root/e['subject']/'hdbet')


def test_default_prefers_unprocessed_and_updates_all_single_subject_consumers(tmp_path):
    ns = fixture_namespace(tmp_path)
    first = ns['SUBJECTS'][0]
    linda = ns['deriv_path_for'](first); linda.mkdir(parents=True)
    synth = ns['synthstroke_path_for'](first); synth.mkdir(parents=True)
    (linda/'Lesion_in_MNI.nii.gz').write_bytes(b'existing')
    (synth/'prediction_lesion_mask.nii.gz').write_bytes(b'existing')
    panel = SingleSubjectInputs(ns)
    try:
        assert panel.subject.value == 1
        assert ns['TEST_SUBJECT_IDX'] == ns['CONFIG']['TEST_SUBJECT_IDX'] == 1
        assert 'Not processed' in panel.subject.label
        panel.subject.value = 2
        assert ns['_CALMAR_TEST_SELECTION'] == ('sub-2','ses-1')
        assert ns['TEST_SUBJECT_IDX'] == ns['CONFIG']['TEST_SUBJECT_IDX'] == 2
        assert ns['DIAG_SUBJECT_IDX'] is ns['CMP_SUBJECT_IDX'] is None
    finally:panel.close()
    # A rerun keeps the deliberate selection rather than moving to another case.
    again = SingleSubjectInputs(ns)
    try:assert again.subject.value == 2
    finally:again.close()


def test_choosing_does_not_start_processing_or_release_the_gate(tmp_path):
    ns=fixture_namespace(tmp_path)
    shell=SimpleNamespace(input_transformers_post=[],kernel=SimpleNamespace(_abort_queues=Mock()))
    panel=SingleSubjectInputs(ns,shell)
    try:
        panel.subject.value=2
        assert panel.gate.paused
        assert len(shell.input_transformers_post)==1
        panel.navigation.request=Mock()
        panel.start.click()
        role, callback=panel.navigation.request.call_args.args
        assert role=='single-test-start'
        assert panel.gate.paused
        callback()
        assert not panel.gate.paused and ns['TEST_SUBJECT_IDX']==2
    finally:panel.close()


def test_agreement_tools_are_columns_and_missing_tool_stays_visible():
    html=agreement_table({'LINDA':dict(dice=.8,iou=.67,sens=.75,prec=.9,n=90,overlap=75),
                          'SynthStroke':None},100)
    plain=lambda value: re.sub('<[^>]+>','',value)
    headers=[plain(h) for h in re.findall(r'<th>(.*?)</th>',html)]
    assert headers==['Metric','■ LINDA (red)','■ SynthStroke (green)']
    dice=re.findall(r'<tr>(.*?)</tr>',html)[1]
    assert [plain(c) for c in re.findall(r'<td[^>]*>(.*?)</td>',dice)]==['Dice','0.800','—']
    assert 'Not yet run' in html


def test_segmentation_tick_boxes_set_the_config_for_test_and_batch(tmp_path):
    ns = fixture_namespace(tmp_path)
    shell = SimpleNamespace(input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=Mock()))
    panel = SingleSubjectInputs(ns, shell)
    try:
        boxes = panel.methods.boxes
        assert boxes['linda'].value and boxes['synthstroke'].value       # default: both
        boxes['linda'].value = False
        assert ns['CONFIG']['SEGMENTATION_METHODS'] == ['synthstroke']
        assert 'registration step' in panel.methods.note.value
        boxes['synthstroke'].value = False                                 # none ticked: cannot start
        assert panel.start.disabled and ns['CONFIG']['SEGMENTATION_METHODS'] == ['synthstroke']
        assert panel.approve() is False and panel.gate.paused
        boxes['linda'].value = True
        assert not panel.start.disabled and ns['CONFIG']['SEGMENTATION_METHODS'] == ['linda']
        assert panel.approve() is True and boxes['linda'].disabled        # fixed once processing starts
    finally:
        panel.close()


def test_batch_checkpoint_offers_the_same_choice():
    from calmar import execution as ex
    config = {'SEGMENTATION_METHODS': ['linda', 'synthstroke']}
    shell = SimpleNamespace(input_transformers_post=[], user_ns={'CONFIG': config},
                            kernel=SimpleNamespace(_abort_queues=Mock(), get_parent=lambda: {}))
    gate = ex.BatchCheckpoint(shell)
    try:
        gate.methods.boxes['linda'].value = False
        assert config['SEGMENTATION_METHODS'] == ['synthstroke']
        gate._resume()
        assert not gate.paused and 'SynthStroke' in gate.message.value
    finally:
        gate.close()
