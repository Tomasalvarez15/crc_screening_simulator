import pandas as pd
import json
from random import uniform, randint, choices, seed
import numpy as np
from clases.person import Person
from parameters import CANCER_TREATMENT_COSTS, FIT_SENSITIVITY, FIT_SPECIFICITY, SEED, FIT_COST, COLONOSCOPY_COST, YEARS_TO_SIMULATE, STARTING_YEAR, SCREENING_FREQUENCY, CRC_PREVALENCE
initial_population = pd.read_csv('processed_data/initial_population.csv', sep=';', encoding='utf-8', low_memory=False)
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
            year_of_birth = self.year
            for j in range(int(initial_population_dict[i][1])):
                self.population.append(Person(i, year_of_birth, self.adherence_percentage, self.counter, self.crc_prevalence))
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
            pd.DataFrame([[self.year, fit, colonoscopy, yearly_fit_cost, yearly_colonoscopy_cost, self.yearly_stage_I_treatments, self.yearly_stage_II_treatments, self.yearly_stage_III_treatments, self.yearly_stage_IV_treatments, cancer_stage_I_cost, cancer_stage_II_cost, cancer_stage_III_cost, cancer_stage_IV_cost, cancer_treatments, total_cancer_treatment_costs, total_cost, self.expectancy_years_gained, self.asymptomatic_ccr_discovered]],
            columns=['Year', 'Fit', 'Colonoscopy', 'Fit Costs', 'Colonoscopy Costs', 'CancerStageITreatments', 'CancerStageIITreatments', 'CancerStageIIITreatments', 'CancerStageIVTreatments', 'CancerStageI', 'CancerStageII', 'CancerStageIII', 'CancerStageIV', 'Cancer Treatments', 'Cancer Treatments Costs', 'Total', 'YearsGained', 'AsymtomaticCCRDiscovered'])], 
            ignore_index=True
            )
        
    def next_year(self):
        seed(self.year)
        conteo_poblacion = {}
        print('='*5, 'ADH', str(self.adherence_percentage) + '%', '='*5,'Año' , self.year, '='*5)
        poblacion_inicial = len(self.population)
        nacimientos = round(np.random.normal(9000, 500))
        nacimientos2 = round(np.random.normal(3200, 300))
        nacimientos3 = round(np.random.normal(1800, 300))
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
            pd.DataFrame([[self.year, len(self.population), nacimientos + nacimientos2 + nacimientos3, self.yearly_deaths, self.yearly_cancer_deaths, poblacion50_75, self.yearly_people_with_cancer, self.yearly_screened, self.yearly_true_positives, self.yearly_false_positives, self.yearly_symptomatic_cancer_treatments, self.yearly_asymptomatic_cancer_treatments, self.yearly_stage_I_treatments, self.yearly_stage_II_treatments, self.yearly_stage_III_treatments, self.yearly_stage_IV_treatments, self.expectancy_years_gained, self.asymptomatic_ccr_discovered]], 
            columns=['Year', 'Total', 'Births', 'Deaths', 'DeathsByCancer', '50-75', 'HaveCancer', 'Screened', 'TruePositives', 'FalsePositives', 'SymptomaticTreatments', 'AsymptomaticTreatments', 'StageITreatments', 'StageIITreatments', 'StageIIITreatments', 'StageIVTreatments', 'YearsGained', 'AsymtomaticCCRDiscovered'])], 
            ignore_index=True
            )
        
        self.population = [i for i in self.population if i.alive]

        # Add the new people to the population
        for i in range(nacimientos):
            self.population.append(Person(0, self.year, self.adherence_percentage, self.counter, self.crc_prevalence))
            self.counter += 1
        for i in range(nacimientos2):
            self.population.append(Person(randint(1,8), self.year, self.adherence_percentage, self.counter, self.crc_prevalence))
            self.counter += 1
        for i in range(nacimientos3):
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
                            self.expectancy_years_gained += person.asymptomatic_screening()
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

        if not os.path.exists('simulations/' + self.folder_name):
            os.makedirs('simulations/' + self.folder_name)
            os.makedirs('simulations/' + self.folder_name + '/censo')
            os.makedirs('simulations/' + self.folder_name + '/population_stats')
            os.makedirs('simulations/' + self.folder_name + '/costs')
            os.makedirs('simulations/' + self.folder_name + '/parameters')
        else:
            print('It already exists')
        self.census.to_csv('simulations/' + self.folder_name + '/censo/censo' + '_'.join(str(self.adherence_percentage).split('.')) + '.csv', index=False, header=True, sep=';')
        self.population_stats.to_csv('simulations/' + self.folder_name + '/population_stats/population_stats' + '_'.join(str(self.adherence_percentage).split('.')) + '.csv', index=False, header=True, sep=';')
        self.costs.to_csv('simulations/' + self.folder_name + '/costs/costs_' + '_'.join(str(self.adherence_percentage).split('.')) + '.csv', index=False, header=True, sep=';')
        with open('simulations/' + self.folder_name + '/parameters/simulation_parameters.json', 'w') as file:
                json.dump(parameters, file, indent=4)
# Start counting the time
import time
start_time = time.time()

adherence_percentage_list = [0, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8]

if not os.path.exists('simulations/default'):
    for adherence_percentage in adherence_percentage_list:
        default = Population(adherence_percentage, 'default')
        default.simulate()


        print("--- %s seconds ---" % int((time.time() - start_time)))
else:
    print('The default folder already exists')

# Defaults
# 1
if not os.path.exists('simulations/default_1'):
    for adherence_percentage in adherence_percentage_list:
        default_1 = Population(adherence_percentage, 'default_1')
        default_1.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default folder already exists')

# 2
if not os.path.exists('simulations/default_2'):
    for adherence_percentage in adherence_percentage_list:
        default_2 = Population(adherence_percentage, 'default_2')
        default_2.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default folder already exists')
# 3
if not os.path.exists('simulations/default_3'):
    for adherence_percentage in adherence_percentage_list:
        default_3 = Population(adherence_percentage, 'default_3')
        default_3.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_3 folder already exists')

# 4
if not os.path.exists('simulations/default_4'):
    for adherence_percentage in adherence_percentage_list:
        default_4 = Population(adherence_percentage, 'default_4')
        default_4.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_4 folder already exists')

# 5
if not os.path.exists('simulations/default_5'):
    for adherence_percentage in adherence_percentage_list:
        default_5 = Population(adherence_percentage, 'default_5')
        default_5.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_5 folder already exists')

# 6
if not os.path.exists('simulations/default_6'):
    for adherence_percentage in adherence_percentage_list:
        default_6 = Population(adherence_percentage, 'default_6')
        default_6.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_6 folder already exists')

# 7
if not os.path.exists('simulations/default_7'):
    for adherence_percentage in adherence_percentage_list:
        default_7 = Population(adherence_percentage, 'default_7')
        default_7.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_7 folder already exists')

# 8
if not os.path.exists('simulations/default_8'):
    for adherence_percentage in adherence_percentage_list:
        default_8 = Population(adherence_percentage, 'default_8')
        default_8.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_8 folder already exists')

# 9
if not os.path.exists('simulations/default_9'):
    for adherence_percentage in adherence_percentage_list:
        default_9 = Population(adherence_percentage, 'default_9')
        default_9.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_9 folder already exists')

# 10
if not os.path.exists('simulations/default_10'):
    for adherence_percentage in adherence_percentage_list:
        default_10 = Population(adherence_percentage, 'default_10')
        default_10.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_10 folder already exists')
# I. Screening Frequency
# 1. 1 year
if not os.path.exists('simulations/1year'):
    year1 = Population(0.8, '1year')
    year1.years_to_simulate = 200
    year1.screening_frequency = ['Annual', 50, 75, 1, 0]
    year1.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 1year folder already exists')

# 2. 2 years
if not os.path.exists('simulations/2year'):
    year2 = Population(0.8, '2year')
    year2.years_to_simulate = 200
    year2.screening_frequency = ['Biennial', 50, 75, 2, 0]
    year2.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 2year folder already exists')

# 3. 3 years
if not os.path.exists('simulations/3year'):
    year3 = Population(0.8, '3year')
    year3.years_to_simulate = 200
    year3.screening_frequency = ['Triennial', 50, 75, 3, 1]
    year3.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 3year folder already exists')

# 4. 4 years
if not os.path.exists('simulations/4year'):
    year4 = Population(0.8, '4year')
    year4.years_to_simulate = 200
    year4.screening_frequency = ['Quadrennial', 50, 75, 4, 2]
    year4.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 4year folder already exists')

# 5. 5 years
if not os.path.exists('simulations/5year'):
    year5 = Population(0.8, '5year')
    year5.years_to_simulate = 200
    year5.screening_frequency = ['Quinquennial', 50, 75, 5, 0]
    year5.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 5year folder already exists')


# II. First round of intervals
# 1. 50-75
if not os.path.exists('simulations/interval50_75'):
    interval50_75 = Population(0.8, 'interval50_75')
    interval50_75.years_to_simulate = 200
    interval50_75.screening_frequency = ['Biennial', 50, 75, 2, 0]
    interval50_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-75 folder already exists')

# 2. 45-80
if not os.path.exists('simulations/interval45_80'):
    interval45_80 = Population(0.8, 'interval45_80')
    interval45_80.years_to_simulate = 200
    interval45_80.screening_frequency = ['Biennial', 45, 80, 2, 1]
    interval45_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 45-80 folder already exists')

# 3. 40-85
if not os.path.exists('simulations/interval40_85'):
    interval40_85 = Population(0.8, 'interval40_85')
    interval40_85.years_to_simulate = 200
    interval40_85.screening_frequency = ['Biennial', 40, 85, 2, 0]
    interval40_85.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 40-85 folder already exists')

# 4. 35-90
if not os.path.exists('simulations/interval35_90'):
    interval35_90 = Population(0.8, 'interval35_90')
    interval35_90.years_to_simulate = 200
    interval35_90.screening_frequency = ['Biennial', 35, 90, 2, 1]
    interval35_90.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 35-90 folder already exists')


# III. Second round of intervals
# OG 50-75
# 1. 45-75
if not os.path.exists('simulations/interval45_75'):
    interval45_75 = Population(0.8, 'interval45_75')
    interval45_75.years_to_simulate = 200
    interval45_75.screening_frequency = ['Biennial', 45, 75, 2, 1]
    interval45_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 45-75 folder already exists')

# 2. 40-75
if not os.path.exists('simulations/interval40_75'):
    interval40_75 = Population(0.8, 'interval40_75')
    interval40_75.years_to_simulate = 200
    interval40_75.screening_frequency = ['Biennial', 40, 75, 2, 0]
    interval40_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 40-75 folder already exists')

# 3. 50-80
if not os.path.exists('simulations/interval50_80'):
    interval50_80 = Population(0.8, 'interval50_80')
    interval50_80.years_to_simulate = 200
    interval50_80.screening_frequency = ['Biennial', 50, 80, 2, 0]
    interval50_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-80 folder already exists')

# 4. 50-85
if not os.path.exists('simulations/interval50_85'):
    interval50_85 = Population(0.8, 'interval50_85')
    interval50_85.years_to_simulate = 200
    interval50_85.screening_frequency = ['Biennial', 50, 85, 2, 0]
    interval50_85.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-85 folder already exists')

# 5. 40-80
if not os.path.exists('simulations/interval40_80'):
    interval40_80 = Population(0.8, 'interval40_80')
    interval40_80.years_to_simulate = 200
    interval40_80.screening_frequency = ['Biennial', 40, 80, 2, 0]
    interval40_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 40-80 folder already exists')

# 6. 35-80
if not os.path.exists('simulations/interval35_80'):
    interval35_80 = Population(0.8, 'interval35_80')
    interval35_80.years_to_simulate = 200
    interval35_80.screening_frequency = ['Biennial', 35, 80, 2, 1]
    interval35_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 35-80 folder already exists')

# 7. 45-85
if not os.path.exists('simulations/interval45_85'):
    interval45_85 = Population(0.8, 'interval45_85')
    interval45_85.years_to_simulate = 200
    interval45_85.screening_frequency = ['Biennial', 45, 85, 2, 1]
    interval45_85.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 45-85 folder already exists')

# 8. 55-75
if not os.path.exists('simulations/interval55_75'):
    interval55_75 = Population(0.8, 'interval55_75')
    interval55_75.years_to_simulate = 200
    interval55_75.screening_frequency = ['Biennial', 55, 75, 2, 1]
    interval55_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 55-75 folder already exists')

# 9. 50-70
if not os.path.exists('simulations/interval50_70'):
    interval50_70 = Population(0.8, 'interval50_70')
    interval50_70.years_to_simulate = 200
    interval50_70.screening_frequency = ['Biennial', 50, 70, 2, 0]
    interval50_70.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-70 folder already exists')

# 9. 60-75
if not os.path.exists('simulations/interval60_75'):
    interval60_75 = Population(0.8, 'interval60_75')
    interval60_75.years_to_simulate = 200
    interval60_75.screening_frequency = ['Biennial', 60, 75, 2, 0]
    interval60_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 60-75 folder already exists')

# 10. 55-80
if not os.path.exists('simulations/interval55_80'):
    interval55_80 = Population(0.8, 'interval55_80')
    interval55_80.years_to_simulate = 200
    interval55_80.screening_frequency = ['Biennial', 55, 80, 2, 1]
    interval55_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 55-80 folder already exists')

# IV. Colonoscopy Costs
if not os.path.exists('simulations/colonoscopy_421005'):
    colonoscopy_421005 = Population(0.8, 'colonoscopy_421005')
    colonoscopy_421005.colonoscopy_cost = 421005
    colonoscopy_421005.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The colonoscopy_421005 folder already exists')

if not os.path.exists('simulations/colonoscopy_504205'):
    colonoscopy_504205 = Population(0.8, 'colonoscopy_504205')
    colonoscopy_504205.colonoscopy_cost = 504205
    colonoscopy_504205.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval colonoscopy_504205 folder already exists')

if not os.path.exists('simulations/colonoscopy_425621'):
    colonoscopy_425621 = Population(0.8, 'colonoscopy_425621')
    colonoscopy_425621.colonoscopy_cost = 425621
    colonoscopy_425621.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The colonoscopy_425621 folder already exists')

if not os.path.exists('simulations/colonoscopy_333190'):
    colonoscopy_333190 = Population(0.8, 'colonoscopy_333190')
    colonoscopy_333190.colonoscopy_cost = 333190
    colonoscopy_333190.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The colonoscopy_333190 folder already exists')


# V. FIT Sensitivity
# 1. Improve Sensitivity
if not os.path.exists('simulations/improved_sensitivity'):
    improved_sensitivity = Population(0.8, 'improved_sensitivity')
    improved_sensitivity.fit_sensitivity = 0.85
    improved_sensitivity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The improved_sensitivity folder already exists')

# 2. Worse Sensitivity
if not os.path.exists('simulations/worse_sensitivity'):
    worse_sensitivity = Population(0.8, 'worse_sensitivity')
    worse_sensitivity.fit_sensitivity = 0.73
    worse_sensitivity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The worse_sensitivity folder already exists')


# VI. FIT Specificity
# 1. Improve Specificity
if not os.path.exists('simulations/improved_specificity'):
    improved_specificity = Population(0.8, 'improved_specificity')
    improved_specificity.fit_specificity = 0.96
    improved_specificity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The improved_specificity folder already exists')

# 2. Worse Specificity
if not os.path.exists('simulations/worse_specificity'):
    worse_specificity = Population(0.8, 'worse_specificity')
    worse_specificity.fit_specificity = 0.92
    worse_specificity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The worse_specificity folder already exists')

# 3. Super Improved Specificity
if not os.path.exists('simulations/super_improved_specificity'):
    super_improved_specificity = Population(0.8, 'super_improved_specificity')
    super_improved_specificity.fit_specificity = 0.999
    super_improved_specificity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The super_improved_specificity folder already exists')

print("--- %s minutes ---" % int((time.time() - start_time)/60))

# VII. FIT Costs
if not os.path.exists('simulations/fit_5865'):
    fit_5865 = Population(0.8, 'fit_5865')
    fit_5865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_5865 folder already exists')

if not os.path.exists('simulations/fit_4865'):
    fit_4865 = Population(0.8, 'fit_4865')
    fit_4865.fit_cost_cost = 4865
    fit_4865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval fit_4865 folder already exists')

if not os.path.exists('simulations/fit_3865'):
    fit_3865 = Population(0.8, 'fit_3865')
    fit_3865.fit_cost = 3865
    fit_3865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_3865 folder already exists')

if not os.path.exists('simulations/fit_6865'):
    fit_6865 = Population(0.8, 'fit_6865')
    fit_6865.fit_cost = 6865
    fit_6865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_6865 folder already exists')

if not os.path.exists('simulations/fit_2865'):
    fit_2865 = Population(0.8, 'fit_2865')
    fit_2865.fit_cost = 2865
    fit_2865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_2865 folder already exists')