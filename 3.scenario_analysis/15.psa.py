"""
Probabilistic Sensitivity Analysis (PSA) for MiCSS.

Samples model parameters from probability distributions and runs the full
20-year simulation for each draw. Produces:
  - CE scatter plot (incremental cost vs incremental DALYs averted)
  - Cost-Effectiveness Acceptability Curve (CEAC)
  - Summary statistics (mean, 2.5th, 97.5th percentile)
  - CSV of all iteration results

Runtime: ~1,000 iterations x 20s = ~5.5 hours.
Includes periodic checkpointing so runs can be resumed.
"""
import sys
import os
import time
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '2.simulation'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from population import Population

OUTPUT_DIR = 'validation'
CHECKPOINT_FILE = os.path.join(OUTPUT_DIR, 'psa_checkpoint.csv')
RESULTS_FILE = os.path.join(OUTPUT_DIR, 'psa_results.csv')
CHECKPOINT_INTERVAL = 10

N_ITERATIONS = 1000
YEARS_TO_SIMULATE = 20
ADHERENCE = 0.15

# ---- Parameter distributions ----
# Beta(a, b) parameterized from mean and sample size (a + b)
# Gamma parameterized from mean and CV (coefficient of variation)


def beta_params(mean: float, n: float) -> tuple[float, float]:
    """Return alpha, beta for a Beta distribution with given mean and sample size."""
    a = mean * n
    b = (1 - mean) * n
    return a, b


def gamma_params(mean: float, cv: float) -> tuple[float, float]:
    """Return shape, scale for a Gamma distribution with given mean and CV."""
    shape = 1.0 / (cv ** 2)
    scale = mean * (cv ** 2)
    return shape, scale


PARAM_DISTS = {
    'fit_sensitivity': {'dist': 'beta', **dict(zip(['a', 'b'], beta_params(0.79, 200)))},
    'fit_specificity': {'dist': 'beta', **dict(zip(['a', 'b'], beta_params(0.94, 500)))},
    'crc_prevalence': {'dist': 'beta', **dict(zip(['a', 'b'], beta_params(0.042, 5000)))},
    'fit_cost': {'dist': 'gamma', **dict(zip(['shape', 'scale'], gamma_params(5865, 0.20)))},
    'colonoscopy_cost': {'dist': 'gamma', **dict(zip(['shape', 'scale'], gamma_params(421005, 0.20)))},
    'cancer_cost_I': {'dist': 'gamma', **dict(zip(['shape', 'scale'], gamma_params(8644 * 879.56, 0.20)))},
    'cancer_cost_II': {'dist': 'gamma', **dict(zip(['shape', 'scale'], gamma_params(12765.2 * 879.56, 0.20)))},
    'cancer_cost_III': {'dist': 'gamma', **dict(zip(['shape', 'scale'], gamma_params(13075.2 * 879.56, 0.20)))},
    'cancer_cost_IV': {'dist': 'gamma', **dict(zip(['shape', 'scale'], gamma_params(51333.5 * 879.56, 0.20)))},
}


def sample_params(rng: np.random.Generator) -> dict:
    """Draw one set of parameters from their distributions."""
    params = {}
    for name, spec in PARAM_DISTS.items():
        if spec['dist'] == 'beta':
            params[name] = rng.beta(spec['a'], spec['b'])
        elif spec['dist'] == 'gamma':
            params[name] = rng.gamma(spec['shape'], spec['scale'])
    return params


def run_iteration(iteration: int, params: dict) -> dict:
    """Run screening and baseline simulations with the given parameters."""
    screening_pop = Population(ADHERENCE, f'psa_screen_{iteration}')
    screening_pop.years_to_simulate = YEARS_TO_SIMULATE
    screening_pop.fit_sensitivity = params['fit_sensitivity']
    screening_pop.fit_specificity = params['fit_specificity']
    screening_pop.crc_prevalence = params['crc_prevalence']
    screening_pop.fit_cost = round(params['fit_cost'])
    screening_pop.colonoscopy_cost = round(params['colonoscopy_cost'])
    screening_pop.cancer_treatment_costs = {
        'I': round(params['cancer_cost_I']),
        'II': round(params['cancer_cost_II']),
        'III': round(params['cancer_cost_III']),
        'IV': round(params['cancer_cost_IV']),
    }
    screening_pop.simulate()

    baseline_pop = Population(0.0, f'psa_base_{iteration}')
    baseline_pop.years_to_simulate = YEARS_TO_SIMULATE
    baseline_pop.fit_sensitivity = params['fit_sensitivity']
    baseline_pop.fit_specificity = params['fit_specificity']
    baseline_pop.crc_prevalence = params['crc_prevalence']
    baseline_pop.fit_cost = round(params['fit_cost'])
    baseline_pop.colonoscopy_cost = round(params['colonoscopy_cost'])
    baseline_pop.cancer_treatment_costs = screening_pop.cancer_treatment_costs
    baseline_pop.simulate()

    screen_total_cost = sum(r['Total'] for r in screening_pop._costs_rows)
    base_total_cost = sum(r['Total'] for r in baseline_pop._costs_rows)
    screen_dalys = sum(r['DALYGained'] for r in screening_pop._costs_rows)
    screen_lyg = sum(r['YearsGained'] for r in screening_pop._costs_rows)
    base_dalys = sum(r['DALYGained'] for r in baseline_pop._costs_rows)
    base_lyg = sum(r['YearsGained'] for r in baseline_pop._costs_rows)

    incremental_cost = screen_total_cost - base_total_cost
    incremental_dalys = screen_dalys - base_dalys
    incremental_lyg = screen_lyg - base_lyg

    return {
        'iteration': iteration,
        'incremental_cost_millions': round(incremental_cost, 4),
        'incremental_dalys': incremental_dalys,
        'incremental_lyg': incremental_lyg,
        'icer_dalys': round(incremental_cost / incremental_dalys, 2) if incremental_dalys != 0 else float('inf'),
        'screen_total_cost': screen_total_cost,
        'base_total_cost': base_total_cost,
        'screen_dalys': screen_dalys,
        'base_dalys': base_dalys,
        **{f'param_{k}': round(v, 6) for k, v in params.items()},
    }


def _suppress_population_output(pop: Population) -> None:
    """Override finalize to skip file I/O during PSA runs."""
    pop.costs = pd.DataFrame(pop._costs_rows)
    pop.population_stats = pd.DataFrame(pop._stats_rows)


def load_checkpoint() -> list[dict]:
    """Load previously completed iterations from checkpoint file."""
    if os.path.exists(CHECKPOINT_FILE):
        df = pd.read_csv(CHECKPOINT_FILE, sep=';')
        return df.to_dict('records')
    return []


def save_checkpoint(results: list[dict]) -> None:
    pd.DataFrame(results).to_csv(CHECKPOINT_FILE, index=False, sep=';')


def plot_ce_scatter(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(df['incremental_dalys'], df['incremental_cost_millions'],
               alpha=0.3, s=10, color='steelblue')
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlabel('Incremental DALYs Averted')
    ax.set_ylabel('Incremental Cost (Millions CLP)')
    ax.set_title('Cost-Effectiveness Plane (PSA)')
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'psa_ce_scatter.png'), dpi=150)
    plt.close(fig)
    print(f'  Saved: {OUTPUT_DIR}/psa_ce_scatter.png')


def plot_ceac(df: pd.DataFrame) -> None:
    """Cost-Effectiveness Acceptability Curve across WTP thresholds."""
    wtp_range = np.linspace(0, 50, 200)
    probabilities = []
    for wtp in wtp_range:
        cost_effective = (df['incremental_cost_millions'] <= wtp * df['incremental_dalys']).mean()
        probabilities.append(cost_effective)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(wtp_range, probabilities, color='steelblue', linewidth=2)
    ax.set_xlabel('Willingness-to-Pay (Millions CLP per DALY averted)')
    ax.set_ylabel('Probability Cost-Effective')
    ax.set_title('Cost-Effectiveness Acceptability Curve (CEAC)')
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, 'psa_ceac.png'), dpi=150)
    plt.close(fig)
    print(f'  Saved: {OUTPUT_DIR}/psa_ceac.png')


def print_summary(df: pd.DataFrame) -> None:
    print('\n--- PSA Summary Statistics ---\n')
    for col, label in [
        ('incremental_cost_millions', 'Incremental Cost (M CLP)'),
        ('incremental_dalys', 'Incremental DALYs'),
        ('incremental_lyg', 'Incremental LYG'),
        ('icer_dalys', 'ICER (M CLP / DALY)'),
    ]:
        finite = df[col].replace([np.inf, -np.inf], np.nan).dropna()
        if len(finite) == 0:
            continue
        print(f'{label}:')
        print(f'  Mean:   {finite.mean():>14.2f}')
        print(f'  Median: {finite.median():>14.2f}')
        print(f'  2.5%:   {finite.quantile(0.025):>14.2f}')
        print(f'  97.5%:  {finite.quantile(0.975):>14.2f}')
        print()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    _patch_finalize()

    rng = np.random.default_rng(seed=42)

    existing = load_checkpoint()
    completed_iters = {r['iteration'] for r in existing}
    results = list(existing)

    remaining = [i for i in range(N_ITERATIONS) if i not in completed_iters]
    print(f'\n=== PSA: {N_ITERATIONS} iterations, {len(remaining)} remaining ===\n')

    total_start = time.time()
    for idx, iteration in enumerate(remaining):
        t0 = time.time()
        params = sample_params(rng)
        result = run_iteration(iteration, params)
        results.append(result)
        elapsed = int(time.time() - t0)
        total_elapsed = int(time.time() - total_start)
        avg_per_iter = total_elapsed / (idx + 1)
        eta = int(avg_per_iter * (len(remaining) - idx - 1))
        print(f'  [{iteration+1}/{N_ITERATIONS}] {elapsed}s  '
              f'(total: {total_elapsed}s, ETA: {eta//3600}h{(eta%3600)//60}m)')

        if (idx + 1) % CHECKPOINT_INTERVAL == 0:
            save_checkpoint(results)
            print(f'  Checkpoint saved ({len(results)} iterations)')

    save_checkpoint(results)

    df = pd.DataFrame(results)
    df.to_csv(RESULTS_FILE, index=False, sep=';')
    print(f'\nAll results saved to: {RESULTS_FILE}')

    print_summary(df)
    plot_ce_scatter(df)
    plot_ceac(df)


def _patch_finalize():
    """Monkey-patch Population.finalize to skip file I/O during PSA."""
    original_finalize = Population.finalize

    def psa_finalize(self):
        if self.folder_name.startswith('psa_'):
            self.costs = pd.DataFrame(self._costs_rows)
            self.population_stats = pd.DataFrame(self._stats_rows)
        else:
            original_finalize(self)

    Population.finalize = psa_finalize


if __name__ == '__main__':
    main()
