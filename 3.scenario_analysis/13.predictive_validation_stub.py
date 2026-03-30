"""
Predictive Validity Framework (Stub) -- MiCSS

Following Eddy et al. 2012 (ISPOR-SMDM Task Force-7), predictive validity
compares model predictions against prospectively observed events -- data
that were collected AFTER the model was built.

MiCSS was developed in 2023-2024 with a starting year of 2023. As Chilean
national cancer registry data for 2025-2026+ become available, this script
can be used to compare model projections against observed values.

STATUS: Placeholder. Fill in observed data when available.
"""
import pandas as pd
import os

OUTPUT_DIR = 'validation'
SCENARIO_DIR = '4.simulation_outputs/default'

# ---- Model predictions (extracted from simulation outputs) ----
# These will be auto-loaded from the default 0% adherence scenario
# for the relevant years (natural history baseline).

# ---- Observed data placeholders ----
# Fill these in when Chilean cancer registry data become available.
OBSERVED_DATA = {
    2025: {
        'crc_new_cases': None,       # Fill from Chilean cancer registry
        'crc_deaths': None,          # Fill from DEIS
        'source': 'TBD - Chilean cancer registry / DEIS',
    },
    2026: {
        'crc_new_cases': None,
        'crc_deaths': None,
        'source': 'TBD',
    },
}


def load_model_predictions(folder: str) -> pd.DataFrame:
    """Load model predictions for validation years."""
    stats = pd.read_csv(
        os.path.join(folder, 'population_stats/population_stats0.csv'), sep=';'
    )
    costs = pd.read_csv(
        os.path.join(folder, 'costs/costs_0.csv'), sep=';'
    )

    predictions = []
    for _, row in stats.iterrows():
        year = int(row['Year'])
        if year in OBSERVED_DATA:
            cost_row = costs[costs['Year'] == year].iloc[0] if len(costs[costs['Year'] == year]) > 0 else None
            total_treatments = 0
            if cost_row is not None:
                total_treatments = (
                    cost_row['CancerStageITreatments'] +
                    cost_row['CancerStageIITreatments'] +
                    cost_row['CancerStageIIITreatments'] +
                    cost_row['CancerStageIVTreatments']
                )
            predictions.append({
                'Year': year,
                'Model_CRC_Cases': round(total_treatments),
                'Model_CRC_Deaths': round(row['DeathsByCancer']),
                'Model_Population': round(row['Total']),
                'Observed_CRC_Cases': OBSERVED_DATA[year]['crc_new_cases'],
                'Observed_CRC_Deaths': OBSERVED_DATA[year]['crc_deaths'],
                'Source': OBSERVED_DATA[year]['source'],
            })

    return pd.DataFrame(predictions)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print('\n=== Predictive Validation Framework (Stub) ===\n')
    print('This script compares model predictions for future years')
    print('against observed data when it becomes available.\n')

    predictions = load_model_predictions(SCENARIO_DIR)

    if predictions.empty:
        print('No prediction years found in simulation outputs.')
        print('The default scenario may not extend to 2025+.')
        print('Run the default200 scenario or check year range.')
        return

    print(predictions.to_string(index=False))
    print()

    has_observed = predictions['Observed_CRC_Cases'].notna().any()
    if has_observed:
        print('Observed data found -- computing prediction accuracy...')
        for _, row in predictions.iterrows():
            if row['Observed_CRC_Cases'] is not None:
                ratio = row['Model_CRC_Cases'] / row['Observed_CRC_Cases']
                print(f"  {row['Year']}: Model/Observed cases = {ratio:.3f}")
    else:
        print('STATUS: No observed data available yet.')
        print('ACTION: Update OBSERVED_DATA dict in this script when')
        print('        Chilean cancer registry data for 2025+ are published.')

    output_path = os.path.join(OUTPUT_DIR, 'predictive_validation_stub.csv')
    predictions.to_csv(output_path, index=False, sep=';')
    print(f'\nSaved to: {output_path}')


if __name__ == '__main__':
    main()
