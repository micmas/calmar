import re
from types import SimpleNamespace
from unittest.mock import Mock

from calmar.single_subject import (
    SingleSubjectInputs,
    mark_optional_completed,
    optional_entries_for_test,
    optional_run_signature,
    pending_optional_entries,
)
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


def test_skip_single_subject_test_starts_at_batch_and_updates_run_test(tmp_path):
    ns = fixture_namespace(tmp_path)
    ns['RUN_TEST'] = ns['CONFIG']['RUN_TEST'] = True
    stale = [Mock(), Mock(), Mock()]
    shell = SimpleNamespace(
        input_transformers_post=[], kernel=SimpleNamespace(_abort_queues=Mock()),
        _calmar_batch_checkpoint=stale[0], _calmar_qc_checkpoint=stale[1],
        _calmar_report_checkpoint=stale[2])
    panel = SingleSubjectInputs(ns, shell)
    try:
        panel.navigation.request = Mock()
        panel.skip.click()
        role, callback = panel.navigation.request.call_args.args
        assert role == 'batch-start'
        assert 'Skip the single-subject test' in panel.navigation.request.call_args.kwargs['prompt']
        assert panel.gate.paused and ns['RUN_TEST'] is True

        assert callback() is True
        assert not panel.gate.paused
        assert ns['RUN_TEST'] is False
        assert ns['CONFIG']['RUN_TEST'] is True
        for checkpoint in stale:
            checkpoint.close.assert_called_once_with()
        assert panel.start.disabled and panel.skip.disabled
        assert 'starting batch processing' in panel.message.value
    finally:
        panel.close()


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
        assert panel.start.disabled and panel.skip.disabled
        assert ns['CONFIG']['SEGMENTATION_METHODS'] == ['synthstroke']
        assert panel.approve() is False and panel.gate.paused
        ns['RUN_TEST'] = True
        assert panel.skip_test() is False and panel.gate.paused
        assert ns['RUN_TEST'] is True
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


def test_optional_entries_follow_the_selected_anatomical_session():
    test_entry = {"subject": "sub-one", "session": "ses-t1a"}
    entries = [
        {"subject": "sub-one", "session": "ses-dwi", "anatomical_session": "ses-t1a",
         "dwi": "/data/first_dwi.nii.gz"},
        {"subject": "sub-one", "session": "ses-t1b", "brain_health_components": ["atrophy"]},
        {"subject": "sub-two", "session": "ses-t1a", "brain_health_components": ["atrophy"]},
    ]

    assert optional_entries_for_test(entries, test_entry) == [entries[0]]


def test_optional_entry_can_link_a_named_dwi_session_to_sessionless_anatomy():
    test_entry = {"subject": "sub-one", "session": None}
    dwi_entry = {"subject": "sub-one", "session": "ses-dwi",
                 "anatomical_session": None, "dwi": "/data/dwi.nii.gz"}

    assert optional_entries_for_test([dwi_entry], test_entry) == [dwi_entry]


def test_completed_single_subject_entries_are_removed_from_optional_batch(tmp_path):
    first = {"subject": "sub-one", "session": "ses-dwi", "anatomical_session": "ses-t1",
             "t1w": tmp_path / "first_dwi.nii.gz", "dwi": tmp_path / "first_dwi.nii.gz"}
    second = {"subject": "sub-two", "session": "ses-dwi", "anatomical_session": "ses-t1",
              "t1w": tmp_path / "second_dwi.nii.gz", "dwi": tmp_path / "second_dwi.nii.gz"}
    first["dwi"].write_bytes(b"first")
    second["dwi"].write_bytes(b"second")
    output = tmp_path / "first_openads.nii.gz"
    output.write_bytes(b"mask")
    study = SimpleNamespace(config={"OVERWRITE": True}, dataset=tmp_path)
    result = {
        "stage": "openads",
        "request": {"entries": [first], "config": study.config, "dataset": str(tmp_path)},
        "results": [{"subject": "sub-one", "session": "ses-dwi",
                     "outputs": [{"path": str(output)}]}],
    }
    state = {}
    assert mark_optional_completed(state, "dwi", [first], study, [result])
    completed = state["dwi"]

    assert pending_optional_entries(
        [first, second], completed, route="dwi", study=study) == [second]

    study.config["OPENADS_SUBDIR"] = "changed"
    assert pending_optional_entries(
        [first], completed, route="dwi", study=study) == [first]


def test_changed_optional_output_invalidates_single_test_completion(tmp_path):
    dwi = tmp_path / "dwi.nii.gz"
    output = tmp_path / "openads.nii.gz"
    dwi.write_bytes(b"dwi")
    output.write_bytes(b"first mask")
    entry = {"subject": "sub-one", "session": None, "t1w": dwi, "dwi": dwi}
    study = SimpleNamespace(config={}, dataset=tmp_path)
    result = {
        "stage": "openads", "request": {"entries": [entry], "config": {},
                                           "dataset": str(tmp_path)},
        "results": [{"subject": "sub-one", "session": None,
                     "outputs": [{"path": str(output)}]}],
    }
    state = {}
    assert mark_optional_completed(state, "dwi", [entry], study, [result])
    assert pending_optional_entries(
        [entry], state["dwi"], route="dwi", study=study) == []

    output.write_bytes(b"replacement mask is different")
    assert pending_optional_entries(
        [entry], state["dwi"], route="dwi", study=study) == [entry]


def test_optional_signature_changes_when_selected_lesion_mask_changes(tmp_path):
    from calmar.study import Study

    t1w = tmp_path / "sub-one" / "ses-t1" / "anat" / "sub-one_ses-t1_T1w.nii.gz"
    t1w.parent.mkdir(parents=True)
    t1w.write_bytes(b"t1")
    entry = {"subject": "sub-one", "session": "ses-dmri", "anatomical_session": "ses-t1",
             "t1w": t1w, "anatomical_t1w": t1w, "dwi": tmp_path / "dwi.nii.gz"}
    entry["dwi"].write_bytes(b"dwi")
    config = {
        "MODALITY": "t1", "DMRI_MASK_SOURCE": "manual", "MANUAL_MASK_SPACE": "t1",
        "MANUAL_MASK_PATH": str(tmp_path / "{sub}_{ses}_mask.nii.gz"),
    }
    mask = tmp_path / "sub-one_ses-t1_mask.nii.gz"
    mask.write_bytes(b"old")
    study = Study(config, tmp_path, tmp_path)

    before = optional_run_signature("dmri", entry, study)
    mask.write_bytes(b"repaired lesion")
    assert optional_run_signature("dmri", entry, study) != before
