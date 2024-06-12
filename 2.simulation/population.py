import pandas as pd
import json
from random import uniform, randint, choices, seed
import numpy as np
from person import Person
from parameters import CANCER_TREATMENT_COSTS, FIT_SENSITIVITY, FIT_SPECIFICITY, SEED, FIT_COST, COLONOSCOPY_COST, YEARS_TO_SIMULATE, STARTING_YEAR, SCREENING_FREQUENCY, CRC_PREVALENCE
initial_population = pd.read_csv('1.processed_data/initial_population.csv', sep=';', encoding='utf-8', low_memory=False)
# Convert initial_population into a dictionary
initial_population_dict = {}
for row in initial_population.iterrows():
    initial_population_dict[row[1]['Edad']] = [row[1]['Edad'], row[1]['Inscritos'], row[1]['Ratio']]

import os



class Population():

    def __init__(self, adherence_percentage, folder_name):
        
        self.seed = SEED
        self.cancer_treatment_costs = CANCER_TREATMENT_COSTS
        self.screening_frequency = SCREENING_FREQUENCY
        self.colonoscopy_cost = COLONOSCOPY_COST
        self.fit_cost = FIT_COST
        self.crc_prevalence = CRC_PREVALENCE
        self.years_to_simulate = YEARS_TO_SIMULATE
        self.starting_year = STARTING_YEAR
        self.year = STARTING_YEAR
        self.fit_sensitivity = FIT_SENSITIVITY
        self.fit_specificity = FIT_SPECIFICITY

        

        self.counter = 0
        self.folder_name = folder_name
        self.population = []
        
        self.adherence_percentage = adherence_percentage

        #self.simulate()



    # Starts the simulation
    def simulate(self):
        for i in range(110):
            year_of_inscription = self.year
            for j in range(int(initial_population_dict[i][1])):
                self.population.append(Person(i, year_of_inscription, self.adherence_percentage, self.counter, self.crc_prevalence))
                self.counter += 1
         
        self.census = pd.DataFrame([[i, 0] for i in range(120)], columns=['Edad', str(self.year)])
        self.census = pd.concat([self.census, pd.DataFrame(np.zeros((len(self.census), self.years_to_simulate), dtype=int), columns=[str(self.year + i) for i in range(self.years_to_simulate)])], axis=1)
        
        self.population_stats = pd.DataFrame(columns=['Year', 'Total', 'Births', 'Deaths', 'DeathsByCancer', '50-75', 'HaveCancer', 'Screened', 'TruePositives', 'FalsePositives'])
        
        self.costs = pd.DataFrame(columns=['Year', 'Fit', 'Colonoscopy', 'CancerStageITreatments', 'CancerStageIITreatments', 'CancerStageIIITreatments', 'CancerStageIVTreatments', 'CancerStageI', 'CancerStageII', 'CancerStageIII', 'CancerStageIV', 'Cancer Treatments', 'Cancer Treatments Costs', 'Total'])

        for i in range(self.years_to_simulate):
            self.next_year()
    
        self.finalizar()

    def cost_center(self):
        cancer_treatments = self.yearly_stage_I_treatments + self.yearly_stage_II_treatments + self.yearly_stage_III_treatments + self.yearly_stage_IV_treatments
        fit = round(self.yearly_screened)
        colonoscopy = round(self.yearly_colonoscopies)
        yearly_fit_cost = round(self.yearly_screened * self.fit_cost / 1000000)
        yearly_colonoscopy_cost = round(self.yearly_colonoscopies * self.colonoscopy_cost / 1000000)
        cancer_stage_I_cost = round(self.yearly_stage_I_treatments * self.cancer_treatment_costs['I'] / 1000000)
        cancer_stage_II_cost = round(self.yearly_stage_II_treatments * self.cancer_treatment_costs['II'] / 1000000)
        cancer_stage_III_cost = round(self.yearly_stage_III_treatments * self.cancer_treatment_costs['III'] / 1000000)
        cancer_stage_IV_cost = round(self.yearly_stage_IV_treatments * self.cancer_treatment_costs['IV'] / 1000000)
        total_cancer_treatment_costs = round(cancer_stage_I_cost + cancer_stage_II_cost + cancer_stage_III_cost + cancer_stage_IV_cost)
        total_cost = yearly_fit_cost + yearly_colonoscopy_cost + cancer_stage_I_cost + cancer_stage_II_cost + cancer_stage_III_cost + cancer_stage_IV_cost
        self.costs = pd.concat(
            [self.costs, 
            pd.DataFrame([[self.year, fit, colonoscopy, yearly_fit_cost, yearly_colonoscopy_cost, self.yearly_stage_I_treatments, self.yearly_stage_II_treatments, self.yearly_stage_III_treatments, self.yearly_stage_IV_treatments, cancer_stage_I_cost, cancer_stage_II_cost, cancer_stage_III_cost, cancer_stage_IV_cost, cancer_treatments, total_cancer_treatment_costs, total_cost, self.expectancy_years_gained, self.healthy_expectancy_years_gained, self.disability_free_expectancy_years_gained, self.daly_gained ,self.asymptomatic_ccr_discovered]],
            columns=['Year', 'Fit', 'Colonoscopy', 'Fit Costs', 'Colonoscopy Costs', 'CancerStageITreatments', 'CancerStageIITreatments', 'CancerStageIIITreatments', 'CancerStageIVTreatments', 'CancerStageI', 'CancerStageII', 'CancerStageIII', 'CancerStageIV', 'Cancer Treatments', 'Cancer Treatments Costs', 'Total', 'YearsGained', 'HYearsGained', 'DFYearsGained', 'DALYGained', 'AsymtomaticCCRDiscovered'])], 
            ignore_index=True
            )
        
    def next_year(self):
        seed(self.year)
        conteo_poblacion = {}
        print('='*5, 'ADH', str(self.adherence_percentage) + '%', '='*5,'Año' , self.year, '='*5)
        poblacion_inicial = len(self.population)
        births = round(np.random.normal(9000, 500))
        births2 = round(np.random.normal(3200, 300))
        births3 = round(np.random.normal(1800, 300))
        self.yearly_deaths = 0
        self.yearly_cancer_deaths = 0
        self.yearly_people_with_cancer = 0
        self.yearly_screened = 0
        self.yearly_colonoscopies = 0
        self.yearly_true_positives = 0
        self.yearly_false_positives = 0
        self.yearly_symptomatic_cancer_treatments = 0
        self.yearly_asymptomatic_cancer_treatments = 0
        self.yearly_stage_I_treatments = 0
        self.yearly_stage_II_treatments = 0
        self.yearly_stage_III_treatments = 0
        self.yearly_stage_IV_treatments = 0
        self.expectancy_years_gained = 0
        self.healthy_expectancy_years_gained = 0
        self.disability_free_expectancy_years_gained = 0
        self.daly_gained = 0
        self.asymptomatic_ccr_discovered = 0
        # Count the population by age
        for i in self.population:
            conteo_poblacion[i.age] = conteo_poblacion.get(i.age, 0) + 1
            
        

        #self.census[self.year] = self.census['Edad'].apply(lambda x: conteo_poblacion.get(x, 0))

        # Update the column of the year in the dataframe
        self.census[str(self.year)] = self.census['Edad'].apply(lambda x: conteo_poblacion.get(x, 0))


        # Process every person in the population
        for i in range(len(self.population)):
            self.procesar_persona(i)
        
        poblacion50_75 = len([i for i in self.population if i.age >= 50 and i.age <= 75])
        
        self.population_stats = pd.concat(
            [self.population_stats, 
            pd.DataFrame([[self.year, len(self.population), births + births2 + births3, self.yearly_deaths, self.yearly_cancer_deaths, poblacion50_75, self.yearly_people_with_cancer, self.yearly_screened, self.yearly_true_positives, self.yearly_false_positives, self.yearly_symptomatic_cancer_treatments, self.yearly_asymptomatic_cancer_treatments, self.yearly_stage_I_treatments, self.yearly_stage_II_treatments, self.yearly_stage_III_treatments, self.yearly_stage_IV_treatments, self.expectancy_years_gained, self.healthy_expectancy_years_gained, self.disability_free_expectancy_years_gained, self.daly_gained, self.asymptomatic_ccr_discovered]], 
            columns=['Year', 'Total', 'Births', 'Deaths', 'DeathsByCancer', '50-75', 'HaveCancer', 'Screened', 'TruePositives', 'FalsePositives', 'SymptomaticTreatments', 'AsymptomaticTreatments', 'StageITreatments', 'StageIITreatments', 'StageIIITreatments', 'StageIVTreatments', 'YearsGained', 'HYearsGained', 'DFYearsGained', 'DALYGained', 'AsymtomaticCCRDiscovered'])], 
            ignore_index=True
            )
        
        self.population = [i for i in self.population if i.alive]

        # Add the new people to the population
        for i in range(births):
            self.population.append(Person(0, self.year, self.adherence_percentage, self.counter, self.crc_prevalence))
            self.counter += 1
        for i in range(births2):
            self.population.append(Person(randint(1,8), self.year, self.adherence_percentage, self.counter, self.crc_prevalence))
            self.counter += 1
        for i in range(births3):
            self.population.append(Person(randint(21,30), self.year, self.adherence_percentage, self.counter, self.crc_prevalence))
            self.counter += 1
        poblacion_final = len(self.population)
        self.cost_center()
        self.year += 1
        
    
    def procesar_persona(self, person_index):
        person = self.population[person_index]

        # Count all people who have cancer
        if person.will_develop_cancer == True and person.treated_cancer == False and person.detectable_cancer == True:
            self.yearly_people_with_cancer += 1

        # Manage people who will have cancer
        if person.will_develop_cancer == True:

            # Pass on people who have already been treated for cancer
            if person.treated_cancer:
                pass
            # Manage people who have not been treated for cancer
            else:
                # Manage people who developed symptomatic cancer
                if person.age >= person.age_of_symptomatic_cancer:
                    person.treat_cancer()
                    self.yearly_symptomatic_cancer_treatments += 1
                    if person.symptomatic_cancer_stage == 'I':
                            self.yearly_stage_I_treatments += 1
                    elif person.symptomatic_cancer_stage == 'II':
                        self.yearly_stage_II_treatments += 1
                    elif person.symptomatic_cancer_stage == 'III':
                        self.yearly_stage_III_treatments += 1
                    elif person.symptomatic_cancer_stage == 'IV':
                        self.yearly_stage_IV_treatments += 1
                    else:
                        print('YIYIIIIIIIIII')
                # Manage people who developed preclinical cancer
                elif person.age == person.age_of_screenable_cancer:
                    person.detectable_cancer = True
        

                # Screen all people between 50 and 75 who will allow it
                if person.screenable == True and self.screenable(person.age) == True:
                    self.yearly_screened += 1
                    # If their CRC is detectable
                    if person.detectable_cancer == True:
                        if uniform(0,1) < self.fit_sensitivity:
                            person.treat_cancer()
                            years_gained, healthy_years_gained, disability_free_years_gained, daly_gained = person.asymptomatic_screening()
                            self.expectancy_years_gained += years_gained
                            self.healthy_expectancy_years_gained += healthy_years_gained
                            self.disability_free_expectancy_years_gained += disability_free_years_gained
                            self.daly_gained += daly_gained
                            self.asymptomatic_ccr_discovered += 1
                            self.yearly_true_positives += 1
                            self.yearly_colonoscopies += 1
                            self.yearly_asymptomatic_cancer_treatments += 1
                            if person.asymptomatic_cancer_stage == 'I':
                                self.yearly_stage_I_treatments += 1
                            elif person.asymptomatic_cancer_stage == 'II':
                                self.yearly_stage_II_treatments += 1
                            elif person.asymptomatic_cancer_stage == 'III':
                                self.yearly_stage_III_treatments += 1
                            elif person.asymptomatic_cancer_stage == 'IV':
                                self.yearly_stage_IV_treatments += 1
                            else:
                                print('GGGGGGGGGGGGGGG')
                    # If their CRC is still not detectable
                    else:
                        self.yearly_screened += 1
                        if uniform(0,1) > self.fit_specificity:
                            self.yearly_false_positives += 1
                            self.yearly_colonoscopies += 1
        
        # Manage people who will not have cancer
        else:
            # Screen all people between 50 and 75 who will allow it
            if person.screenable == True and self.screenable(person.age) == True:
                self.yearly_screened += 1
                if uniform(0,1) > self.fit_specificity:
                    self.yearly_false_positives += 1
                    self.yearly_colonoscopies += 1


        # Check if the person will die
        if person.age == person.age_of_death:
            person.die()
            self.yearly_deaths += 1
            if person.will_develop_cancer:
                self.yearly_cancer_deaths += 1
        elif person.age >= person.age_of_death:
            person.die()
            self.yearly_deaths += 1
            print('hiihihiihihihih', person.age, person.age_of_death, person.will_develop_cancer, person.treated_cancer, person.prueba)
            if person.will_develop_cancer:
                print('Troleaste')
                self.yearly_cancer_deaths += 1
        elif person.age > 119 and person.alive == True:
            print('JEJAZOOOOOOOOOOOO', person.age, person.age_of_death, person.year_of_birth, person.will_develop_cancer)
            person.die()
            self.yearly_deaths += 1
            if person.will_develop_cancer:
                self.yearly_cancer_deaths += 1
        else:
            person.age += 1

    def screenable(self, age):
        if age >= self.screening_frequency[1] and age <= self.screening_frequency[2] and (age + self.screening_frequency[4]) % self.screening_frequency[3] == 0:
            return True
        return False

    def finalizar(self):
        parameters = {
            'SEED': self.seed,
            'CANCER_TREATMENT_COSTS': self.cancer_treatment_costs,
            'SCREENING_FREQUENCY': self.screening_frequency,
            'COLONOSCOPY_COST': self.colonoscopy_cost,
            'FIT_COST': self.fit_cost,
            'CRC_PREVALENCE': self.crc_prevalence,
            'YEARS_TO_SIMULATE': self.years_to_simulate,
            'STARTING_YEAR': self.starting_year,
            'FIT_SENSITIVITY': self.fit_sensitivity,
            'FIT_SPECIFICITY': self.fit_specificity
        }

        if not os.path.exists('4.simulation_outputs/' + self.folder_name):
            os.makedirs('4.simulation_outputs/' + self.folder_name)
            os.makedirs('4.simulation_outputs/' + self.folder_name + '/censo')
            os.makedirs('4.simulation_outputs/' + self.folder_name + '/population_stats')
            os.makedirs('4.simulation_outputs/' + self.folder_name + '/costs')
            os.makedirs('4.simulation_outputs/' + self.folder_name + '/parameters')
        else:
            print('It already exists')
        self.census.to_csv('4.simulation_outputs/' + self.folder_name + '/censo/censo' + '_'.join(str(self.adherence_percentage).split('.')) + '.csv', index=False, header=True, sep=';')
        self.population_stats.to_csv('4.simulation_outputs/' + self.folder_name + '/population_stats/population_stats' + '_'.join(str(self.adherence_percentage).split('.')) + '.csv', index=False, header=True, sep=';')
        self.costs.to_csv('4.simulation_outputs/' + self.folder_name + '/costs/costs_' + '_'.join(str(self.adherence_percentage).split('.')) + '.csv', index=False, header=True, sep=';')
        with open('4.simulation_outputs/' + self.folder_name + '/parameters/simulation_parameters.json', 'w') as file:
                json.dump(parameters, file, indent=4)