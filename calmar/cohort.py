"""Select participants from discovered T1 images, independently of mask sessions."""

import random


def sample_t1_participants(entries, limit, *, seed=42):
    """Sample distinct participants and one available T1 session/run per person.

    Manual-mask sessions do not constrain T1 eligibility. The existing mask
    discovery/registration steps find the annotation's own source scan later.
    Sorting inputs makes a saved seed repeatable across filesystem orderings.
    """
    by_subject = {}
    for entry in sorted(entries, key=lambda e: (e["subject"], e.get("session") or "", str(e["t1w"]))):
        by_subject.setdefault(entry["subject"], []).append(entry)
    rng = random.Random(seed)
    subjects = sorted(by_subject)
    if limit is not None and limit > 0 and limit < len(subjects):
        subjects = rng.sample(subjects, limit)
    selected = [rng.choice(by_subject[subject]) for subject in subjects]
    return sorted(selected, key=lambda e: (e["subject"], e.get("session") or ""))
