import json

def format_with_spaces(n):
    n_str = str(n)[::-1]
    formatted_str = ' '.join(n_str[i:i+3] for i in range(0, len(n_str), 3))
    return formatted_str[::-1]


def costs_analysis():
    import pandas as pd
    file_names = [
        ['4.simulation_outputs/default_1/costs/costs_0_2.csv', 'Default 1'], 
        ['4.simulation_outputs/default_2/costs/costs_0_2.csv', 'Default 2'], 
        ['4.simulation_outputs/default_3/costs/costs_0_2.csv', 'Default 3'],
        ['4.simulation_outputs/default_4/costs/costs_0_2.csv', 'Default 4'],
        ['4.simulation_outputs/default_5/costs/costs_0_2.csv', 'Default 5'],
        ['4.simulation_outputs/default_6/costs/costs_0_2.csv', 'Default 6'],
        ['4.simulation_outputs/default_7/costs/costs_0_2.csv', 'Default 7'], 
        ['4.simulation_outputs/default_8/costs/costs_0_2.csv', 'Default 8'],
        ['4.simulation_outputs/default_9/costs/costs_0_2.csv', 'Default 9'],
        ['4.simulation_outputs/default_10/costs/costs_0_2.csv', 'Default 10']]

    costs = pd.DataFrame(columns=['Total Cost M CLP',
    'Percentage Cost', 'DifferenceCosts',
    'FIT', 'Colonoscopy',
    'FIT Costs', 'Colonoscopy Costs', 
    'Stage I Costs','Stage II Costs','Stage III Costs','Stage IV Costs',
    'Treatments', 'StageI', 'StageII', 'StageIII', 'StageIV',
    'StageI%', 'StageII%', 'StageIII%', 'StageIV%', 
    'YearsGained', 'HYearsGained', 'DFYearsGained', 'DALYGained',
    'AsymptomaticTreatments', 'SymptomaticTreatments'])

    # Path to your JSON file
    file_path = '4.simulation_outputs/1year/parameters/simulation_parameters.json'

    # Read from file
    with open(file_path, 'r') as file:
        parameters = json.load(file)

    CRC_PREVALENCE = parameters['CRC_PREVALENCE']
    YEARS_TO_SIMULATE = parameters['YEARS_TO_SIMULATE']
    FIT_SENSITIVITY = parameters['FIT_SENSITIVITY']
    FIT_SPECIFICITY = parameters['FIT_SPECIFICITY']
    CANCER_TREATMENT_COSTS = parameters['CANCER_TREATMENT_COSTS']
    STARTING_YEAR = parameters['STARTING_YEAR']
    FIT_COST = parameters['FIT_COST']
    COLONOSCOPY_COST = parameters['COLONOSCOPY_COST']

    for f in file_names:
        file_name = f[0]

        table = pd.read_csv(file_name, sep=';', encoding='utf-8', low_memory=False)
        print(table.columns)
        print(file_name)
        total_cost = table['Total'].sum()
        fit = table['Fit'].sum()
        colonoscopy = table['Colonoscopy'].sum()
        print('Colonoscopies', colonoscopy)
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
        healthy_years_gained = table['HYearsGained'].sum()
        disability_free_years_gained = table['DFYearsGained'].sum()
        daly_gained = table['DALYGained'].sum()
        asymptomatic_treatments = table['AsymtomaticCCRDiscovered'].sum()
        symptomatic_treatments = cancer_treatments - asymptomatic_treatments
        costs.loc[f[1]] = {'Total Cost M CLP': total_cost, 
        'Percentage Cost': 0.01, 'DifferenceCosts': 0,
        'FIT': fit, 'Colonoscopy': colonoscopy, 
        'FIT Costs': fit_costs, 'Colonoscopy Costs': colonoscopy_costs,
        'Stage I Costs': stage_I_costs, 'Stage II Costs': stage_II_costs, 'Stage III Costs': stage_III_costs, 'Stage IV Costs': stage_IV_costs,
        'Treatments': cancer_treatments, 
        'StageI': cancer_stage_I_treatments, 'StageII': cancer_stage_II_treatments, 'StageIII': cancer_stage_III_treatments, 'StageIV': cancer_stage_IV_treatments,
        'StageI%': cancer_stage_I_pct, 'StageII%': cancer_stage_II_pct, 'StageIII%': cancer_stage_III_pct, 'StageIV%': cancer_stage_IV_pct, 
        'YearsGained': years_gained, 'HYearsGained': healthy_years_gained, 'DFYearsGained': disability_free_years_gained, 'DALYGained': daly_gained,
        'AsymptomaticTreatments': asymptomatic_treatments, 'SymptomaticTreatments': symptomatic_treatments}

    print(costs.head)
    # Set the base cost as the Total Cost M CLP of the lowest default
    
    base_cost = costs.loc['Default 1']['Total Cost M CLP']
    for f in file_names:
        if costs.loc[f[1]]['Total Cost M CLP'] < base_cost:
            base_cost = costs.loc[f[1]]['Total Cost M CLP']
    

    for f in file_names:
        costs.loc[f[1],'Percentage Cost'] = (costs.loc[f[1]]['Total Cost M CLP']-base_cost)/base_cost
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


    costs.to_csv('4.simulation_outputs/default_1/costs_summary.csv', sep=';', encoding='utf-8', index=True)

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
    costs[['AsymptomaticTreatmentsPercentage', 'SymptomaticTreatmentsPercentage']].plot(kind='barh', ax=ax, stacked=True, color=['#1f77b4', '#ff7f0e'])
    ax.invert_yaxis()

    # Set the legend in the upper right corner
    ax.legend(loc='upper right', labels=['Asymptomatic', 'Symptomatic'])

    # Put the asymptomatic percentage in the bars
    for i, v in enumerate(costs['AsymptomaticTreatmentsPercentage']):
        ax.text(v, i, '{:.2%}'.format(v), ha='left', va='center', fontsize=8)
    

    plt.savefig('4.analysis_plots/screening_efficacy_for_defaults.png')

    # Print all the asymptomatic treatments percentages divided by the adherence percentage
    adherences_percentages = [0, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8]
    for i in range(8):
        adherences_percentage = adherences_percentages[i]
        asymptomatic_treatments = costs.loc[adherences[i], 'AsymptomaticTreatments']
        print(asymptomatic_treatments / adherences_percentage)



    

    # Make a multiple graphs by the adherence percentage with the stage treatments quantity

    fig, ax = plt.subplots(2, 5, figsize=(11, 7))
    #fig.position = (0, 6)
    adherences = costs.index
    adherences = [x for x in adherences]
    for i in range(2):
        for j in range(5):
            adherence = adherences[i*5+j]
            costs.loc[adherence, ['StageI', 'StageII', 'StageIII', 'StageIV']].plot(kind='bar', ax=ax[i, j], stacked=True)
            ax[i, j].set_title(adherence, fontsize=10)
            ax[i, j].set_xticklabels(['I', 'II', 'III', 'IV'], rotation=0)
            ax[i, j].set_ylim(0, 5500)

            # Put the values in the top of the bars as integers
            for p in ax[i, j].patches:
                ax[i, j].annotate(str(int(p.get_height())), (p.get_x() * 0.93, p.get_height() * 1.015), fontsize=10)

            # Add the total number of FIT and Colonoscopy at the bottom of each graph
            ax[i, j].text(-0.5, -950, 'FIT: ' + str(format_with_spaces(int(costs.loc[adherence, 'FIT']))), fontsize=10)
            ax[i, j].text(-0.5, -1250, 'Colonoscopies: ' + str(format_with_spaces(int(costs.loc[adherence, 'Colonoscopy']))), fontsize=10)


    # Add text with PARAMETERS
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig.text(0.5, 0.95, 'FIT Sensitivity: ' + str(parameters['FIT_SENSITIVITY']) + ' FIT Specificity: ' + str(parameters['FIT_SPECIFICITY'])
    + ' Years: ' + str(parameters['YEARS_TO_SIMULATE']) + ' Prevalence: ' + str(parameters['CRC_PREVALENCE']),
    ha='center', va='center', fontsize=10, bbox=props)

    #plt.subplots_adjust(hspace=0.5, wspace=0.5, top=0.8)
    plt.subplots_adjust(hspace=0.4, wspace=0.5)
    plt.savefig('4.analysis_plots/treatments_for_defaults.png')

    # Make multiple pie graphs with all the costs: FIT, Colonoscopy, Stage I, Stage II, Stage III, Stage IV
    # Add the total cost at the bottom of each pie graph

    #to add percentages
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 5 else ''


    fig, ax = plt.subplots(2, 5)
    fig.set_size_inches(14, 8)
    adherences = costs.index
    adherences = [x for x in adherences]
    for i in range(2):
        for j in range(5):
            adherence = adherences[i*5+j]
            #Only show pct if it is higher than 5%

            #costs.loc[adherence, ['FIT Costs', 'Colonoscopy Costs', 'Stage I Costs', 'Stage II Costs', 'Stage III Costs', 'Stage IV Costs']].plot(kind='pie', ax=ax[i, j], autopct='%1.1f%%', startangle=90, legend=False, labels=None)
            costs.loc[adherence, ['FIT Costs', 'Colonoscopy Costs', 'Stage I Costs', 'Stage II Costs', 'Stage III Costs', 'Stage IV Costs']].plot(kind='pie', ax=ax[i, j], startangle=90, legend=False, autopct=my_autopct, labels=None, fontsize=8, pctdistance=0.7)


            
            ax[i, j].set_title(adherence)
            ax[i, j].set_ylabel('')
            total_cost_of_one_year = 0
            if costs.loc[adherence, 'DifferenceCosts'] != 0:
                costsDifferenceText = 'Cost Difference: ' + str(format_with_spaces(costs.loc[adherence, 'Percentage Cost'])) + '\n'
            else:
                costsDifferenceText = ''
            MCLP_per_DALY = ''
            if costs.loc[adherence, 'YearsGained'] != 0:
                total_cost_of_one_year = costs.loc[adherence, 'Total Cost M CLP']/costs.loc[adherence, 'YearsGained']
                MCLP_per_DALY = '\nCost per DALY: ' + str(round(costs.loc[adherence, 'DifferenceCosts']/costs.loc[adherence, 'DALYGained'], 2)) + ' M CLP'
            ax[i, j].text(-1, -2, 'Total Cost: ' + str(format_with_spaces(costs.loc[adherence, 'Total Cost M CLP']))
            + ' M CLP\n' + costsDifferenceText
            #+  'Years Gained: ' + str(format_with_spaces(int(costs.loc[adherence, 'YearsGained']))
            + 'DALYs gained: ' + str(format_with_spaces(int(costs.loc[adherence, 'DALYGained'])))
            #+ MCLP_per_DALY
            )

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


    plt.savefig('4.analysis_plots/costs_for_defaults.png', dpi=600)

    

costs_analysis()