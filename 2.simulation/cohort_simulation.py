"""
Closed-Cohort Benchmarking Simulation for MiCSS.

Follows 1,000 individuals from age 40 to death with no births or immigration,
matching the CISNET methodology for direct comparison with MISCAN-Colon,
SimCRC, and CRC-SPIN published benchmarks.
"""
from random import uniform, seed
import numpy as np
from person import Person
from parameters import (
    CANCER_TREATMENT_COSTS, FIT_SENSITIVITY, FIT_SPECIFICITY,
    SEED, FIT_COST, COLONOSCOPY_COST, SCREENING_FREQUENCY, CRC_PREVALENCE,
    POLYPECTOMY_PREVENTION_RATE,
)


class CohortSimulation:

    def __init__(self, cohort_size: int = 1000, adherence: float = 1.0,
                 screening: bool = True) -> None:
        self.cohort_size = cohort_size
        self.adherence = adherence
        self.screening = screening

        self.seed = SEED
        self.cancer_treatment_costs = CANCER_TREATMENT_COSTS
        self.screening_frequency = SCREENING_FREQUENCY
        self.colonoscopy_cost = COLONOSCOPY_COST
        self.fit_cost = FIT_COST
        self.fit_sensitivity = FIT_SENSITIVITY
        self.fit_specificity = FIT_SPECIFICITY
        self.crc_prevalence = CRC_PREVALENCE
        self.polypectomy_prevention_rate = POLYPECTOMY_PREVENTION_RATE

        self.starting_age = 40
        self.starting_year = 2023

        self._reset_accumulators()

    def _reset_accumulators(self) -> None:
        self.total_lyg = 0
        self.total_dalys = 0
        self.total_fits = 0
        self.total_colonoscopies = 0
        self.total_true_positives = 0
        self.total_false_positives = 0
        self.total_symptomatic_treatments = 0
        self.total_asymptomatic_treatments = 0
        self.total_polypectomies = 0
        self.total_deaths = 0
        self.total_cancer_deaths = 0
        self.total_stage_treatments = {'I': 0, 'II': 0, 'III': 0, 'IV': 0}
        self.total_fit_cost = 0
        self.total_colonoscopy_cost = 0
        self.total_cancer_treatment_cost = 0

    def _screenable_age(self, age: int) -> bool:
        freq = self.screening_frequency
        return (age >= freq[1] and age <= freq[2]
                and (age + freq[4]) % freq[3] == 0)

    def simulate(self) -> dict:
        self._reset_accumulators()

        effective_adherence = self.adherence if self.screening else 0.0

        cohort: list[Person] = []
        for i in range(self.cohort_size):
            p = Person(self.starting_age, self.starting_year,
                       effective_adherence, i, self.crc_prevalence)
            cohort.append(p)

        year = self.starting_year
        while any(p.alive for p in cohort):
            seed(year)
            np.random.seed(year)

            for person in cohort:
                if not person.alive:
                    continue
                self._process_person(person)

            cohort = [p for p in cohort if p.alive]
            year += 1

            if year - self.starting_year > 120:
                for p in cohort:
                    p.die()
                break

        return self._build_results()

    def _process_person(self, person: Person) -> None:
        if person.will_develop_cancer and not person.treated_cancer:
            if person.age >= person.age_of_symptomatic_cancer:
                person.treat_cancer()
                self.total_symptomatic_treatments += 1
                self._count_stage_treatment(person.symptomatic_cancer_stage)
                self.total_cancer_treatment_cost += self.cancer_treatment_costs.get(
                    person.symptomatic_cancer_stage, 0)
            elif person.age == person.age_of_screenable_cancer:
                person.detectable_cancer = True

            if (self.screening and person.screenable
                    and self._screenable_age(person.age)):
                self.total_fits += 1
                self.total_fit_cost += self.fit_cost
                if person.detectable_cancer:
                    if uniform(0, 1) < self.fit_sensitivity:
                        self.total_true_positives += 1
                        self.total_colonoscopies += 1
                        self.total_colonoscopy_cost += self.colonoscopy_cost

                        if uniform(0, 1) < self.polypectomy_prevention_rate:
                            person.revert_to_natural_death()
                            self.total_polypectomies += 1
                        else:
                            person.treat_cancer()
                            lyg, _, _, daly = person.asymptomatic_screening()
                            self.total_lyg += lyg
                            self.total_dalys += daly
                            self.total_asymptomatic_treatments += 1
                            self._count_stage_treatment(person.asymptomatic_cancer_stage)
                            self.total_cancer_treatment_cost += self.cancer_treatment_costs.get(
                                person.asymptomatic_cancer_stage, 0)
                else:
                    if uniform(0, 1) > self.fit_specificity:
                        self.total_false_positives += 1
                        self.total_colonoscopies += 1
                        self.total_colonoscopy_cost += self.colonoscopy_cost

        elif not person.will_develop_cancer:
            if (self.screening and person.screenable
                    and self._screenable_age(person.age)):
                self.total_fits += 1
                self.total_fit_cost += self.fit_cost
                if uniform(0, 1) > self.fit_specificity:
                    self.total_false_positives += 1
                    self.total_colonoscopies += 1
                    self.total_colonoscopy_cost += self.colonoscopy_cost

        if person.age >= person.age_of_death:
            person.die()
            self.total_deaths += 1
            if person.cancer_determined_death:
                self.total_cancer_deaths += 1
        else:
            person.age += 1

    def _count_stage_treatment(self, stage: str) -> None:
        if stage in self.total_stage_treatments:
            self.total_stage_treatments[stage] += 1

    def _build_results(self) -> dict:
        n = self.cohort_size
        total_cost = (self.total_fit_cost + self.total_colonoscopy_cost
                      + self.total_cancer_treatment_cost)
        return {
            'cohort_size': n,
            'screening': self.screening,
            'adherence': self.adherence,
            'total_lyg': self.total_lyg,
            'lyg_per_1000': round(self.total_lyg * 1000 / n, 2),
            'total_dalys': self.total_dalys,
            'dalys_per_1000': round(self.total_dalys * 1000 / n, 2),
            'total_fits': self.total_fits,
            'fits_per_1000': round(self.total_fits * 1000 / n, 2),
            'total_colonoscopies': self.total_colonoscopies,
            'colonoscopies_per_1000': round(self.total_colonoscopies * 1000 / n, 2),
            'total_cancer_deaths': self.total_cancer_deaths,
            'cancer_deaths_per_1000': round(self.total_cancer_deaths * 1000 / n, 2),
            'total_deaths': self.total_deaths,
            'total_symptomatic_treatments': self.total_symptomatic_treatments,
            'total_asymptomatic_treatments': self.total_asymptomatic_treatments,
            'total_polypectomies': self.total_polypectomies,
            'stage_treatments': dict(self.total_stage_treatments),
            'total_cost': total_cost,
            'cost_per_person': round(total_cost / n, 2),
            'total_fit_cost': self.total_fit_cost,
            'total_colonoscopy_cost': self.total_colonoscopy_cost,
            'total_cancer_treatment_cost': self.total_cancer_treatment_cost,
        }


if __name__ == '__main__':
    import time

    print('=== Closed-Cohort Simulation (1,000 from age 40) ===\n')

    t0 = time.time()
    screening_sim = CohortSimulation(cohort_size=1000, adherence=1.0, screening=True)
    screening_results = screening_sim.simulate()
    print(f'Screening cohort done in {int(time.time() - t0)}s')

    t0 = time.time()
    baseline_sim = CohortSimulation(cohort_size=1000, adherence=0.0, screening=False)
    baseline_results = baseline_sim.simulate()
    print(f'Baseline cohort done in {int(time.time() - t0)}s')

    print(f'\n--- Results per 1,000 individuals ---')
    print(f'{"Metric":<35} {"Screening":>12} {"No Screening":>14} {"Difference":>12}')
    print('-' * 75)
    for key, label in [
        ('lyg_per_1000', 'LYG per 1,000'),
        ('dalys_per_1000', 'DALYs gained per 1,000'),
        ('fits_per_1000', 'FITs per 1,000'),
        ('colonoscopies_per_1000', 'Colonoscopies per 1,000'),
        ('cancer_deaths_per_1000', 'CRC deaths per 1,000'),
        ('cost_per_person', 'Cost per person (CLP)'),
    ]:
        s = screening_results[key]
        b = baseline_results[key]
        diff = round(s - b, 2)
        print(f'{label:<35} {s:>12} {b:>14} {diff:>12}')
