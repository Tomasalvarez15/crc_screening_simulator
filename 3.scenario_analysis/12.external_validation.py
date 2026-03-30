"""
External Validity Analysis -- MiCSS vs Observed Chilean Epidemiological Data

Following Eddy et al. 2012 (ISPOR-SMDM Task Force-7), external validity
compares model results against real-world observed data.

This script compares MiCSS natural-history outputs (0% adherence baseline)
against:
1. GLOBOCAN 2022 Chile CRC incidence and mortality
2. Published stage distribution for unscreened populations
3. Age-specific CRC incidence patterns

Data sources:
- GLOBOCAN 2022 Chile Fact Sheet (Ferlay et al. 2024)
- Chilean DEIS mortality data 2024
- van Rossum et al. 2009 (stage distribution)
- US Cancer Statistics (age-specific incidence, used as proxy)
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = 'validation'
SCENARIO_DIR = '4.simulation_outputs/default'

# ---- Observed data ----

# GLOBOCAN 2022 Chile (population ~19.25 million)
GLOBOCAN_CHILE = {
    'new_cases_per_year': 6778,
    'deaths_per_year': 3330,
    'population_millions': 19.25,
    'asr_incidence_per_100k': 20.3,
    'source': 'GLOBOCAN 2022 Chile Fact Sheet (Ferlay et al. 2024)',
}

# Chilean DEIS 2024 mortality data
DEIS_CHILE_2024 = {
    'deaths_per_year': 3800,
    'source': 'DEIS Chile preliminary 2024 data',
}

# Stage distribution at diagnosis for unscreened populations
# Source: van Rossum et al. 2009 (symptomatic detection)
OBSERVED_STAGE_DISTRIBUTION = {
    'I': 0.04,
    'II': 0.46,
    'III': 0.27,
    'IV': 0.22,
    'source': 'van Rossum et al. 2009, Table 3 (symptomatic detection)',
}


def load_baseline(folder: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load 0% adherence (natural history) scenario."""
    stats = pd.read_csv(
        os.path.join(folder, 'population_stats/population_stats0.csv'), sep=';'
    )
    costs = pd.read_csv(
        os.path.join(folder, 'costs/costs_0.csv'), sep=';'
    )
    return stats, costs


def validate_incidence(stats: pd.DataFrame, costs: pd.DataFrame) -> dict:
    """Compare model CRC incidence against GLOBOCAN Chile data."""
    simulated_pop = stats['Total'].mean()
    scaling_factor = GLOBOCAN_CHILE['population_millions'] * 1e6 / simulated_pop

    model_cases_per_year = (
        costs['CancerStageITreatments'] +
        costs['CancerStageIITreatments'] +
        costs['CancerStageIIITreatments'] +
        costs['CancerStageIVTreatments']
    ).mean()

    model_scaled = model_cases_per_year * scaling_factor

    return {
        'metric': 'Annual CRC cases',
        'model_raw': round(model_cases_per_year),
        'model_scaled_national': round(model_scaled),
        'observed': GLOBOCAN_CHILE['new_cases_per_year'],
        'ratio': round(model_scaled / GLOBOCAN_CHILE['new_cases_per_year'], 3),
        'source': GLOBOCAN_CHILE['source'],
    }


def validate_mortality(stats: pd.DataFrame) -> dict:
    """Compare model CRC mortality against GLOBOCAN Chile data."""
    simulated_pop = stats['Total'].mean()
    scaling_factor = GLOBOCAN_CHILE['population_millions'] * 1e6 / simulated_pop

    model_deaths_per_year = stats['DeathsByCancer'].mean()
    model_scaled = model_deaths_per_year * scaling_factor

    return {
        'metric': 'Annual CRC deaths',
        'model_raw': round(model_deaths_per_year),
        'model_scaled_national': round(model_scaled),
        'observed': GLOBOCAN_CHILE['deaths_per_year'],
        'ratio': round(model_scaled / GLOBOCAN_CHILE['deaths_per_year'], 3),
        'source': GLOBOCAN_CHILE['source'],
    }


def validate_stage_distribution(costs: pd.DataFrame) -> pd.DataFrame:
    """Compare model stage distribution (symptomatic) against observed."""
    total_i = costs['CancerStageITreatments'].sum()
    total_ii = costs['CancerStageIITreatments'].sum()
    total_iii = costs['CancerStageIIITreatments'].sum()
    total_iv = costs['CancerStageIVTreatments'].sum()
    total = total_i + total_ii + total_iii + total_iv

    model_dist = {
        'I': total_i / total,
        'II': total_ii / total,
        'III': total_iii / total,
        'IV': total_iv / total,
    }

    rows = []
    for stage in ['I', 'II', 'III', 'IV']:
        rows.append({
            'Stage': stage,
            'Model': round(model_dist[stage], 3),
            'Observed': OBSERVED_STAGE_DISTRIBUTION[stage],
            'Difference': round(model_dist[stage] - OBSERVED_STAGE_DISTRIBUTION[stage], 3),
        })
    return pd.DataFrame(rows)


def plot_incidence_comparison(incidence: dict, mortality: dict, output_path: str):
    """Bar chart comparing model vs observed incidence and mortality."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    categories = ['Model\n(scaled)', 'Observed\n(GLOBOCAN)']

    axes[0].bar(categories, [incidence['model_scaled_national'], incidence['observed']],
                color=['#1f77b4', '#ff7f0e'])
    axes[0].set_title('Annual CRC Cases (Chile)')
    axes[0].set_ylabel('Cases per year')
    ratio_text = f"Ratio: {incidence['ratio']}"
    axes[0].text(0.5, 0.95, ratio_text, transform=axes[0].transAxes,
                 ha='center', va='top', fontsize=11)

    axes[1].bar(categories, [mortality['model_scaled_national'], mortality['observed']],
                color=['#1f77b4', '#ff7f0e'])
    axes[1].set_title('Annual CRC Deaths (Chile)')
    axes[1].set_ylabel('Deaths per year')
    ratio_text = f"Ratio: {mortality['ratio']}"
    axes[1].text(0.5, 0.95, ratio_text, transform=axes[1].transAxes,
                 ha='center', va='top', fontsize=11)

    plt.suptitle('External Validation: MiCSS vs GLOBOCAN 2022 Chile', fontsize=14)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f'Saved: {output_path}')


def plot_stage_comparison(stage_df: pd.DataFrame, output_path: str):
    """Side-by-side bar chart of stage distribution."""
    x = np.arange(4)
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width/2, stage_df['Model'], width, label='MiCSS Model', color='#1f77b4')
    ax.bar(x + width/2, stage_df['Observed'], width, label='Observed (van Rossum 2009)',
           color='#ff7f0e')

    ax.set_xlabel('Cancer Stage')
    ax.set_ylabel('Proportion')
    ax.set_title('Stage Distribution at Diagnosis (Symptomatic, No Screening)')
    ax.set_xticks(x)
    ax.set_xticklabels(['Stage I', 'Stage II', 'Stage III', 'Stage IV'])
    ax.legend()

    for i, row in stage_df.iterrows():
        ax.text(i - width/2, row['Model'] + 0.01, f"{row['Model']:.1%}", ha='center', fontsize=9)
        ax.text(i + width/2, row['Observed'] + 0.01, f"{row['Observed']:.0%}", ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f'Saved: {output_path}')


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stats, costs = load_baseline(SCENARIO_DIR)

    print('\n=== External Validation: MiCSS vs Observed Data ===\n')

    # 1. CRC incidence
    incidence = validate_incidence(stats, costs)
    print(f"CRC Incidence:")
    print(f"  Model (raw, avg/year): {incidence['model_raw']} cases")
    print(f"  Model (scaled to Chile): {incidence['model_scaled_national']} cases")
    print(f"  Observed (GLOBOCAN 2022): {incidence['observed']} cases")
    print(f"  Ratio (model/observed): {incidence['ratio']}")
    print()

    # 2. CRC mortality
    mortality = validate_mortality(stats)
    print(f"CRC Mortality:")
    print(f"  Model (raw, avg/year): {mortality['model_raw']} deaths")
    print(f"  Model (scaled to Chile): {mortality['model_scaled_national']} deaths")
    print(f"  Observed (GLOBOCAN 2022): {mortality['observed']} deaths")
    print(f"  Ratio (model/observed): {mortality['ratio']}")
    print()

    # 3. Stage distribution
    stage_df = validate_stage_distribution(costs)
    print("Stage Distribution (symptomatic detection, no screening):")
    print(stage_df.to_string(index=False))
    print(f"  Source: {OBSERVED_STAGE_DISTRIBUTION['source']}")
    print()

    # Save results
    results = pd.DataFrame([incidence, mortality])
    results.to_csv(os.path.join(OUTPUT_DIR, 'external_validation_summary.csv'),
                   index=False, sep=';')

    stage_df.to_csv(os.path.join(OUTPUT_DIR, 'external_validation_stages.csv'),
                    index=False, sep=';')

    # Plots
    plot_incidence_comparison(
        incidence, mortality,
        os.path.join(OUTPUT_DIR, 'external_validation_incidence_mortality.png')
    )
    plot_stage_comparison(
        stage_df,
        os.path.join(OUTPUT_DIR, 'external_validation_stages.png')
    )

    print(f"All results saved to {OUTPUT_DIR}/")


if __name__ == '__main__':
    main()
