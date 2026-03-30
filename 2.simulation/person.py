from random import uniform, randint, choices, seed
import numpy as np
import pandas as pd
from life_expectancy import get_female_life_expectancy_dictionary, get_male_life_expectancy_dictionary
from crc_life_expectancy import get_crc_life_expectancies

male_life_expectancy_dict = get_male_life_expectancy_dictionary()
female_life_expectancy_dict = get_female_life_expectancy_dictionary()


# Obtained from https://gis.cdc.gov/Cancer/USCS/#/Demographics/  
ccr_age_risk = pd.read_csv('1.processed_data/ccr_risk.csv', sep=';', encoding='utf-8', low_memory=False)

ccr_age_risk_list = []

# From https://pubmed.ncbi.nlm.nih.gov/21984657/ Table 2
# [start_age, end_age, mean, lower, upper] CI 95%
preclinical_sojourn_time_list = {
    'male': [[0, 59 ,5.5 ,5.1, 6.0], [60, 64, 5.2, 4.9, 5.5], [65, 69, 4.7, 4.5, 4.9], [70, 74, 4.9, 4.6, 5.1], [75, 79, 5.0, 4.7, 5.3], [80, 120, 5.5, 5.0, 6.0]],
    'female': [[0, 59, 4.7, 4.3, 5.1], [60, 65, 4.5, 4.1, 4.8], [65, 69, 4.6, 4.3, 4.8], [70, 74, 4.8, 4.5, 5.1], [75, 79, 5.2, 4.8, 5.6], [80, 120, 5.8, 5.3, 6.3]]
}

# From https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3415614/ Table 4
cancer_life_expectancy_by_stage_and_age = get_crc_life_expectancies()

# From https://pubmed.ncbi.nlm.nih.gov/19581668/ Table 3
cancer_stage_probability = {
    'symptomatic': [0.04, 0.46, 0.27, 0.22], 
    'asymptomatic': [0.49, 0.15, 0.29, 0.07]
}

for row in ccr_age_risk.iterrows():
    start_year = row[1]['Start Year']
    end_year = row[1]['End Year']
    cases = row[1]['Case Count']
    if cases == 'Data not presented':
        cases = 0
    if cases == '12933':
        start_year = 85
        end_year = 120

    cases = int(cases)
    ccr_age_risk_list.append([start_year, end_year, cases])
ccr_age_risk_list.pop(0)





class Person():

    def __init__(self, age: int, year_of_inscription: int, adherence_percentage: float, counter: int, prevalence: float) -> None:
        seed(counter)
        np.random.seed(counter % (2**31))
        self.alive = True
        self.age = int(age)
        self.year_of_birth = int(year_of_inscription)-self.age
        self.will_develop_cancer = False
        self.male = False
        self.detectable_cancer = False
        self.treated_cancer = False
        self.screenable = False
        self.debug_flag = False
        self.cancer_determined_death = False
        self.counter = counter
        if uniform(0,1) < 0.5:
            self.male = True

        # Generate the age of natural death
        self.simulate_age_of_natural_death()
        simulate_age_of_death_attempts = 0
        

        # Generate the probability of being screenable
        self.screenable = False
        if uniform(0,1) < adherence_percentage:
            self.screenable = True
        
        # Generate the probability of developing cancer
        if uniform(0,1) < prevalence:
            self.simulate_cancer_history()
        #if self.will_develop_cancer:
        #    print('Person: ', self.counter, '\nScreenable', self.screenable, '\nAge of Death', self.age_of_death, '\nAge of Screnable Cancer', self.age_of_screenable_cancer, '\nAge of Symptomatic Cancer', self.age_of_symptomatic_cancer, '\nAge', self.age, '\n*******************')

    def die(self) -> None:
        self.alive = False

    def simulate_age_of_natural_death(self) -> None:
        if self.year_of_birth > 2095:
            media = 91-self.age
        elif self.male:
            media = male_life_expectancy_dict[self.year_of_birth][self.age]
        else:
            media = female_life_expectancy_dict[self.year_of_birth][self.age]
        self.attempts = 0
        sd = 8-round(self.age/15)
        #sd = 8
        expected_years_left = round(np.random.normal(media, sd))
        if expected_years_left < 0:
            expected_years_left = 0
        
        self.age_of_death = round(self.age + expected_years_left)
        if self.age_of_death > 120:
            self.age_of_death = 120
        self.natural_age_of_death = self.age_of_death
        
    def simulate_cancer_history(self) -> None:
        # Booleans to manage the cancer history
        self.will_develop_cancer = True
        self.detectable_cancer = False
        self.treated_cancer = False

        # Cancer stage
        self.asymptomatic_cancer_stage = choices(['I', 'II', 'III', 'IV'], weights=cancer_stage_probability['asymptomatic'])[0]
        self.symptomatic_cancer_stage = choices(['I', 'II', 'III', 'IV'], weights=cancer_stage_probability['symptomatic'])[0]

        # Define age of symptomatic cancer
        age_interval_of_cancer = choices(ccr_age_risk_list, weights=[item[2] for item in ccr_age_risk_list])[0]
        self.age_of_symptomatic_cancer = randint(age_interval_of_cancer[0], age_interval_of_cancer[1])
        
        # Define age of screenable cancer
        preclinical_sojourn_time = 5
        if self.male:
            sojourn_time_list = preclinical_sojourn_time_list['male']
        else:
            sojourn_time_list = preclinical_sojourn_time_list['female']
        for i in sojourn_time_list:
            if self.age_of_symptomatic_cancer >= i[0] and self.age_of_symptomatic_cancer <= i[1]:
                preclinical_sojourn_time = round(np.random.normal(i[2], (i[4]-i[2])/2))
        self.age_of_screenable_cancer = self.age_of_symptomatic_cancer - preclinical_sojourn_time

        # Define age of death based on cancer stage
        self.cancer_determined_death = True
        if self.male:
            self.age_of_death = round(self.age_of_symptomatic_cancer + cancer_life_expectancy_by_stage_and_age['LE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
        else:
            self.age_of_death = round(self.age_of_symptomatic_cancer + cancer_life_expectancy_by_stage_and_age['LE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])

        # This person can already be screened
        if self.age >= self.age_of_screenable_cancer:
            self.detectable_cancer = True

        # If the age is higher than the age of death, redefine age
        if self.age > self.age_of_death:
            self.age = randint(0, self.age_of_death)
        
        # This person already had their cancer detected and treated
        if self.age > self.age_of_symptomatic_cancer:
            self.treat_cancer()
            self.debug_flag = True
        
        if self.age_of_death > 120:
            self.age_of_death = 120
        

    
    def asymptomatic_screening(self) -> tuple[int, int, int, int]:
        year_of_birth = self.year_of_birth
        if year_of_birth > 2095:
            year_of_birth = 2095
        
        old_age = self.age_of_death
        if self.male:
            self.age_of_death = round(self.age_of_symptomatic_cancer + cancer_life_expectancy_by_stage_and_age['LE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            years_gained = round(cancer_life_expectancy_by_stage_and_age['LE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['LE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            healthy_years_gained = round(cancer_life_expectancy_by_stage_and_age['HLE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['HLE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            disability_free_years_gained = round(cancer_life_expectancy_by_stage_and_age['DFLE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            disability_years_difference = round(
                cancer_life_expectancy_by_stage_and_age['LE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] 
                - (cancer_life_expectancy_by_stage_and_age['LE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            )
            # Asymptomatic DALY
            asymptomatic_disability_years_lost = cancer_life_expectancy_by_stage_and_age['LE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            asymptomatic_years_lost = male_life_expectancy_dict[year_of_birth][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['LE']['male'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            asymptomatic_daly = (asymptomatic_disability_years_lost * 0.288) + asymptomatic_years_lost

            # Symptomatic DALY
            symptomatic_disability_years_lost = cancer_life_expectancy_by_stage_and_age['LE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            symptomatic_years_lost = male_life_expectancy_dict[year_of_birth][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['LE']['male'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            symptomatic_daly = (symptomatic_disability_years_lost * 0.288) + symptomatic_years_lost
        else:
            self.age_of_death = round(self.age_of_symptomatic_cancer + cancer_life_expectancy_by_stage_and_age['LE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            years_gained = round(cancer_life_expectancy_by_stage_and_age['LE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['LE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            healthy_years_gained = round(cancer_life_expectancy_by_stage_and_age['HLE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['HLE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            disability_free_years_gained = round(cancer_life_expectancy_by_stage_and_age['DFLE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            disability_years_difference = round(
                cancer_life_expectancy_by_stage_and_age['LE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] 
                - (cancer_life_expectancy_by_stage_and_age['LE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer])
            , 3)

            # Asymptomatic DALY
            asymptomatic_disability_years_lost = cancer_life_expectancy_by_stage_and_age['LE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            asymptomatic_years_lost = female_life_expectancy_dict[year_of_birth][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['LE']['female'][self.asymptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            asymptomatic_daly = (asymptomatic_disability_years_lost * 0.288) + asymptomatic_years_lost

            # Symptomatic DALY
            symptomatic_disability_years_lost = cancer_life_expectancy_by_stage_and_age['LE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['DFLE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            symptomatic_years_lost = female_life_expectancy_dict[year_of_birth][self.age_of_symptomatic_cancer] - cancer_life_expectancy_by_stage_and_age['LE']['female'][self.symptomatic_cancer_stage][self.age_of_symptomatic_cancer]
            symptomatic_daly = (symptomatic_disability_years_lost * 0.288) + symptomatic_years_lost
        
        daly = round(symptomatic_daly - asymptomatic_daly)
        #print('male', str(self.male), '\nyears gained', str(years_gained), '\ndisability years difference', str(disability_years_difference), '\nsymptomatic daly', str(symptomatic_daly), '\nasymptomatic daly', str(asymptomatic_daly), '\ndaly', str(daly) + '\n*******************')
        return years_gained, healthy_years_gained, disability_free_years_gained, daly
    def treat_cancer(self) -> None:
        self.treated_cancer = True
        self.will_develop_cancer = False
        self.detectable_cancer = False

    def revert_to_natural_death(self) -> None:
        """Revert death age to pre-cancer natural death (used after polypectomy)."""
        self.age_of_death = self.natural_age_of_death
        self.cancer_determined_death = False
        self.will_develop_cancer = False
        self.detectable_cancer = False
        self.treated_cancer = True


def generate_random_cancer_age() -> int:
    age_interval = choices(ccr_age_risk_list, weights=[item[2] for item in ccr_age_risk_list])[0]
    age_of_symptomatic_cancer = randint(age_interval[0], age_interval[1])
    return age_of_symptomatic_cancer

def test() -> None:
    cancer_list = []
    for i in range(10000):
        cancer_list.append(generate_random_cancer_age())

    cancer_list_85 = [i for i in cancer_list if i >= 85]
    cancer_list_under_50 = [i for i in cancer_list if i < 50]
    # Plot the histogram of the cancer_list with ranges of 5 years until 85 and then 85-120 as one bin
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(20,10))
    plt.hist(cancer_list, bins=range(0, 111, 5), density=True, label='Cancer')
    plt.hist(cancer_list_85, bins=1, density=True, label='Cancer 85-120')
    plt.legend()
    plt.show()

    print(len(cancer_list_under_50))
