import json


def format_with_spaces(n):
    n_str = str(n)[::-1]
    formatted_str = ' '.join(n_str[i:i+3] for i in range(0, len(n_str), 3))
    return formatted_str[::-1]


def costs_analysis():
    import pandas as pd
    file_names = [['costs_0_2.csv', 'ADH 20%']]

    costs = pd.DataFrame(columns=['Total Cost M CLP', 'Percentage Cost', 'DifferenceCosts',
    'FIT', 'Colonoscopy',
    'FIT Costs', 'Colonoscopy Costs', 
    'Stage I Costs','Stage II Costs','Stage III Costs','Stage IV Costs',
    'Treatments', 'StageI', 'StageII', 'StageIII', 'StageIV',
    'StageI%', 'StageII%', 'StageIII%', 'StageIV%', 
    'YearsGained', 'AsymptomaticTreatments', 'SymptomaticTreatments'])
    import json

    # Path to your JSON file
    file_path = 'simulations/default/parameters/simulation_parameters.json'

    # Read from file
    with open(file_path, 'r') as file:
        parameters = json.load(file)

    print(parameters)
    for f in file_names:
        file_name = f[0]

        table = pd.read_csv('simulations/default/costs/' + file_name, sep=';', encoding='utf-8', low_memory=False)
        print(table.columns)
        total_cost = table['Total'].sum()
        fit = table['Fit'].sum()
        colonoscopy = table['Colonoscopy'].sum()
        fit_costs = table['Fit Costs'].sum()
        colonoscopy_costs = table['Colonoscopy Costs'].sum()
        stage_I_costs = table['CancerStageI'].sum()
        stage_II_costs = table['CancerStageII'].sum()
        stage_III_costs = table['CancerStageIII'].sum()
        stage_IV_costs = table['CancerStageIV'].sum()
        cancer_treatments = table['Cancer Treatments'].sum()
        cancer_stage_I_treatments = table['CancerStageITreatments'].sum()
        cancer_stage_II_treatments = table['CancerStageIITreatments'].sum()
        cancer_stage_III_treatments = table['CancerStageIIITreatments'].sum()
        cancer_stage_IV_treatments = table['CancerStageIVTreatments'].sum()
        cancer_stage_I_pct = cancer_stage_I_treatments/cancer_treatments
        cancer_stage_II_pct = cancer_stage_II_treatments/cancer_treatments
        cancer_stage_III_pct = cancer_stage_III_treatments/cancer_treatments
        cancer_stage_IV_pct = cancer_stage_IV_treatments/cancer_treatments
        years_gained = table['YearsGained'].sum()
        asymptomatic_treatments = table['AsymtomaticCCRDiscovered'].sum()
        symptomatic_treatments = cancer_treatments - asymptomatic_treatments
        print(f[1],'Total Cost in M CLP:', total_cost, 'Total Cancer Treatments', cancer_treatments, 'Cancer Stage I Treatments', cancer_stage_I_treatments, 'Cancer Stage II Treatments', cancer_stage_II_treatments, 'Cancer Stage III Treatments', cancer_stage_III_treatments, 'Cancer Stage IV Treatments', cancer_stage_IV_treatments, sep='\n')
        #costs.loc[f[1]] = [total_cost, 0.01, cancer_treatments, cancer_stage_I_treatments, cancer_stage_II_treatments, cancer_stage_III_treatments, cancer_stage_IV_treatments, cancer_stage_I_pct, cancer_stage_II_pct, cancer_stage_III_pct, cancer_stage_IV_pct, years_gained, asymptomatic_discoveries]
        costs.loc[f[1]] = {'Total Cost M CLP': total_cost, 
        'Percentage Cost': 0.01, 'DifferenceCosts': 0, 
        'FIT': fit, 'Colonoscopy': colonoscopy,
        'FIT Costs': fit_costs, 'Colonoscopy Costs': colonoscopy_costs,
        'Stage I Costs': stage_I_costs, 'Stage II Costs': stage_II_costs, 'Stage III Costs': stage_III_costs, 'Stage IV Costs': stage_IV_costs,
        'Treatments': cancer_treatments, 
        'StageI': cancer_stage_I_treatments, 'StageII': cancer_stage_II_treatments, 'StageIII': cancer_stage_III_treatments, 'StageIV': cancer_stage_IV_treatments,
        'StageI%': cancer_stage_I_pct, 'StageII%': cancer_stage_II_pct, 'StageIII%': cancer_stage_III_pct, 'StageIV%': cancer_stage_IV_pct, 
        'YearsGained': years_gained, 'AsymptomaticTreatments': asymptomatic_treatments, 'SymptomaticTreatments': symptomatic_treatments}

    print(costs.head)
    base_cost = costs.loc['ADH 20%']['Total Cost M CLP']
    print(base_cost)
    for f in file_names:
        costs.loc[f[1],'Percentage Cost'] = costs.loc[f[1]]['Total Cost M CLP']/base_cost
        costs.loc[f[1],'DifferenceCosts'] = costs.loc[f[1]]['Total Cost M CLP'] - base_cost

    # Percentaje Cost as percentage string
    costs['Percentage Cost'] = costs['Percentage Cost'].apply(lambda x: '{:.2%}'.format(x))
    # Treaments as ints
    costs['Cancer Treatments'] = costs['Treatments'].apply(lambda x: int(x))
    costs['StageI'] = costs['StageI'].apply(lambda x: int(x))
    costs['StageII'] = costs['StageII'].apply(lambda x: int(x))
    costs['StageIII'] = costs['StageIII'].apply(lambda x: int(x))
    costs['StageIV'] = costs['StageIV'].apply(lambda x: int(x))


    costs['StageI%'] = costs['StageI%'].apply(lambda x: '{:.2%}'.format(x))
    costs['StageII%'] = costs['StageII%'].apply(lambda x: '{:.2%}'.format(x))
    costs['StageIII%'] = costs['StageIII%'].apply(lambda x: '{:.2%}'.format(x))
    costs['StageIV%'] = costs['StageIV%'].apply(lambda x: '{:.2%}'.format(x))


    costs.to_csv('simulations/default/costs_example.csv', sep=';', encoding='utf-8', index=True)

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    # Make a graph bar with the symptomatic and asymptomatic treatments by the adherence percentage
    # No subplots

    fig, ax = plt.subplots()
    adherences = costs.index
    adherences = [x for x in adherences]
    costs['AsymptomaticTreatmentsPercentage'] = costs['AsymptomaticTreatments']/costs['Treatments']
    costs['SymptomaticTreatmentsPercentage'] = costs['SymptomaticTreatments']/costs['Treatments']
    print('PAAAAN')
    print(costs[['AsymptomaticTreatmentsPercentage', 'SymptomaticTreatmentsPercentage']])
    costs[['AsymptomaticTreatmentsPercentage', 'SymptomaticTreatmentsPercentage']].plot(kind='barh', ax=ax, stacked=True, color=['#1f77b4', '#ff7f0e'], figsize=(10, 2))
    ax.invert_yaxis()

    # Set the legend in the upper right corner
    ax.legend(loc='upper right', labels=['Asymptomatic', 'Symptomatic'])

    # Put the asymptomatic percentage in the bars
    for i, v in enumerate(costs['AsymptomaticTreatmentsPercentage']):
        ax.text(v, i, '{:.2%}'.format(v), ha='left', va='center', fontsize=12)
    

    plt.savefig('plots/screening_efficacy_for_example.png')

    # Print all the asymptomatic treatments percentages divided by the adherence percentage
    adherences_percentages = [0.2]
    for i in range(1):
        adherences_percentage = adherences_percentages[i]
        asymptomatic_treatments = costs.loc[adherences[i], 'AsymptomaticTreatments']
        print(asymptomatic_treatments / adherences_percentage)



    

    # Make a multiple graphs by the adherence percentage with the stage treatments quantity

    fig, ax = plt.subplots(1, figsize=(8, 12))
    adherence = adherences[0]
    costs.loc[adherence, ['StageI', 'StageII', 'StageIII', 'StageIV']].plot(kind='bar', ax=ax, stacked=True)
    ax.set_title(adherence, fontsize=14, y = 1.025)
    ax.set_xticklabels(['I', 'II', 'III', 'IV'], rotation=0, fontsize=14)
    ax.set_ylim(0, 5500)

    # Put the values in the top of the bars as integers
    for p in ax.patches:
        ax.annotate(str(int(p.get_height())), (p.get_x() * 1.0 + 0.1, p.get_height() * 1.015), fontsize=14)

    # Add the total number of FIT and Colonoscopy at the bottom of each graph
    ax.text(0.8, -350, 'FIT: ' + str(format_with_spaces(int(costs.loc[adherence, 'FIT']))), fontsize=14)
    ax.text(0.8, -500, 'Colonoscopies: ' + str(format_with_spaces(int(costs.loc[adherence, 'Colonoscopy']))), fontsize=14)


    # Add text with PARAMETERS
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig.text(0.5, 0.95, 'FIT Sensitivity: ' + str(parameters['FIT_SENSITIVITY']) + ' FIT Specificity: ' + str(parameters['FIT_SPECIFICITY'])
    + ' Years: ' + str(parameters['YEARS_TO_SIMULATE']) + ' Prevalence: ' + str(parameters['CRC_PREVALENCE']),
    ha='center', va='center', fontsize=14, bbox=props)

    #plt.subplots_adjust(hspace=0.5, wspace=0.5, top=0.8)
    plt.subplots_adjust(hspace=0.4, wspace=0.5)
    plt.savefig('plots/treatments_for_example.png')

    # Make multiple pie graphs with all the costs: FIT, Colonoscopy, Stage I, Stage II, Stage III, Stage IV
    # Add the total cost at the bottom of each pie graph

    #to add percentages
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 5 else ''


    fig, ax = plt.subplots(1, figsize=(10, 8))
    adherences = costs.index
    adherences = [x for x in adherences]
    for i in range(1):
        adherence = adherences[i]
        #Only show pct if it is higher than 5%

        costs.loc[adherence, ['FIT Costs', 'Colonoscopy Costs', 'Stage I Costs', 'Stage II Costs', 'Stage III Costs', 'Stage IV Costs']].plot(kind='pie', ax=ax, startangle=90, legend=False, autopct=my_autopct, labels=None, fontsize=20, pctdistance=0.7)


        
        ax.set_title(adherence, y=0.92, fontsize=18)
        ax.set_ylabel('')
        total_cost_of_one_year = 0
        if costs.loc[adherence, 'YearsGained'] != 0:
            total_cost_of_one_year = costs.loc[adherence, 'Total Cost M CLP']/costs.loc[adherence, 'YearsGained']
        ax.text(-0.6, -1.35, 'Total Cost: ' + str(format_with_spaces(costs.loc[adherence, 'Total Cost M CLP']))
        + ' M CLP\nYears Gained: ' + str(format_with_spaces(int(costs.loc[adherence, 'YearsGained']))
        ), fontsize=18)

    # Make it horizontal
    fig.legend(loc=(0.15,0.877), labels=[ 
    'FIT', 'Colonoscopy', 'Stage I', 'Stage II', 'Stage III', 'Stage IV'], title='Costs', ncols=2 )

    # Add text with PARAMETERS
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig.text(0.7, 0.933, 'FIT Sensitivity: ' + str(parameters['FIT_SENSITIVITY']) + ' FIT Specificity: ' + str(parameters['FIT_SPECIFICITY']) 
    + ' \nPeriod: ' + str(parameters['STARTING_YEAR']) + '-' + str(parameters['STARTING_YEAR']+parameters['YEARS_TO_SIMULATE']) + ' Prevalence: ' + str(parameters['CRC_PREVALENCE'])
    + ' \n  FIT Cost: '  + str(format_with_spaces(parameters['FIT_COST'])) + ' CLP FIT Frequency: ' + str(parameters['SCREENING_FREQUENCY'][0]) + ' (' + str(parameters['SCREENING_FREQUENCY'][1]) + '-' + str(parameters['SCREENING_FREQUENCY'][2]) + ')'
    + ' \n Colonoscopy Cost: ' + str(format_with_spaces(parameters['COLONOSCOPY_COST'])) + ' CLP   Treatment Cost by Stage\n I:' + str(format_with_spaces(parameters['CANCER_TREATMENT_COSTS']['I'])) + ' CLP II:' + str(format_with_spaces(parameters['CANCER_TREATMENT_COSTS']['II'])) + ' CLP III:' + str(format_with_spaces(parameters['CANCER_TREATMENT_COSTS']['III'])) + ' CLP IV:' + str(format_with_spaces(parameters['CANCER_TREATMENT_COSTS']['IV'])) + 'CLP', 
    ha='center', va='center', fontsize=10, bbox=props, linespacing = 1.5 )


    plt.savefig('plots/costs_for_example.png', dpi=600)

costs_analysis()