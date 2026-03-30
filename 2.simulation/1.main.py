import os
import time

from population import Population

ADHERENCE_LIST = [0, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8]

SCENARIOS = [
    # Defaults (use adherence list)
    {"folder": "default"},
    {"folder": "default200", "overrides": {"years_to_simulate": 200}},
    {"folder": "default_1"},
    {"folder": "default_2"},
    {"folder": "default_3"},
    {"folder": "default_4"},
    {"folder": "default_5"},
    {"folder": "default_6"},
    {"folder": "default_7"},
    {"folder": "default_8"},
    {"folder": "default_9"},
    {"folder": "default_10"},
    # I. Screening Frequency (single adherence 0.8, 200 years)
    {"folder": "1year", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Annual", 50, 75, 1, 0]}},
    {"folder": "2year", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 50, 75, 2, 0]}},
    {"folder": "3year", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Triennial", 50, 75, 3, 1]}},
    {"folder": "4year", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Quadrennial", 50, 75, 4, 2]}},
    {"folder": "5year", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Quinquennial", 50, 75, 5, 0]}},
    # II. Intervals - first round
    {"folder": "interval50_75", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 50, 75, 2, 0]}},
    {"folder": "interval45_80", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 45, 80, 2, 1]}},
    {"folder": "interval40_85", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 40, 85, 2, 0]}},
    {"folder": "interval35_90", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 35, 90, 2, 1]}},
    # III. Intervals - second round
    {"folder": "interval45_75", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 45, 75, 2, 1]}},
    {"folder": "interval40_75", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 40, 75, 2, 0]}},
    {"folder": "interval50_80", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 50, 80, 2, 0]}},
    {"folder": "interval50_85", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 50, 85, 2, 0]}},
    {"folder": "interval40_80", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 40, 80, 2, 0]}},
    {"folder": "interval35_80", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 35, 80, 2, 1]}},
    {"folder": "interval45_85", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 45, 85, 2, 1]}},
    {"folder": "interval55_75", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 55, 75, 2, 1]}},
    {"folder": "interval50_70", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 50, 70, 2, 0]}},
    {"folder": "interval60_75", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 60, 75, 2, 0]}},
    {"folder": "interval55_80", "adherence": 0.8, "overrides": {"years_to_simulate": 200, "screening_frequency": ["Biennial", 55, 80, 2, 1]}},
    # IV. Colonoscopy Costs
    {"folder": "colonoscopy_421005", "adherence": 0.8, "overrides": {"colonoscopy_cost": 421005}},
    {"folder": "colonoscopy_504205", "adherence": 0.8, "overrides": {"colonoscopy_cost": 504205}},
    {"folder": "colonoscopy_425621", "adherence": 0.8, "overrides": {"colonoscopy_cost": 425621}},
    {"folder": "colonoscopy_333190", "adherence": 0.8, "overrides": {"colonoscopy_cost": 333190}},
    # V. FIT Sensitivity
    {"folder": "improved_sensitivity", "adherence": 0.8, "overrides": {"fit_sensitivity": 0.85}},
    {"folder": "worse_sensitivity", "adherence": 0.8, "overrides": {"fit_sensitivity": 0.73}},
    # VI. FIT Specificity
    {"folder": "improved_specificity", "adherence": 0.8, "overrides": {"fit_specificity": 0.96}},
    {"folder": "worse_specificity", "adherence": 0.8, "overrides": {"fit_specificity": 0.92}},
    {"folder": "super_improved_specificity", "adherence": 0.8, "overrides": {"fit_specificity": 0.999}},
    # VII. FIT Costs
    {"folder": "fit_5865", "adherence": 0.8, "overrides": {"fit_cost": 5865}},
    {"folder": "fit_4865", "adherence": 0.8, "overrides": {"fit_cost": 4865}},
    {"folder": "fit_3865", "adherence": 0.8, "overrides": {"fit_cost": 3865}},
    {"folder": "fit_6865", "adherence": 0.8, "overrides": {"fit_cost": 6865}},
    {"folder": "fit_2865", "adherence": 0.8, "overrides": {"fit_cost": 2865}},
]


def run_scenario(config: dict, adherence_list: list[float]) -> None:
    folder = config["folder"]
    if os.path.exists(f"4.simulation_outputs/{folder}"):
        print(f"Skipping '{folder}' — output already exists")
        return

    adherence_spec = config.get("adherence", "list")
    adherence_values = adherence_list if adherence_spec == "list" else [adherence_spec]
    overrides = config.get("overrides", {})

    for adherence in adherence_values:
        t0 = time.time()
        pop = Population(adherence, folder)
        for attr, value in overrides.items():
            setattr(pop, attr, value)
        pop.simulate()
        elapsed = int(time.time() - t0)
        print(f"  [{folder}] adherence={adherence} done in {elapsed}s")


if __name__ == "__main__":
    total_start = time.time()
    for scenario in SCENARIOS:
        run_scenario(scenario, ADHERENCE_LIST)
    total_elapsed = int((time.time() - total_start) / 60)
    print(f"All scenarios finished in {total_elapsed} minutes")
