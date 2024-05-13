import pandas as pd

poblacion = pd.read_excel('initial_data/PoblacionInscritaValidada2024.xlsx', sheet_name='SSMS')

print(poblacion.columns)
print(poblacion.shape)

# Get mean, median and std from Inscritos

edades = {}
for row in poblacion.iterrows():
    if type(row[1]['Edad']) == str:
            continue  
    if row[1]['Edad'] in edades:
        
        edades[row[1]['Edad']] += row[1]['Inscritos']
    else:
        edades[row[1]['Edad']] = row[1]['Inscritos']


print(edades)


#Sort the dictionary by key
edades = {k: v for k, v in sorted(edades.items(), key=lambda item: item[0])}

for i in edades:
    
    #print(i, edades[i])
    pass
# Sum all the values
total = 0
for i in edades:
    total += edades[i]

print('Total', total)

# Sum them by intervals of 5
edades_5 = {}

for i in range(0, 120, 5):
    try:
        edades_5[str(i) + '-' + str(i+4)] = 0
        for j in range(i, i+5):
           edades_5[str(i) + '-' + str(i+4)] += edades[j]
    except:
        pass

print(edades_5)

# Sum all the values
total = 0
for i in edades_5:
    total += edades_5[i]

print('Total', total)

# Sum all ages from 50 to 75

total = 0
for i in range(50, 76):


    # PubMed colorrectal cancer screening 
    #
    total += edades[i]

print(total)

# Make a dataframe with all ages and the number of people in each age
df = pd.DataFrame(list(edades.items()), columns=['Edad', 'Inscritos'])

# Add a new column called 'ratio' that is the number of Inscritos divided by the Inscritos of the previous row with only 3 decimals
df['Ratio'] = df['Inscritos'] / df['Inscritos'].shift(1)
df['Ratio'] = df['Ratio'].round(3)
poblacion_max = df['Inscritos'].max()
df['InscritosNeg'] = df['Inscritos'].apply(lambda x: poblacion_max - x)

print(df['Inscritos'].mean())
print(df['Inscritos'].median())
print(df['Inscritos'].std())
print('Poblacion 50-75', df['Inscritos'].loc[50:75].sum())
df.to_csv('processed_data/initial_population.csv', index=False, header=True, sep=';')

# Plot Inscritos vs Edad
import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(20,10))
plt.plot(df['Edad'], df['Inscritos'], label='Inscritos')
plt.legend()
# make xlabel label and text bigger
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Age', fontsize=18)
plt.ylabel('Registered', fontsize=18)
plt.title('Registered vs Age', fontsize=20)
plt.savefig('Registered_vs_Age.png')
