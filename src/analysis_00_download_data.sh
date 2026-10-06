#!/bin/bash
#SBATCH --job-name=isles2022_download
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --time=01:00:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=2

# Acquisition record for the ISLES 2022 dataset (Zenodo record 7153326).
# The dataset was originally materialized by lesion-segmentation-benchmark.ipynb
# (section 4); this script preserves the same acquisition so it is reproducible
# without the notebook. Idempotent: skips if the dataset is already extracted.
# Data-only: no neuroimaging module needed (curl/unzip are in the base env).

set -euo pipefail

PROJECT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
cd "${PROJECT_DIR}"

URL="https://zenodo.org/records/7153326/files/ISLES-2022.zip?download=1"
MD5="302ee280373cdd5c190ab763d72a7a50"
DEST="data/ISLES-2022"

if [ -d "${DEST}" ] && [ "$(find "${DEST}" -maxdepth 1 -name 'sub-*' | wc -l)" -ge 250 ]; then
    echo "ISLES-2022 already extracted (${DEST}) — nothing to do."
    exit 0
fi

mkdir -p data
TMP_ZIP="data/.ISLES-2022.zip.part"
curl -L --fail -o "${TMP_ZIP}" "${URL}"
echo "${MD5}  ${TMP_ZIP}" | md5sum -c -

TMP_DIR="data/.ISLES-2022.extract.$$"
mkdir -p "${TMP_DIR}"
unzip -q "${TMP_ZIP}" -d "${TMP_DIR}"

# The zip contains a single ISLES-2022/ root — publish it atomically.
mv "${TMP_DIR}/ISLES-2022" "${DEST}"
rm -rf "${TMP_DIR}" "${TMP_ZIP}"
echo "ISLES-2022 extracted → ${DEST}"
