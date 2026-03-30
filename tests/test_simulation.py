import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '2.simulation'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from population import Population


def test_zero_adherence_no_screening():
    """At 0% adherence, no one is screened and no FITs/colonoscopies occur."""
    pop = Population(0, 'test_zero_adherence')
    pop.years_to_simulate = 3
    pop.simulate()
    for row in pop._stats_rows:
        assert row['Screened'] == 0
        assert row['FalsePositives'] == 0
        assert row['TruePositives'] == 0


def test_population_growth():
    """Population should grow over 5 years (births > deaths in a young population)."""
    pop = Population(0.2, 'test_growth')
    pop.years_to_simulate = 5
    pop.simulate()
    first_year_total = pop._stats_rows[0]['Total']
    last_year_total = pop._stats_rows[-1]['Total']
    assert last_year_total > first_year_total


def test_fit_cost_applied():
    """Different fit_cost values must produce different FIT cost totals."""
    pop_cheap = Population(0.8, 'test_cheap')
    pop_cheap.years_to_simulate = 3
    pop_cheap.fit_cost = 1000
    pop_cheap.simulate()

    pop_expensive = Population(0.8, 'test_expensive')
    pop_expensive.years_to_simulate = 3
    pop_expensive.fit_cost = 10000
    pop_expensive.simulate()

    cheap_total = sum(r['Fit Costs'] for r in pop_cheap._costs_rows)
    expensive_total = sum(r['Fit Costs'] for r in pop_expensive._costs_rows)
    assert expensive_total > cheap_total


def test_deterministic_seed():
    """Same parameters must produce identical results."""
    pop1 = Population(0.2, 'test_seed1')
    pop1.years_to_simulate = 3
    pop1.simulate()

    pop2 = Population(0.2, 'test_seed2')
    pop2.years_to_simulate = 3
    pop2.simulate()

    for r1, r2 in zip(pop1._stats_rows, pop2._stats_rows):
        assert r1 == r2
    for r1, r2 in zip(pop1._costs_rows, pop2._costs_rows):
        assert r1 == r2
