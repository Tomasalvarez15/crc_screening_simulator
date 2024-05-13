# From https://pubmed.ncbi.nlm.nih.gov/19581668/ Table 3
cancer_stage_probability = {
    'symptomatic': [0.04, 0.46, 0.27, 0.22], 
    'asymptomatic': [0.49, 0.15, 0.29, 0.07]
}


# Make two graph plots one with the symptomatic and the other with the asymptomatic stage percentages

# Do not show the y axis labels and put the percentage in the bars

from matplotlib import pyplot as plt
import numpy as np

# Data
labels = ['Stage I', 'Stage II', 'Stage III', 'Stage IV']
symptomatic = cancer_stage_probability['symptomatic']
asymptomatic = cancer_stage_probability['asymptomatic']

plt, ax = plt.subplots(1, 2, figsize=(10, 5))

# Plot
ax[1].bar(labels, symptomatic, color='#ff7f0e')
ax[0].bar(labels, asymptomatic, color='#1f77b4')

# Add title and labels
ax[1].set_title('Symptomatic\n(Base Scenario)')
ax[0].set_title('Asymptomatic\n(Optimum Scenario)')
ax[1].set_ylabel('Stage Probability')
ax[0].set_ylabel('Stage Probability')
ax[1].set_xlabel('Cancer Stage')
ax[0].set_xlabel('Cancer Stage')

# Add percentage to the bars
for i in range(4):
    ax[1].text(i, symptomatic[i], f'{symptomatic[i]*100:.0f}%', ha='center', va='bottom')
    ax[0].text(i, asymptomatic[i], f'{asymptomatic[i]*100:.0f}%', ha='center', va='bottom')

# Hide the y axis labels
ax[1].tick_params(axis='y', which='both', left=False, labelleft=False)
ax[0].tick_params(axis='y', which='both', left=False, labelleft=False)


plt.savefig('cancer_stage_probability.png')