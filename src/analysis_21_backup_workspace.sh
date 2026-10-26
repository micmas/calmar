#!/bin/bash
#SBATCH --job-name=calmar_backup
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1
set -euo pipefail
PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "$PROJECT_DIR"
FINAL="${1:?usage: $0 <backup-directory>}"
test ! -e "$FINAL"
mkdir -p "$(dirname "$FINAL")"
TMP="$(mktemp -d "${FINAL}.attempt.XXXXXX")"
trap 'rm -rf "$TMP"' EXIT
# Independent copies preserve QC, annex objects and historical artifacts.
for item in data reports atlases qc_edits notes logs alignment-repair workflow-validation stroke-aphasia-kb/_neurosynth_cache; do
    if [[ -e "$item" ]]; then
        mkdir -p "$TMP/$(dirname "$item")"
        cp -a --reflink=auto "$item" "$TMP/$item"
    fi
done
git bundle create "$TMP/source.bundle" --all
git diff --no-textconv --binary > "$TMP/worktree.patch"
find "$TMP" -type f -printf '%P\t%s\n' > "$TMP/files.tsv"
neurodesk-astra-provenance publish "$TMP" "$FINAL" --output-id workspace_backup --tool python --script "$0"
