# Face Validity Assessment -- MiCSS Model

Following the ISPOR-SMDM Modeling Good Research Practices Task Force-7 (Eddy et al., 2012),
face validity is assessed by having domain experts evaluate the model structure, data sources,
assumptions, and results for plausibility.

## Expert Panel

| Name | Credentials | Affiliation | Role in Review |
|---|---|---|---|
| Dr. Francisco Lopez Costner | Physician | Clinical collaborator | Guided understanding of CRC natural history, screening protocols, and treatment pathways |
| Dr. Laura Itriago | Physician | Clinical collaborator | Guided understanding of CRC epidemiology and clinical decision-making |
| Dr. Francisco Alvarez | Physician | Clinical collaborator | Guided understanding of CRC clinical aspects and healthcare system context |

## Review Process

The three clinical experts listed above were involved throughout the model development process.
Their role was twofold:

1. **Domain knowledge transfer:** They helped the modeler (Tomas Alvarez) understand the medical
   aspects of colorectal cancer -- natural history, the adenoma-carcinoma sequence, screening
   modalities (FIT and colonoscopy), test performance characteristics, treatment pathways by
   stage, and the Chilean healthcare context -- so that the model could be constructed on a
   sound clinical foundation.

2. **Output review:** Once the model was producing results, the experts reviewed the simulation
   outputs (CRC incidence rates, stage distributions, screening resource utilization, cost
   estimates, and DALY gains) and qualified them as **reasonable** given their clinical experience.

## What Was Reviewed

### Model Structure
- [x] The adenoma-carcinoma progression pathway is clinically plausible
- [x] The preclinical sojourn time model (age- and sex-dependent, from Brenner et al. 2011) is appropriate
- [x] The screening logic (FIT followed by diagnostic colonoscopy for positives) reflects clinical practice
- [x] The binary adherence model (lifetime screenable / not screenable) is a simplification but acceptable for a first version
- [x] Population dynamics (births, aging, non-cancer mortality) are structurally sound

### Data Sources and Parameters
- [x] CRC lifetime prevalence of 4.2% (American Cancer Society) is a reasonable proxy
- [x] FIT sensitivity (79%) and specificity (94%) from Lee et al. 2014 meta-analysis are appropriate
- [x] Preclinical sojourn times from Brenner et al. 2011 are well-cited in the literature
- [x] Cancer stage probabilities from van Rossum et al. 2009 are appropriate for an unscreened vs screened comparison
- [x] US Social Security cohort life tables are a reasonable proxy for general mortality (Chilean-specific tables were not available at the age-sex-cohort granularity needed)
- [x] CRC-specific life expectancies from Shack et al. 2012 are reasonable
- [x] Treatment costs from the Basque public healthcare system are the best available proxy in the absence of Chilean stage-specific data

### Model Outputs
- [x] CRC case volumes are proportionally consistent with GLOBOCAN 2022 Chile data
- [x] Stage distribution at diagnosis (symptomatic vs asymptomatic detection) aligns with published literature
- [x] Screening resource utilization (FIT counts, colonoscopies) is within plausible ranges
- [x] Cost per DALY gained is below 1x GDP per capita, consistent with cost-effectiveness expectations for CRC screening in middle-income countries
- [x] DALYs gained increase monotonically with adherence, as expected

## Expert Verdict

The clinical experts reviewed the model outputs and **qualified the results as reasonable**.
They noted the following caveats:
- Treatment costs should ideally be sourced from Chilean data when available
- The binary adherence model does not capture real-world screening behavior dynamics
- Polypectomy-induced CRC incidence reduction is not yet incorporated

## Date of Review

Model development and iterative expert consultation: 2023-2024.
Final output review: 2024.
