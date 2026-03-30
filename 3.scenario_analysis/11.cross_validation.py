"""
Cross Validity Analysis -- MiCSS vs Published CISNET/MISCAN Benchmarks

Following Eddy et al. 2012 (ISPOR-SMDM Task Force-7), cross validity
compares model results against other models analyzing the same problem.

This script compares MiCSS outputs (biennial FIT, ages 50-75, 80% adherence)
against published results from MISCAN-Colon, SimCRC, and CRC-SPIN models
used in the USPSTF 2021 colorectal cancer screening recommendations.

IMPORTANT CAVEATS (documented in output):
- CISNET models use US population data; MiCSS uses Chilean population data
- CISNET reports per-1000 40-year-old cohort; MiCSS simulates an open population
- Adherence assumptions differ across models
- Direct numeric comparison is illustrative, not definitive
"""
import pandas as pd
import os

OUTPUT_DIR = 'validation'
SCENARIO_DIR = '4.simulation_outputs/default200'

# ---- Published benchmarks ----
# Source: Knudsen et al. 2021, JAMA (USPSTF 2021 modeling study)
# Strategy: FIT every 2 years, ages 50-75
# Values are ranges across SimCRC, CRC-SPIN, and MISCAN-Colon
# Units: per 1,000 individuals in a 40-year-old cohort followed to death
CISNET_BENCHMARKS = {
    'metric': [
        'Life-years gained per 1,000',
        'CRC deaths averted per 1,000',
        'Colonoscopies per 1,000',
        'FITs per 1,000',
    ],
    'cisnet_low': [270, 5.0, 1700, 13000],
    'cisnet_high': [330, 8.0, 2200, 13000],
    'source': [
        'Knudsen et al. 2021 / Lansdorp-Vogelaar et al. 2009',
        'Knudsen et al. 2021',
        'Knudsen et al. 2021',
        'Knudsen et al. 2021',
    ],
}

CISNET_SCREENING_YEARS = 35


def load_scenario(folder: str, adherence: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    stats_path = os.path.join(folder, f'population_stats/population_stats{adherence}.csv')
    costs_path = os.path.join(folder, f'costs/costs_{adherence}.csv')
    stats = pd.read_csv(stats_path, sep=';')
    costs = pd.read_csv(costs_path, sep=';')
    return stats, costs


def compute_micss_metrics(stats: pd.DataFrame, costs: pd.DataFrame) -> dict:
    """Compute per-1,000 aggregate metrics using both total and eligible population."""
    avg_pop = stats['Total'].mean()
    avg_eligible = stats['50-75'].mean()
    n_years = len(stats)

    total_lyg = costs['YearsGained'].sum()
    total_dalys = costs['DALYGained'].sum()
    total_colonoscopies = costs['Colonoscopy'].sum()
    total_fits = costs['Fit'].sum()

    scale_total = 1000.0 / avg_pop
    scale_eligible = 1000.0 / avg_eligible if avg_eligible > 0 else 0

    return {
        'avg_population': avg_pop,
        'avg_eligible': avg_eligible,
        'n_years': n_years,
        'lyg_per_1000_total_per_year': round(total_lyg * scale_total / n_years, 4),
        'lyg_per_1000_eligible_per_year': round(total_lyg * scale_eligible / n_years, 4),
        'dalys_per_1000_total_per_year': round(total_dalys * scale_total / n_years, 4),
        'dalys_per_1000_eligible_per_year': round(total_dalys * scale_eligible / n_years, 4),
        'colonoscopies_per_1000_total_per_year': round(total_colonoscopies * scale_total / n_years, 2),
        'colonoscopies_per_1000_eligible_per_year': round(total_colonoscopies * scale_eligible / n_years, 2),
        'fits_per_1000_total_per_year': round(total_fits * scale_total / n_years, 2),
        'fits_per_1000_eligible_per_year': round(total_fits * scale_eligible / n_years, 2),
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stats_screen, costs_screen = load_scenario(SCENARIO_DIR, '0_8')
    stats_noscreen, costs_noscreen = load_scenario(SCENARIO_DIR, '0')

    micss = compute_micss_metrics(stats_screen, costs_screen)

    avg_pop = micss['avg_population']
    avg_eligible = micss['avg_eligible']
    n_years = micss['n_years']

    base_cancer_deaths = stats_noscreen['DeathsByCancer'].sum()
    screen_cancer_deaths = stats_screen['DeathsByCancer'].sum()
    deaths_averted = base_cancer_deaths - screen_cancer_deaths
    deaths_averted_per_1000_total = round(
        deaths_averted * 1000.0 / avg_pop / n_years, 4
    )
    deaths_averted_per_1000_eligible = round(
        deaths_averted * 1000.0 / avg_eligible / n_years, 4
    ) if avg_eligible > 0 else 0

    cisnet_lyg_low_annual = round(CISNET_BENCHMARKS['cisnet_low'][0] / CISNET_SCREENING_YEARS, 2)
    cisnet_lyg_high_annual = round(CISNET_BENCHMARKS['cisnet_high'][0] / CISNET_SCREENING_YEARS, 2)
    cisnet_deaths_low_annual = round(CISNET_BENCHMARKS['cisnet_low'][1] / CISNET_SCREENING_YEARS, 4)
    cisnet_deaths_high_annual = round(CISNET_BENCHMARKS['cisnet_high'][1] / CISNET_SCREENING_YEARS, 4)
    cisnet_col_low_annual = round(CISNET_BENCHMARKS['cisnet_low'][2] / CISNET_SCREENING_YEARS, 1)
    cisnet_col_high_annual = round(CISNET_BENCHMARKS['cisnet_high'][2] / CISNET_SCREENING_YEARS, 1)
    cisnet_fit_low_annual = round(CISNET_BENCHMARKS['cisnet_low'][3] / CISNET_SCREENING_YEARS, 1)
    cisnet_fit_high_annual = round(CISNET_BENCHMARKS['cisnet_high'][3] / CISNET_SCREENING_YEARS, 1)

    # Build comparison table with both denominators
    rows = [
        {
            'Metric': 'LYG per 1,000 per year',
            'MiCSS (total pop)': micss['lyg_per_1000_total_per_year'],
            'MiCSS (ages 50-75)': micss['lyg_per_1000_eligible_per_year'],
            'CISNET Low': cisnet_lyg_low_annual,
            'CISNET High': cisnet_lyg_high_annual,
            'Note': 'CISNET per 1,000 cohort; annualized /35 yrs',
        },
        {
            'Metric': 'DALYs gained per 1,000 per year',
            'MiCSS (total pop)': micss['dalys_per_1000_total_per_year'],
            'MiCSS (ages 50-75)': micss['dalys_per_1000_eligible_per_year'],
            'CISNET Low': '-',
            'CISNET High': '-',
            'Note': 'CISNET reports LYG, not DALYs',
        },
        {
            'Metric': 'Colonoscopies per 1,000 per year',
            'MiCSS (total pop)': micss['colonoscopies_per_1000_total_per_year'],
            'MiCSS (ages 50-75)': micss['colonoscopies_per_1000_eligible_per_year'],
            'CISNET Low': cisnet_col_low_annual,
            'CISNET High': cisnet_col_high_annual,
            'Note': 'CISNET per 1,000 cohort; annualized /35 yrs',
        },
        {
            'Metric': 'FITs per 1,000 per year',
            'MiCSS (total pop)': micss['fits_per_1000_total_per_year'],
            'MiCSS (ages 50-75)': micss['fits_per_1000_eligible_per_year'],
            'CISNET Low': cisnet_fit_low_annual,
            'CISNET High': cisnet_fit_high_annual,
            'Note': 'CISNET per 1,000 cohort; annualized /35 yrs',
        },
        {
            'Metric': 'CRC deaths averted per 1,000 per year',
            'MiCSS (total pop)': deaths_averted_per_1000_total,
            'MiCSS (ages 50-75)': deaths_averted_per_1000_eligible,
            'CISNET Low': cisnet_deaths_low_annual,
            'CISNET High': cisnet_deaths_high_annual,
            'Note': 'CISNET per 1,000 cohort; annualized /35 yrs',
        },
    ]

    df_comparison = pd.DataFrame(rows)
    output_path = os.path.join(OUTPUT_DIR, 'cross_validation_comparison.csv')
    df_comparison.to_csv(output_path, index=False, sep=';')

    print('\n=== Cross Validation: MiCSS vs CISNET/MISCAN Benchmarks ===\n')
    print(df_comparison.to_string(index=False))
    print(f'\nMiCSS scenario: biennial FIT 50-75, 80% adherence, {n_years} years')
    print(f'Average total population: {avg_pop:,.0f}')
    print(f'Average screening-eligible population (50-75): {avg_eligible:,.0f}')
    print(f'\nComparison saved to: {output_path}')
    print('\nCAVEATS:')
    print('- CISNET uses US population structure; MiCSS uses Chilean (SSMS) population')
    print('- CISNET tracks a closed cohort from age 40; MiCSS simulates an open population')
    print('- "MiCSS (ages 50-75)" normalizes to screening-eligible pop for fairer comparison')
    print('- Adherence definitions differ (CISNET uses per-round; MiCSS uses lifetime binary)')
    print('- Annualized CISNET rates are approximate (lifetime / ~35 screening years)')


if __name__ == '__main__':
    main()
