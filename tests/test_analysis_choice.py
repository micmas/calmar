from calmar.analysis_choice import (RERUN, RUN, SKIP, USE_PRIOR, action_buttons,
                                    action_dropdown, action_options, entry_with_action,
                                    set_action_options)
from calmar.study import ENTRY_CONFIG


def test_optional_analysis_actions_have_one_consistent_safe_presentation():
    apply, skip = action_buttons()
    assert (apply.description, apply.button_style, apply.layout.width) == (
        "Apply choices and continue", "primary", "230px")
    assert (skip.description, skip.button_style, skip.layout.width) == (
        "Skip all and continue", "warning", "190px")

    fresh, default = action_options()
    assert [value for _, value in fresh] == [RUN, SKIP]
    assert default == SKIP
    stale, default = action_options(prior_available=True)
    assert [value for _, value in stale] == [USE_PRIOR, RERUN, SKIP]
    assert default == SKIP
    current, default = action_options(prior_available=True, current_complete=True)
    assert [label for label, _ in current] == [
        "Use saved results", "Rerun from the start", "Do not analyse"]
    assert default == USE_PRIOR
    existing, default = action_options(outputs_exist=True)
    assert [value for _, value in existing] == [RERUN, SKIP]
    assert default == SKIP
    assert action_dropdown().layout.width == "360px"


def test_changing_from_current_to_stale_resets_instead_of_silently_reusing_prior():
    action = action_dropdown(prior_available=True, current_complete=True, outputs_exist=True)
    assert action.value == USE_PRIOR
    set_action_options(
        action, prior_available=True, current_complete=False, outputs_exist=True)
    assert action.value == SKIP


def test_run_reuse_and_rerun_flags_are_scoped_to_one_entry():
    original = {"subject": "sub-one", ENTRY_CONFIG: {"COHORT_SETTING": 3}}
    prior = entry_with_action(
        original, USE_PRIOR, overwrite_key="DMRI_OVERWRITE", reuse_key="DMRI_REUSE_PRIOR")
    rerun = entry_with_action(
        original, RERUN, overwrite_key="DMRI_OVERWRITE", reuse_key="DMRI_REUSE_PRIOR")
    configured = entry_with_action(
        original, RUN, overwrite_key="DMRI_OVERWRITE", reuse_key="DMRI_REUSE_PRIOR")
    assert original[ENTRY_CONFIG] == {"COHORT_SETTING": 3}
    assert configured[ENTRY_CONFIG] == {"COHORT_SETTING": 3}
    assert prior[ENTRY_CONFIG] == {
        "COHORT_SETTING": 3, "DMRI_OVERWRITE": False, "DMRI_REUSE_PRIOR": True}
    assert rerun[ENTRY_CONFIG] == {
        "COHORT_SETTING": 3, "DMRI_OVERWRITE": True, "DMRI_REUSE_PRIOR": False}
    preconfigured = {"subject": "sub-two", ENTRY_CONFIG: {"DMRI_OVERWRITE": True}}
    assert entry_with_action(
        preconfigured, RUN, overwrite_key="DMRI_OVERWRITE",
        reuse_key="DMRI_REUSE_PRIOR")[ENTRY_CONFIG]["DMRI_OVERWRITE"] is True
