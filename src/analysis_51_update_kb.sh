#!/bin/bash
#SBATCH --job-name=calmar_update_kb
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=00:10:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1

set -euo pipefail

# Git is installed in the main Neurodesk environment and does not require a
# module. Pin both the repository revision and the generated export identity so
# a moving origin/main cannot silently change the KB used by CALMAR.
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
EXPECTED_COMMIT="5ad3d7425318e24ba225422456782d0db154830c"
EXPECTED_CONTENT_COMMIT="cc92791"
EXPECTED_CONTENT_DATE="2026-10-31"
EXPECTED_DIGEST="4959b3b0c6e2146b"
REFERENCE_EXPORTED_ON="2026-11-01"
export GIT_TERMINAL_PROMPT=0

# Match calmar.kb_location.resolve_kb_root: explicit override, then sibling,
# then the CALMAR submodule.
if [[ -n "${CALMAR_KB_ROOT:-}" ]]; then
    KB_DIR="$(realpath "${CALMAR_KB_ROOT}")"
    KB_REASON="CALMAR_KB_ROOT override"
elif [[ -f "${PROJECT_DIR}/../stroke-aphasia-kb/scripts/aphasia_kb.py" && \
        -d "${PROJECT_DIR}/../stroke-aphasia-kb/regions" ]]; then
    KB_DIR="$(realpath "${PROJECT_DIR}/../stroke-aphasia-kb")"
    KB_REASON="sibling working copy"
else
    KB_DIR="$(realpath "${PROJECT_DIR}/stroke-aphasia-kb")"
    KB_REASON="CALMAR submodule"
fi

if [[ ! -d "${KB_DIR}/.git" && ! -f "${KB_DIR}/.git" ]]; then
    echo "ERROR: missing knowledge-base checkout: ${KB_DIR}" >&2
    exit 1
fi

if ! KB_STATUS="$(git -C "${KB_DIR}" status --porcelain --untracked-files=all)"; then
    echo "ERROR: could not inspect the knowledge-base checkout: ${KB_DIR}" >&2
    exit 1
fi
if [[ -n "${KB_STATUS}" ]]; then
    echo "ERROR: refusing to update a knowledge-base checkout with local changes" >&2
    printf '%s\n' "${KB_STATUS}" >&2
    exit 1
fi

PREVIOUS_COMMIT="$(git -C "${KB_DIR}" rev-parse HEAD)"
echo "Selected KB: ${KB_DIR} (${KB_REASON})"
echo "Previous KB commit: ${PREVIOUS_COMMIT}"

git -C "${KB_DIR}" fetch --no-tags origin \
    "+refs/heads/main:refs/remotes/origin/main"
if ! git -C "${KB_DIR}" cat-file -e "${EXPECTED_COMMIT}^{commit}"; then
    echo "ERROR: expected commit is not available from origin/main: ${EXPECTED_COMMIT}" >&2
    exit 1
fi
if ! git -C "${KB_DIR}" merge-base --is-ancestor \
    "${EXPECTED_COMMIT}" refs/remotes/origin/main; then
    echo "ERROR: expected commit is not contained in origin/main: ${EXPECTED_COMMIT}" >&2
    exit 1
fi
if ! git -C "${KB_DIR}" merge-base --is-ancestor \
    "${PREVIOUS_COMMIT}" "${EXPECTED_COMMIT}"; then
    # A maintainer may have rewritten origin/main. Moving away from the old
    # history is safe only when the current HEAD is recorded in origin/main's
    # reflog, proving it was previously fetched rather than created locally.
    REMOTE_REFLOG="$(git -C "${KB_DIR}" reflog show --format='%H' refs/remotes/origin/main)"
    if grep -Fxq "${PREVIOUS_COMMIT}" <<<"${REMOTE_REFLOG}"; then
        echo "Previous HEAD was a formerly fetched origin/main revision; accepting remote history rewrite."
    else
        echo "ERROR: current KB HEAD has commits not contained in the requested revision" >&2
        echo "Current: ${PREVIOUS_COMMIT}" >&2
        echo "Requested: ${EXPECTED_COMMIT}" >&2
        exit 1
    fi
fi

# Generate and verify the approved export from an isolated worktree. The live
# checkout is moved only after the candidate revision passes every check.
VERIFY_PARENT="$(mktemp -d "${PROJECT_DIR}/.kb-verify.XXXXXX")"
VERIFY_DIR="${VERIFY_PARENT}/worktree"
cleanup() {
    git -C "${KB_DIR}" worktree remove --force "${VERIFY_DIR}" >/dev/null 2>&1 || true
    rmdir "${VERIFY_PARENT}" >/dev/null 2>&1 || true
}
trap cleanup EXIT
git -C "${KB_DIR}" worktree add --quiet --detach "${VERIFY_DIR}" "${EXPECTED_COMMIT}"
VERIFY_COMMIT="$(git -C "${VERIFY_DIR}" rev-parse HEAD)"
if [[ "${VERIFY_COMMIT}" != "${EXPECTED_COMMIT}" ]]; then
    echo "ERROR: verification worktree is ${VERIFY_COMMIT}, expected ${EXPECTED_COMMIT}" >&2
    exit 1
fi
python -I "${VERIFY_DIR}/scripts/export_webapp.py" \
    --root "${VERIFY_DIR}" --include approved \
    --out "${VERIFY_DIR}/verified-stroke-aphasia-kb.json"

python -I - "${VERIFY_DIR}/verified-stroke-aphasia-kb.json" \
    "${EXPECTED_COMMIT}" "${EXPECTED_CONTENT_COMMIT}" \
    "${EXPECTED_CONTENT_DATE}" "${EXPECTED_DIGEST}" "${REFERENCE_EXPORTED_ON}" <<'PY'
import json
import sys
from pathlib import Path

export_path = Path(sys.argv[1])
expected = {
    "commit": sys.argv[3],
    "date": sys.argv[4],
    "contentDigest": sys.argv[5],
    "statuses": ["approved"],
}
reference_exported_on = sys.argv[6]
data = json.loads(export_path.read_text(encoding="utf-8"))
version = data.get("version", {})
errors = [
    f"version.{key}: found {version.get(key)!r}, expected {value!r}"
    for key, value in expected.items()
    if version.get(key) != value
]

screening = data.get("screening", {})
prisma = screening.get("prisma", {})
counts = {
    "candidates": len(screening.get("candidates", [])),
    "searches": len(screening.get("searches", [])),
    "included": prisma.get("included", {}).get("total"),
    "in_knowledge_base": prisma.get("included", {}).get("kb", {}).get("in_kb"),
}
expected_counts = {
    "candidates": 159,
    "searches": 24,
    "included": 121,
    "in_knowledge_base": 41,
}
errors.extend(
    f"{key}: found {counts[key]!r}, expected {value!r}"
    for key, value in expected_counts.items()
    if counts[key] != value
)

if errors:
    raise SystemExit("ERROR: KB export verification failed:\n  " + "\n  ".join(errors))

print(f"Verified KB checkout: {sys.argv[2]}")
print(
    "Verified approved export: "
    f"content commit {version['commit']} · digest {version['contentDigest']} · "
    f"exported {version['exportedOn']} · "
    f"{counts['candidates']} candidates · {counts['searches']} searches · "
    f"{counts['included']} included · {counts['in_knowledge_base']} in the knowledge base"
)
print(
    f"Reference export date: {reference_exported_on}; regenerated export date: "
    f"{version['exportedOn']} (the content identity is pinned by commit and digest)."
)
PY

git -C "${KB_DIR}" checkout --quiet --detach "${EXPECTED_COMMIT}"
ACTUAL_COMMIT="$(git -C "${KB_DIR}" rev-parse HEAD)"
if [[ "${ACTUAL_COMMIT}" != "${EXPECTED_COMMIT}" ]]; then
    echo "ERROR: checkout is ${ACTUAL_COMMIT}, expected ${EXPECTED_COMMIT}" >&2
    exit 1
fi

echo "Pinned selected KB checkout to ${ACTUAL_COMMIT}."
if [[ "${KB_REASON}" == "CALMAR submodule" ]]; then
    echo "NOTE: the CALMAR submodule pointer now differs from the committed release pin."
fi
echo "NOTE: launch CALMAR with CALMAR_KB_UPDATE=off to keep this exact revision pinned."
