"""
Closed-Cohort Cross Validation -- MiCSS vs CISNET Benchmarks

Runs a closed-cohort simulation (1,000 individuals from age 40 to death)
with and without biennial FIT screening (ages 50-75), then compares the
results directly against published CISNET/MISCAN benchmarks from
Knudsen et al. 2021 (USPSTF modeling study).

This eliminates the open-population denominator mismatch that complicates
the standard cross-validation in 11.cross_validation.py.
"""
import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '2.simulation'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from cohort_simulation import CohortSimulation

OUTPUT_DIR = 'validation'

CISNET_BENCHMARKS = {
    'LYG per 1,000': (270, 330),
    'CRC deaths averted per 1,000': (5.0, 8.0),
    'Colonoscopies per 1,000': (1700, 2200),
    'FITs per 1,000': (13000, 13000),
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print('=== Cohort Cross Validation: MiCSS vs CISNET ===\n')

    t0 = time.time()
    screening = CohortSimulation(cohort_size=1000, adherence=1.0, screening=True)
    screen_results = screening.simulate()
    print(f'  Screening cohort: {int(time.time() - t0)}s')

    t0 = time.time()
    baseline = CohortSimulation(cohort_size=1000, adherence=0.0, screening=False)
    base_results = baseline.simulate()
    print(f'  Baseline cohort:  {int(time.time() - t0)}s')

    deaths_averted = base_results['cancer_deaths_per_1000'] - screen_results['cancer_deaths_per_1000']

    rows = [
        {
            'Metric': 'LYG per 1,000',
            'MiCSS Cohort': screen_results['lyg_per_1000'],
            'CISNET Low': CISNET_BENCHMARKS['LYG per 1,000'][0],
            'CISNET High': CISNET_BENCHMARKS['LYG per 1,000'][1],
            'In Range': _in_range(screen_results['lyg_per_1000'], *CISNET_BENCHMARKS['LYG per 1,000']),
        },
        {
            'Metric': 'CRC deaths averted per 1,000',
            'MiCSS Cohort': deaths_averted,
            'CISNET Low': CISNET_BENCHMARKS['CRC deaths averted per 1,000'][0],
            'CISNET High': CISNET_BENCHMARKS['CRC deaths averted per 1,000'][1],
            'In Range': _in_range(deaths_averted, *CISNET_BENCHMARKS['CRC deaths averted per 1,000']),
        },
        {
            'Metric': 'Colonoscopies per 1,000',
            'MiCSS Cohort': screen_results['colonoscopies_per_1000'],
            'CISNET Low': CISNET_BENCHMARKS['Colonoscopies per 1,000'][0],
            'CISNET High': CISNET_BENCHMARKS['Colonoscopies per 1,000'][1],
            'In Range': _in_range(screen_results['colonoscopies_per_1000'], *CISNET_BENCHMARKS['Colonoscopies per 1,000']),
        },
        {
            'Metric': 'FITs per 1,000',
            'MiCSS Cohort': screen_results['fits_per_1000'],
            'CISNET Low': CISNET_BENCHMARKS['FITs per 1,000'][0],
            'CISNET High': CISNET_BENCHMARKS['FITs per 1,000'][1],
            'In Range': _in_range(screen_results['fits_per_1000'], *CISNET_BENCHMARKS['FITs per 1,000']),
        },
    ]

    df = pd.DataFrame(rows)

    print('\n--- Comparison (per 1,000 individuals, lifetime) ---\n')
    print(df.to_string(index=False))

    print('\n--- Additional MiCSS Cohort Details ---')
    print(f'  DALYs gained per 1,000:            {screen_results["dalys_per_1000"]}')
    print(f'  Asymptomatic treatments per 1,000:  {screen_results["total_asymptomatic_treatments"]}')
    print(f'  Symptomatic treatments per 1,000:   {screen_results["total_symptomatic_treatments"]}')
    print(f'  CRC deaths (screening):             {screen_results["cancer_deaths_per_1000"]} per 1,000')
    print(f'  CRC deaths (no screening):          {base_results["cancer_deaths_per_1000"]} per 1,000')
    print(f'  Total cost per person (CLP):        {screen_results["cost_per_person"]:,.0f}')

    output_path = os.path.join(OUTPUT_DIR, 'cohort_cross_validation.csv')
    df.to_csv(output_path, index=False, sep=';')
    print(f'\nSaved to: {output_path}')

    print('\nCAVEATS:')
    print('- CISNET uses US population; MiCSS uses Chilean life tables')
    print('- CISNET models the adenoma-carcinoma sequence; MiCSS assigns cancer directly')
    print('- Per-round adherence (CISNET) vs binary lifetime adherence (MiCSS)')
    print('- MiCSS cohort uses 100% adherence for closest CISNET comparability')


def _in_range(value: float, low: float, high: float) -> str:
    if low <= value <= high:
        return 'YES'
    ratio = value / ((low + high) / 2)
    return f'No ({ratio:.1%} of midpoint)'


if __name__ == '__main__':
    main()
