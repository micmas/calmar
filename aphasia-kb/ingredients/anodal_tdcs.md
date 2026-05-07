---
schema_version: 2.3
id: anodal_tdcs
name: Anodal tDCS (Left Temporoparietal)
kind: ingredient
status: approved
created_by: agent:claude-sonnet-4-6
created_on: 2026-05-07

rtss_category: technology

rtss:
  target: >-
    Cortical excitability of perilesional left temporoparietal cortex; LTP-like synaptic plasticity augmentation.
  ingredient: >-
    1 mA anodal direct current applied via sponge electrode to the intact
    left temporoparietal region for the first 20 minutes of each
    behavioural therapy session (15 sessions over 3 weeks, 5 days/week).
    Active behavioural treatment is delivered concurrently.
  theory: >-
    Anodal tDCS depolarises resting membrane potential of cortical neurons
    under the anode, increasing firing probability. When applied during
    concurrent language therapy, it is hypothesised to augment LTP-like
    synaptic changes triggered by behavioural practice. Fridriksson et
    al. 2018 (BDNF paper) found tDCS + therapy improved naming more than
    sham + therapy, and the benefit was moderated by BDNF Val66Met
    genotype.

used_in_therapies:
  - tdcs_aphasia_treatment

targets_impairments:
  - anomic_aphasia
  - brocas_aphasia
  - fluency
  - phonological_production

short_description: >-
  Anodal tDCS to left temporoparietal cortex applied during concurrent
  behavioural therapy to boost cortical excitability and augment LTP-
  like plasticity; efficacy moderated by BDNF Val66Met genotype.

notes: |
  tDCS is an adjunct to behavioural therapy, not a standalone treatment. Optimal electrode placement and current parameters remain under investigation. BDNF genotype is a significant moderator of response (see bdnf_val66met predictor entry).

---

# Anodal tDCS (Left Temporoparietal)

## RTSS specification

**Target**: Cortical excitability of perilesional left temporoparietal cortex; LTP-like synaptic plasticity augmentation.

**Ingredient**: 1 mA anodal direct current applied via sponge electrode to the intact left temporoparietal region for the first 20 minutes of each behavioural therapy session (15 sessions over 3 weeks, 5 days/week). Active behavioural treatment is delivered concurrently.

**Theory**: Anodal tDCS depolarises resting membrane potential of cortical neurons under the anode, increasing firing probability. When applied during concurrent language therapy, it is hypothesised to augment LTP-like synaptic changes triggered by behavioural practice. Fridriksson et al. 2018 (BDNF paper) found tDCS + therapy improved naming more than sham + therapy, and the benefit was moderated by BDNF Val66Met genotype.

## Used in therapies

- tdcs_aphasia_treatment


## Addresses impairments

- anomic_aphasia
- brocas_aphasia
- fluency
- phonological_production


## Notes

tDCS is an adjunct to behavioural therapy, not a standalone treatment. Optimal electrode placement and current parameters remain under investigation. BDNF genotype is a significant moderator of response (see bdnf_val66met predictor entry).
