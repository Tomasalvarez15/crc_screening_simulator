# MiCSS Model Validation Report

Following the ISPOR-SMDM Modeling Good Research Practices Task Force-7 framework
(Eddy et al., 2012), the MiCSS microsimulation model was assessed across five
validation types. This report summarizes the results, identifies issues discovered,
and recommends improvements.

**Updates (March 2025):**

1. **Cancer death tracking bug** -- fixed by introducing a `cancer_determined_death`
   flag in `Person` that persists after treatment.
2. **NumPy random seeding** -- fixed by adding `np.random.seed()` calls alongside
   existing Python `random.seed()` calls.
3. **Life-Years Gained (LYG)** -- now reported in cross-validation alongside DALYs.
4. **Normalized denominators** -- cross-validation now reports metrics per 1,000
   screening-eligible population (ages 50-75) in addition to total population.
5. **Closed-cohort benchmarking** -- a new simulation mode following 1,000
   individuals from age 40 to death for direct CISNET comparison.
6. **Probabilistic sensitivity analysis (PSA)** -- new script sampling parameter
   distributions across 1,000 iterations with CE scatter and CEAC outputs.
7. **Polypectomy-induced incidence reduction** -- 52% of screening-detected cancers
   are now reclassified as removed polyps, reverting the person to natural death age.

---

## 1. Face Validity

**Method:** Three clinical experts (Dr. Francisco Lopez Costner, Dr. Laura Itriago,
and Dr. Francisco Alvarez) were involved throughout model development. They helped
the modeler understand CRC natural history, screening protocols, and treatment
pathways, and reviewed model outputs for plausibility.

**Result:** The experts qualified the model results as **reasonable**. They noted
that treatment costs should ideally use Chilean data, and that the binary adherence
model is a simplification.

**Assessment:** PASS. Face validity is established through documented expert review.

**What to improve:**

- Conduct a formal structured review session with a written protocol
- Include a health economist in addition to the clinical experts
- Document specific quantitative thresholds that experts considered "reasonable"

---

## 2. Verification (Internal Validity)

**Method:** 15 automated tests were executed using pytest: 4 smoke tests
(`test_simulation.py`) and 11 verification tests (`test_verification.py`).

### Results


| Test                               | Result |
| ---------------------------------- | ------ |
| test_zero_adherence_no_screening   | PASS   |
| test_population_growth             | PASS   |
| test_fit_cost_applied              | PASS   |
| test_deterministic_seed            | PASS   |
| test_zero_prevalence               | PASS   |
| test_full_prevalence               | PASS   |
| test_perfect_sensitivity           | PASS   |
| test_zero_sensitivity              | PASS   |
| test_perfect_specificity           | PASS   |
| test_zero_specificity              | PASS   |
| test_cancer_deaths_tracked         | PASS   |
| test_impossible_screening_interval | PASS   |
| test_population_conservation       | PASS   |
| test_age_consistency               | PASS   |
| test_screening_age_boundaries      | PASS   |


**All 15 tests pass.** Key fixes applied:

- **NumPy seeding:** Added `np.random.seed()` alongside Python `random.seed()` calls.
  The `test_deterministic_seed` test now passes consistently.
- **Cancer death tracking:** A `cancer_determined_death` flag persists after treatment.
  The `test_cancer_deaths_tracked` test confirms cancer deaths are recorded.
- **Polypectomy consistency:** The `test_perfect_sensitivity` test verifies that
  true positives equal asymptomatic treatments plus polypectomies.

**Assessment:** PASS. All verification tests pass after bug fixes and new features.

**What to improve on verification:**

- Add trace-level tests that follow individual person trajectories
- Add tests for screening-induced life extension
- Add tests verifying polypectomy rate is approximately 52% of true positives

---

## 3. Cross Validity

### 3a. Open-Population Cross Validation

**Method:** MiCSS outputs for biennial FIT screening (ages 50-75, 80% adherence,
200-year simulation) were compared against CISNET/MISCAN benchmarks (Knudsen et al.,
2021). Metrics are now reported per 1,000 total population and per 1,000
screening-eligible population (ages 50-75).


| Metric                          | MiCSS (total) | MiCSS (50-75) | CISNET Low | CISNET High |
| ------------------------------- | ------------- | -------------- | ---------- | ----------- |
| LYG per 1,000 per year          | 0.28          | 0.89           | 7.71       | 9.43        |
| DALYs gained per 1,000 per year | 0.26          | 0.82           | --         | --          |
| Colonoscopies per 1,000/yr      | 7.76          | 24.76          | 48.6       | 62.9        |
| FITs per 1,000 per year         | 125.15        | 399.46         | 371.4      | 371.4       |
| Deaths averted per 1,000/yr     | 0.13          | 0.41           | 0.14       | 0.23        |


**Key observations:**

1. **FITs per 1,000 eligible (399.5)** is now very close to CISNET (371.4) -- within
   8% when normalized to screening-eligible population. This validates the screening
   frequency logic.
2. **CRC deaths averted per 1,000 eligible (0.41)** exceeds CISNET's annualized
   range (0.14-0.23), likely because polypectomy effectively prevents many cancer
   deaths in the MiCSS model.
3. **LYG per 1,000 eligible (0.89)** is still lower than CISNET (7.7-9.4), expected
   because LYG only counts gains from asymptomatic detection stage shift, not the
   full life extension from polypectomy-prevented deaths.
4. **Colonoscopies per 1,000 eligible (24.76)** is below CISNET range, reflecting
   the biennial schedule and binary adherence model.

### 3b. Closed-Cohort Cross Validation

**Method:** A new closed-cohort simulation follows 1,000 individuals from age 40
to death with 100% per-round adherence, directly matching CISNET methodology.


| Metric                          | MiCSS Cohort | CISNET Low | CISNET High | Match     |
| ------------------------------- | ------------ | ---------- | ----------- | --------- |
| LYG per 1,000                   | 57           | 270        | 330         | 19%       |
| CRC deaths averted per 1,000    | 18           | 5          | 8           | 277%      |
| Colonoscopies per 1,000         | 857          | 1,700      | 2,200       | 44%       |
| FITs per 1,000                  | 12,898       | 13,000     | 13,000      | **99.2%** |


**Key observations:**

1. **FITs per 1,000 (12,898 vs 13,000)** is an almost perfect match, confirming that
   biennial FIT screening from ages 50-75 produces the right number of tests.
2. **CRC deaths averted (18 vs 5-8)** is higher than CISNET because the polypectomy
   mechanism effectively cures 52% of screening-detected cancers. CISNET models the
   adenoma-carcinoma sequence more granularly.
3. **LYG (57 vs 270-330)** is lower because the model only counts LYG from
   asymptomatic-to-symptomatic stage shift, not from polypectomy-prevented deaths.
   Polypectomy restores natural life expectancy but this gain is not captured in the
   current LYG metric.
4. **Colonoscopies (857 vs 1,700-2,200)** are lower because MiCSS only performs
   colonoscopies after positive FIT, while CISNET includes diagnostic and surveillance
   colonoscopies.

**Assessment:** PARTIAL. FIT utilization validates well. Structural differences in
how polypectomy, LYG, and colonoscopies are modeled explain the remaining gaps.

**What to improve:**

- Count life-years gained from polypectomy-prevented deaths (natural death age minus
  cancer death age) to capture the full LYG benefit
- Add surveillance colonoscopies after positive findings
- Consider age-dependent adherence rather than lifetime binary

---

## 4. External Validity

**Method:** Model outputs at 0% screening adherence (natural history baseline, default
20-year scenario) were compared against observed Chilean epidemiological data.

### Results

#### CRC Incidence


|                  | Model (raw, avg/yr) | Scaled to Chile | Observed (GLOBOCAN) | Ratio |
| ---------------- | ------------------- | --------------- | ------------------- | ----- |
| Annual CRC cases | 552                 | 8,805           | 6,778               | 1.30  |


Overestimation of ~30%. The 4.2% US-based lifetime CRC risk may be higher than
Chile's actual population risk.

#### CRC Mortality


|                   | Model (raw, avg/yr) | Scaled to Chile | Observed (GLOBOCAN) | Ratio |
| ----------------- | ------------------- | --------------- | ------------------- | ----- |
| Annual CRC deaths | 437                 | 6,977           | 3,330               | 2.10  |


Overestimation of ~110%. The cancer-specific life expectancy parameters may be too
pessimistic, and the model counts every cancer-determined death as a cancer death
even when competing causes might have been closer.

#### Stage Distribution


| Stage | Model | Observed (van Rossum 2009) | Difference |
| ----- | ----- | -------------------------- | ---------- |
| I     | 3.8%  | 4.0%                       | -0.2%      |
| II    | 46.1% | 46.0%                      | +0.1%      |
| III   | 26.4% | 27.0%                      | -0.6%      |
| IV    | 23.7% | 22.0%                      | +1.7%      |


Stage distribution is excellent (all within 2 percentage points).

**Assessment:** MIXED. Stage distribution is strong. Incidence and mortality
overestimation warrant investigation.

**What to improve:**

- Use Chile-specific lifetime CRC risk instead of US 4.2%
- Review cancer life expectancy parameters for competing mortality
- Compare age-specific incidence against Chilean registry data

---

## 5. Predictive Validity


| Year | Model CRC Cases | Model CRC Deaths | Model Population | Observed |
| ---- | --------------- | ---------------- | ---------------- | -------- |
| 2025 | 460             | 326              | 1,149,721        | Pending  |
| 2026 | 484             | 329              | 1,161,463        | Pending  |


**Assessment:** NOT YET EVALUABLE. Framework ready; awaiting Chilean registry data.

---

## 6. Probabilistic Sensitivity Analysis (PSA)

**Method:** 1,000 iterations of the full 20-year simulation were run, each time
sampling model parameters from probability distributions:

- FIT sensitivity: Beta(mean=0.79, n=200) -- sampled mean 0.789, SD 0.029
- FIT specificity: Beta(mean=0.94, n=500) -- sampled mean 0.940, SD 0.011
- CRC prevalence: Beta(mean=0.042, n=5000) -- sampled mean 0.042, SD 0.003
- Treatment costs by stage: Gamma(mean=current, CV=20%)
- Colonoscopy cost: Gamma(mean=421,005, CV=20%) -- sampled mean 417,802
- FIT cost: Gamma(mean=5,865, CV=20%) -- sampled mean 5,925

Each iteration ran a screening scenario (15% adherence) and a no-screening baseline,
computing incremental costs and incremental DALYs/LYG averted.

### Results

#### Summary Statistics (1,000 iterations)


| Metric                   | Mean     | Median   | 2.5th %ile | 97.5th %ile |
| ------------------------ | -------- | -------- | ---------- | ----------- |
| Incremental Cost (M CLP) | 4,570    | 4,349    | -3,754     | 13,577      |
| Incremental DALYs        | 1,264    | 1,263    | 1,087      | 1,439       |
| Incremental LYG          | 1,360    | 1,360    | 1,168      | 1,540       |
| ICER (M CLP / DALY)      | 3.65     | 3.46     | -2.83      | 10.85       |


The negative lower bound on incremental cost indicates that in some parameter
draws, screening is cost-saving (treatment cost savings from polypectomy and
early detection exceed screening costs).

#### Cost-Effectiveness Acceptability Curve (CEAC)


| WTP Threshold (M CLP/DALY) | Probability Cost-Effective |
| --------------------------- | ------------------------- |
| 1                           | 21.5%                     |
| 3                           | 44.4%                     |
| 5                           | 67.5%                     |
| 10                          | 96.1%                     |
| 15                          | 99.6%                     |
| 20                          | 100.0%                    |


At a WTP threshold of 10 M CLP per DALY averted, screening is cost-effective in
96.1% of iterations. At 15 M CLP per DALY, it is cost-effective in 99.6%.

For context, Chile's GDP per capita is approximately 17 M CLP (~17,000 USD). Using
the WHO-CHOICE threshold of 1x GDP per capita as the WTP, screening at 15% adherence
is cost-effective with very high probability (>99%).

#### Plots

- **CE scatter plot** (`validation/psa_ce_scatter.png`): Shows the distribution of
  incremental cost vs incremental DALYs across 1,000 iterations. Most points fall
  in the northeast quadrant (more effective, higher cost), with some in the southeast
  (more effective, cost-saving).
- **CEAC** (`validation/psa_ceac.png`): Shows the probability of cost-effectiveness
  as a function of WTP threshold.

**Assessment:** COMPLETE. PSA confirms that screening is robustly cost-effective
across plausible parameter ranges at standard WTP thresholds.

**What to improve:**

- Include adherence rate as a sampled parameter
- Add structural uncertainty (e.g., polypectomy prevention rate)
- Run PSA for multiple adherence levels (not just 15%)
- Report cost per LYG alongside cost per DALY

---

## Summary of Findings


| Validation Type        | Status       | Key Findings                                                       |
| ---------------------- | ------------ | ------------------------------------------------------------------ |
| Face Validity          | PASS         | Experts confirmed plausibility                                     |
| Verification           | PASS         | All 15 tests pass after fixes                                      |
| Cross Validity (open)  | PARTIAL      | FITs align well; LYG gap due to polypectomy metric limitation      |
| Cross Validity (cohort)| PARTIAL      | FITs 99.2% match; deaths averted higher; LYG lower than CISNET     |
| External Validity      | MIXED        | Good stages; 30% incidence and 110% mortality overestimation       |
| Predictive Validity    | PENDING      | Framework ready; no observed data yet                              |
| PSA                    | COMPLETE     | Cost-effective at >96% probability at 10 M CLP/DALY WTP           |


---

## New Features Added

### Polypectomy-Induced Incidence Reduction

When a screening-detected cancer is found asymptomatically (true positive), a
52% probability roll determines whether the cancer is reclassified as a removed
polyp (polypectomy). If prevented:
- Person's death age reverts to natural (non-cancer) lifespan
- No cancer treatment cost is incurred (only colonoscopy cost)
- Person is no longer counted as a cancer death

This feature reduces cancer deaths in screening scenarios and brings the model
closer to real-world screening effectiveness where polyp removal prevents CRC.

### Closed-Cohort Benchmarking

A standalone `CohortSimulation` class (`2.simulation/cohort_simulation.py`) enables
1,000-person cohort runs from age 40 to death, matching CISNET study design for
direct comparability.

### Life-Years Gained and Normalized Denominators

The cross-validation script now reports both LYG and DALYs, and provides rates
per 1,000 total population and per 1,000 screening-eligible (ages 50-75) population
for fairer comparison with CISNET.

---

## Priority Improvements

### High Priority

1. **Count LYG from polypectomy:** Currently, polypectomy-prevented deaths restore
   natural lifespan but the gained years are not included in LYG totals. This
   underestimates the screening benefit by a significant margin.
2. **Investigate incidence/mortality overestimation:** The 30% incidence and 110%
   mortality overestimation likely stem from US-based CRC risk and survival parameters.
   Chile-specific data would improve external validity.
3. **Add surveillance colonoscopies:** The model only counts diagnostic colonoscopies
   after positive FIT. Adding follow-up surveillance colonoscopies would improve
   cross-validation alignment.

### Medium Priority

4. **Extend PSA:** The 1,000-iteration PSA is complete but uses only 15% adherence.
   Run PSA across multiple adherence levels and include structural parameters
   (polypectomy rate, adherence) in the sampling.
5. **Chile-specific calibration targets:** Formal quantitative calibration against
   age-specific incidence from DEIS.
6. **Age-dependent adherence:** Replace binary lifetime adherence with per-round
   probability for more realistic screening behavior.

### Lower Priority

7. **Competing mortality:** Implement logic to distinguish cancer-specific death
   from all-cause death for cancer patients whose natural death would have occurred
   at a similar age.
8. **Additional cohort sizes:** Run cohort benchmarking with 10,000+ individuals
   to reduce stochastic noise in the comparison.
