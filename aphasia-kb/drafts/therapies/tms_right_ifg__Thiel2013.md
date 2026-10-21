---
schema_version: 2.3
id: tms_right_ifg
name: "Inhibitory rTMS to Right Inferior Frontal Gyrus"
kind: therapy
status: draft
created_by: "agent:ollama-extract-cli/gemma4:31b-it-q8_0"
created_on: 2026-10-21
short_description: "Low-frequency (1 Hz) inhibitory repetitive transcranial magnetic stimulation applied to the right posterior inferior frontal gyrus (pars triangularis) to reduce maladaptive right-hemisphere overactivation."
targets_impairments: ["fluency", "semantics", "syntactic_processing"]
notes: "This therapy is typically used as a supportive adjunct to standard speech and language therapy (SLT)."

findings:
  - id: f1
    target: severity_metric
    target_kind: predictor
    claim: "Inhibitory 1 Hz rTMS over the right posterior inferior frontal gyrus, combined with speech and language therapy, significantly improves global language recovery in subacute stroke patients."
    direction: likely
    relationship: responder
    citation: "@Thiel2013"
    method: TMS
    design: RCT
    strength: strong
    evidence_quality: RCT
    sample:
      n: 24
      population: "subacute poststroke aphasia"
      time_post_onset: "average 5.4 weeks (TMS group), 7.2 weeks (sham group)"
      age_range: "mean 69.8-71.2 years"
      handedness: "all right handed"
      language: "German"
    statistics:
      threshold: "P=0.003"
      effect_size: "mean change 23.6 (TMS) vs 7.55 (sham)"
      p_value: 0.003
    confounders_controlled: ["initial test performance", "infarct volume", "aphasia type"]
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "triangular part of the right posterior inferior frontal gyrus"
    author_limitations:
      - "The study was underpowered to detect a specific aphasia type and treatment interaction."
      - "Infarct location probably is the more relevant indicator [than size] because small strategic lesions can have severe clinical effects."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 2242"
      confidence: high
      flags: []
    source_passages:
      - section: "Abstract"
        page: 1
        quote: "The primary outcome measure, global Aachen Aphasia Test score change, was significantly higher in the rTMS group (t test, P=0.003)."
        supports: claim
      - section: "Methods"
        page: 2
        quote: "A total of 30 patients with first ischemic infarct within the left middle cerebral artery territory were recruited... All patients were right handed, with German as the first language."
        supports: sample
      - section: "Methods"
        page: 2
        quote: "patients either received 20 minutes of inhibitory 1 Hz rTMS... over the triangular part of the right posterior inferior frontal gyrus (treatment group) or over the midline at the vertex (sham group)"
        supports: method
      - section: "Results"
        page: 2
        quote: "Aphasia recovery measured as absolute change in global AAT score was significantly higher in the TMS group (mean 23.6\u00b1SD 12.15) than in the sham group (mean 7.55\u00b1SD 11.00; P=0.003; Figure 1A; Table 2)."
        supports: statistics
      - section: "Discussion"
        page: 5
        quote: "however, the study was underpowered to detect a specific aphasia type and treatment interaction, so larger studies are needed to specifically address this question."
        supports: limitation

  - id: f2
    target: severity_metric
    target_kind: predictor
    claim: "Inhibitory rTMS to the right posterior IFG specifically produces the largest gains in naming performance."
    direction: likely
    relationship: responder
    citation: "@Thiel2013"
    method: TMS
    design: RCT
    strength: moderate
    evidence_quality: RCT
    sample:
      n: 24
      population: "subacute poststroke aphasia"
      time_post_onset: "average 5.4-7.2 weeks"
      age_range: "mean 69.8-71.2 years"
      handedness: "all right handed"
      language: "German"
    statistics:
      threshold: "P=0.002"
      effect_size: "not_reported"
      p_value: 0.002
    confounders_controlled: ["initial test performance"]
    confounders_not_controlled: []
    region_definition:
      kind: manual_ROI
      description: "triangular part of the right posterior inferior frontal gyrus"
    author_limitations:
      - "The study was underpowered to detect a specific aphasia type and treatment interaction."
    provenance:
      extracted_by: "agent"
      extracted_on: 2026-01-01
      paper_section: "Results, page 2242"
      confidence: high
      flags: []
    source_passages:
      - section: "Results"
        page: 2
        quote: "The mean increase in subtest scores was higher for the TMS group in all subtests. It was highest for subtest naming (P=0.002)"
        supports: claim
      - section: "Discussion"
        page: 4
        quote: "Consistent with previous studies, the strongest increase was observed on naming performance."
        supports: claim
      - section: "Discussion"
        page: 5
        quote: "however, the study was underpowered to detect a specific aphasia type and treatment interaction"
        supports: limitation
---

This study demonstrates that inhibitory rTMS to the right pars triangularis, when combined with SLT, improves global aphasia recovery in the subacute phase, with the most significant effects seen in naming.
