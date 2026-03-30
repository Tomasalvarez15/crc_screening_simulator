

# Optimistic test
#FIT_SPECIFICITY = 0.96


# 1. Sets the SEED for the random number generator
SEED = 3000


# 2. Define the cost of cancer treatment by stage
# Values in Euros obtained from https://pubmed.ncbi.nlm.nih.gov/28189254/
# CLP value on January 6, 2017: 1 EUR = 702.14 CLP
# Inflation values obtained from https://es.statista.com/estadisticas/1189953/tasa-de-inflacion-chile/ 
# Inflation from 2017 to 2023
EUR_VALUE_2017 = 702.14
inflation2017_2023 = 1.0218 * 1.0232 * 1.00225 * 1.0304 * 1.0452 * 1.1165
conversion = EUR_VALUE_2017 * inflation2017_2023
CANCER_TREATMENT_COSTS = {
    'I': round(8644 * conversion),
    'II': round(12765.2 * conversion),
    'III': round(13075.2 * conversion),
    'IV': round(51333.5 * conversion)
}

# 3. Define the screening frequency
SCREENING_FREQUENCY = ['Biennial', 50, 75, 2, 0]



# 4. Define the cost of colonoscopy
# Colonoscopy cost obtained from https://www.ucchristus.cl/docs/default-source/pdf/aranceles-csc.pdf 

#COLONOSCOPY_COST = 80560

#Clinica Alemana
#COLONOSCOPY_COST = 504205

#Clinica UC Christus
#COLONOSCOPY_COST = 425621

#Clinica BUPA
#COLONOSCOPY_COST = 333190

#Average Clinic Cost
COLONOSCOPY_COST = 421005

# 5. Define the cost of FIT
# Value of FIT cost obtained from https://www.ucchristus.cl/docs/default-source/pdf/aranceles-csc.pdf 
FIT_COST = 5865

# 6. Define the prevalence of CRC in the population
# Obtained from https://www.cancer.org/cancer/types/colon-rectal-cancer/about/key-statistics.html#:~:text=the%20mid%2D1990s.-,Lifetime%20risk%20of%20colorectal%20cancer,risk%20factors%20for%20colorectal%20cancer.
CRC_PREVALENCE = 0.042


# 7. Define the number of years to run the simulation
YEARS_TO_SIMULATE = 20

# 8. Define the starting year
STARTING_YEAR = 2023

# From 
# 9. Define FIT sensitivity
FIT_SENSITIVITY = 0.79

# 10. Define FIT specificity
FIT_SPECIFICITY = 0.94

# 11. Polypectomy prevention rate
# ~52% of screening-detected cancers are caught as removable polyps
# Source: Zauber et al. NEJM 2012
POLYPECTOMY_PREVENTION_RATE = 0.52

if __name__ == '__main__':
    print('Inflation 2017-2023:', inflation2017_2023)
    print('Cancer Treatment Costs', CANCER_TREATMENT_COSTS)
