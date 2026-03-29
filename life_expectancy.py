import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from random import randint
from random import choices



def get_male_life_expectancy_dictionary():
    male_life_expectancy = pd.read_csv('initial_data/cohort_life_expectancy_male.csv', sep=';', encoding='utf-8', low_memory=False)
    print(male_life_expectancy.shape)
    male_life_expectancy_dict = {}
    print(male_life_expectancy.columns)
    for i in range(1900,2096):

        male_life_expectancy_dict[i] = {}
        
        for j in range(120):
            male_life_expectancy_dict[i][j] = male_life_expectancy[(male_life_expectancy['Year'] == i) & (male_life_expectancy['x'] == j)]['e(x)'].values[0]


    return male_life_expectancy_dict

def get_female_life_expectancy_dictionary():
    female_life_expectancy = pd.read_csv('initial_data/cohort_life_expectancy_female.csv', sep=';', encoding='utf-8', low_memory=False)
    print(female_life_expectancy.shape)
    female_life_expectancy_dict = {}

    for i in range(1900,2096):
        female_life_expectancy_dict[i] = {}
        
        for j in range(120):
            female_life_expectancy_dict[i][j] = female_life_expectancy[(female_life_expectancy['Year'] == i) & (female_life_expectancy['x'] == j)]['e(x)'].values[0]


    return female_life_expectancy_dict


def get_male_life_expectancy_dictionary2():
    male_life_expectancy = pd.read_csv('initial_data/cohort_life_expectancy_male.csv', sep=';', encoding='utf-8', low_memory=False)

    male_life_expectancy_dict = {}
    print(male_life_expectancy.columns)
    for i in range(1900,2096):
        male_life_expectancy_dict[i] = male_life_expectancy[(male_life_expectancy['Year'] == i) & (male_life_expectancy['x'] == 0)]['e(x)'].values[0]

    return male_life_expectancy_dict

def get_female_life_expectancy_dictionary2():
    female_life_expectancy = pd.read_csv('initial_data/cohort_life_expectancy_female.csv', sep=';', encoding='utf-8', low_memory=False)

    female_life_expectancy_dict = {}

    for i in range(1900,2096):
        female_life_expectancy_dict[i] =  female_life_expectancy[(female_life_expectancy['Year'] == i) & (female_life_expectancy['x'] == 0)]['e(x)'].values[0]

    return female_life_expectancy_dict


def get_male_life_expectancy_plot():
    male_life_expectancy = pd.read_csv('initial_data/cohort_life_expectancy_male.csv', sep=';', encoding='utf-8', low_memory=False)
    female_life_expectancy = pd.read_csv('initial_data/cohort_life_expectancy_female.csv', sep=';', encoding='utf-8', low_memory=False)
    chilean_male_life_expectancy = pd.read_excel('initial_data/tablas-de-mortalidad-de-chile-1992-2050.xlsx', sheet_name='BD Tablas de Mortalidad', skiprows=1)
    print(chilean_male_life_expectancy.shape)
    chilean_male_life_expectancy = chilean_male_life_expectancy[chilean_male_life_expectancy['Cod_region'] == 0]

    

    print(chilean_male_life_expectancy.shape)
    years = []
    male_life_expectancy_list = []
    female_life_expectancy_list = []
    chilean_male_life_expectancy_list = []
    for i in range(1900,2096):
        years.append(i)
        male_life_expectancy_list.append(male_life_expectancy[(male_life_expectancy['Year'] == i) & (male_life_expectancy['x'] == 0)]['e(x)'].values[0])
        female_life_expectancy_list.append(female_life_expectancy[(female_life_expectancy['Year'] == i) & (female_life_expectancy['x'] == 0)]['e(x)'].values[0])
        if chilean_male_life_expectancy[(chilean_male_life_expectancy['Año'] == i) & (chilean_male_life_expectancy['Edad'] == 0)].shape[0] > 0:
            chilean_male_life_expectancy_list.append(chilean_male_life_expectancy[(chilean_male_life_expectancy['Año'] == i) & (chilean_male_life_expectancy['Edad'] == 0)]['e(x)'].values[0])
        else:
            chilean_male_life_expectancy_list.append(0)

    print(male_life_expectancy_list)
    print(chilean_male_life_expectancy_list)

    # Make the plot of the life expectancy vs the year with the male_life_expectancy_list and female_life_expectancy_list
    plt.figure(figsize=(10,5))
    plt.plot(years, male_life_expectancy_list, label='Male Cohort Life Expectancy')
    plt.plot(years, female_life_expectancy_list, label='Female Cohort Life Expectancy')
    plt.plot(years, chilean_male_life_expectancy_list, label='Chilean Male Life Expectancy')
    plt.legend()
    plt.savefig('plots/life_expectancy.png')

get_male_life_expectancy_plot()
    