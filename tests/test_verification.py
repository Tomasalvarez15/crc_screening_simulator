"""
Verification / Internal Validity tests for MiCSS.

Following Eddy et al. 2012 (ISPOR-SMDM Task Force-7), verification checks
that the code implements the conceptual model correctly. These tests use
extreme parameter values and conservation laws to detect coding errors.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '2.simulation'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from population import Population


# ---------------------------------------------------------------------------
# Extreme-value tests
# ---------------------------------------------------------------------------

def test_zero_prevalence():
    """With 0% CRC prevalence, no one develops cancer."""
    pop = Population(0.8, 'verify_zero_prev')
    pop.years_to_simulate = 3
    pop.crc_prevalence = 0.0
    pop.simulate()
    for row in pop._stats_rows:
        assert row['HaveCancer'] == 0
        assert row['SymptomaticTreatments'] == 0
        assert row['AsymptomaticTreatments'] == 0
        assert row['DeathsByCancer'] == 0
        assert row['TruePositives'] == 0
    for row in pop._costs_rows:
        assert row['Cancer Treatments'] == 0
        assert row['DALYGained'] == 0


def test_full_prevalence():
    """With 100% CRC prevalence, every person is assigned a cancer history."""
    pop = Population(0.0, 'verify_full_prev')
    pop.years_to_simulate = 5
    pop.crc_prevalence = 1.0
    pop.simulate()
    total_treatments = sum(
        r['SymptomaticTreatments'] + r['AsymptomaticTreatments']
        for r in pop._stats_rows
    )
    assert total_treatments > 0, "With 100% prevalence some cancers must be treated"


def test_perfect_sensitivity():
    """With FIT sensitivity=1.0 and full adherence, every detectable cancer is found."""
    pop = Population(1.0, 'verify_perf_sens')
    pop.years_to_simulate = 5
    pop.fit_sensitivity = 1.0
    pop.simulate()
    total_tp = sum(r['TruePositives'] for r in pop._stats_rows)
    total_asymp = sum(r['AsymptomaticTreatments'] for r in pop._stats_rows)
    total_polypectomies = sum(r['Polypectomies'] for r in pop._stats_rows)
    assert total_tp == total_asymp + total_polypectomies, (
        "With perfect sensitivity, every true positive should result in "
        "either an asymptomatic treatment or a polypectomy"
    )


def test_zero_sensitivity():
    """With FIT sensitivity=0.0, screening never detects cancer."""
    pop = Population(1.0, 'verify_zero_sens')
    pop.years_to_simulate = 5
    pop.fit_sensitivity = 0.0
    pop.simulate()
    for row in pop._stats_rows:
        assert row['TruePositives'] == 0
        assert row['AsymptomaticTreatments'] == 0


def test_perfect_specificity():
    """With FIT specificity=1.0, there are no false positives."""
    pop = Population(1.0, 'verify_perf_spec')
    pop.years_to_simulate = 5
    pop.fit_specificity = 1.0
    pop.simulate()
    for row in pop._stats_rows:
        assert row['FalsePositives'] == 0


def test_zero_specificity():
    """With FIT specificity=0.0, every negative FIT is a false positive triggering colonoscopy."""
    pop = Population(1.0, 'verify_zero_spec')
    pop.years_to_simulate = 3
    pop.fit_specificity = 0.0
    pop.simulate()
    total_fp = sum(r['FalsePositives'] for r in pop._stats_rows)
    total_screened = sum(r['Screened'] for r in pop._stats_rows)
    total_tp = sum(r['TruePositives'] for r in pop._stats_rows)
    assert total_fp > 0, "With 0% specificity there must be false positives"
    assert total_fp + total_tp >= total_screened * 0.5, (
        "Most screened people without detectable cancer should produce false positives"
    )


def test_cancer_deaths_tracked():
    """With 100% CRC prevalence and no screening, cancer deaths must be recorded."""
    pop = Population(0.0, 'verify_cancer_deaths')
    pop.years_to_simulate = 10
    pop.crc_prevalence = 1.0
    pop.simulate()
    total_cancer_deaths = sum(r['DeathsByCancer'] for r in pop._stats_rows)
    assert total_cancer_deaths > 0, (
        "With 100% CRC prevalence, some deaths must be attributed to cancer"
    )


def test_impossible_screening_interval():
    """With screening ages set to an impossible range, no one is screened."""
    pop = Population(1.0, 'verify_no_screen')
    pop.years_to_simulate = 3
    pop.screening_frequency = ['Never', 200, 200, 1, 0]
    pop.simulate()
    for row in pop._stats_rows:
        assert row['Screened'] == 0
        assert row['FalsePositives'] == 0
        assert row['TruePositives'] == 0
    for row in pop._costs_rows:
        assert row['Fit'] == 0
        assert row['Colonoscopy'] == 0


# ---------------------------------------------------------------------------
# Conservation tests
# ---------------------------------------------------------------------------

def test_population_conservation():
    """Total population next year = this year + births - deaths."""
    pop = Population(0.2, 'verify_conservation')
    pop.years_to_simulate = 5
    pop.simulate()
    for i in range(len(pop._stats_rows) - 1):
        current = pop._stats_rows[i]
        nxt = pop._stats_rows[i + 1]
        expected_next = current['Total'] + current['Births'] - current['Deaths']
        assert nxt['Total'] == expected_next, (
            f"Year {current['Year']}: {current['Total']} + {current['Births']} "
            f"- {current['Deaths']} = {expected_next}, but got {nxt['Total']}"
        )


def test_age_consistency():
    """After simulation, no person has age < 0 or age > 120."""
    pop = Population(0.2, 'verify_age')
    pop.years_to_simulate = 3
    pop.simulate()
    for person in pop.population:
        assert 0 <= person.age <= 120, f"Person age {person.age} out of bounds"


# ---------------------------------------------------------------------------
# Boundary tests
# ---------------------------------------------------------------------------

def test_screening_age_boundaries():
    """Only persons aged 50-75 (biennial default) should be screenable."""
    pop = Population(1.0, 'verify_boundary')
    pop.years_to_simulate = 1
    pop.simulate()
    assert pop.screenable(49) == False
    assert pop.screenable(50) == True
    assert pop.screenable(75) == False  # 75 is odd, biennial starts at 50 (even)
    assert pop.screenable(74) == True
    assert pop.screenable(76) == False
