import json

def format_with_spaces(n):
    n_str = str(n)[::-1]
    formatted_str = ' '.join(n_str[i:i+3] for i in range(0, len(n_str), 3))
    return formatted_str[::-1]


def costs_analysis():
    import pandas as pd
    file_names = [
        ['4.simulation_outputs/colonoscopy_421005/costs/costs_0_8.csv', 'Average\nColonoscopy Cost\n'+ str(format_with_spaces(421005)) + ' CLP'], 
        ['4.simulation_outputs/colonoscopy_333190/costs/costs_0_8.csv', 'Clínica Bupa\nColonoscopy Cost\n'+ str(format_with_spaces(333190)) + ' CLP'], 
        ['4.simulation_outputs/colonoscopy_425621/costs/costs_0_8.csv', 'UC Christus\nColonoscopy Cost\n'+ str(format_with_spaces(425621)) + ' CLP'], 
        ['4.simulation_outputs/colonoscopy_504205/costs/costs_0_8.csv', 'Clínica Alemana\nColonoscopy Cost\n'+ str(format_with_spaces(504205)) + ' CLP']
        ]

    # Path to your JSON file
    file_path = '4.simulation_outputs/colonoscopy_421005/parameters/simulation_parameters.json'

    # Read from file
    with open(file_path, 'r') as file:
        parameters = json.load(file)

    CRC_PREVALENCE = parameters['CRC_PREVALENCE']
    YEARS_TO_SIMULATE = parameters['YEARS_TO_SIMULATE']
    SCREENING_FREQUENCY = parameters['SCREENING_FREQUENCY']
    FIT_SENSITIVITY = parameters['FIT_SENSITIVITY']
    FIT_SPECIFICITY = parameters['FIT_SPECIFICITY']
    CANCER_TREATMENT_COSTS = parameters['CANCER_TREATMENT_COSTS']
    STARTING_YEAR = parameters['STARTING_YEAR']
    FIT_COST = parameters['FIT_COST']


    costs = pd.DataFrame(columns=['Total Cost M CLP',
    'Percentage Cost', 'DifferenceCosts',
    'FIT Costs', 'Colonoscopy Costs', 
    'Stage I Costs','Stage II Costs','Stage III Costs','Stage IV Costs',
    'Treatments', 'StageI', 'StageII', 'StageIII', 'StageIV',
    'StageI%', 'StageII%', 'StageIII%', 'StageIV%', 
    'YearsGained', 'AsymptomaticDiscoveries'])
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
        asymptomatic_discoveries = table['AsymtomaticCCRDiscovered'].sum()
        costs.loc[f[1]] = {'Total Cost M CLP': total_cost, 
        'Percentage Cost': 0.01, 'DifferenceCosts': 0, 
        'FIT Costs': fit_costs, 'Colonoscopy Costs': colonoscopy_costs,
        'Stage I Costs': stage_I_costs, 'Stage II Costs': stage_II_costs, 'Stage III Costs': stage_III_costs, 'Stage IV Costs': stage_IV_costs,
        'Treatments': cancer_treatments, 
        'StageI': cancer_stage_I_treatments, 'StageII': cancer_stage_II_treatments, 'StageIII': cancer_stage_III_treatments, 'StageIV': cancer_stage_IV_treatments,
        'StageI%': cancer_stage_I_pct, 'StageII%': cancer_stage_II_pct, 'StageIII%': cancer_stage_III_pct, 'StageIV%': cancer_stage_IV_pct, 
        'YearsGained': years_gained, 'AsymptomaticDiscoveries': asymptomatic_discoveries}

    print(costs.head)
    
    base_cost = costs.loc['Average\nColonoscopy Cost\n421 005 CLP']['Total Cost M CLP']
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


    costs.to_csv('4.simulation_outputs/colonoscopy_421005/costs_summary.csv', sep=';', encoding='utf-8', index=True)

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns


    # Make multiple pie graphs with all the costs: FIT, Colonoscopy, Stage I, Stage II, Stage III, Stage IV
    # Add the total cost at the bottom of each pie graph

    #to add percentages
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct > 5 else ''


    fig, ax = plt.subplots(1, 4)
    fig.set_size_inches(12, 6)
    adherences = costs.index
    adherences = [x for x in adherences]
    for i in range(4):
        adherence = adherences[i]
        #Only show pct if it is higher than 5%

        #costs.loc[adherence, ['FIT Costs', 'Colonoscopy Costs', 'Stage I Costs', 'Stage II Costs', 'Stage III Costs', 'Stage IV Costs']].plot(kind='pie', ax=ax[i, j], autopct='%1.1f%%', startangle=90, legend=False, labels=None)
        costs.loc[adherence, ['FIT Costs', 'Colonoscopy Costs', 'Stage I Costs', 'Stage II Costs', 'Stage III Costs', 'Stage IV Costs']].plot(kind='pie', ax=ax[i], startangle=90, legend=False, autopct=my_autopct, labels=None, fontsize=8, pctdistance=0.7)


        
        ax[i].set_title(adherence)
        ax[i].set_ylabel('')
        if costs.loc[adherence, 'DifferenceCosts'] != 0:
            costsDifferenceText = 'Cost Difference: ' + str(format_with_spaces(costs.loc[adherence, 'Percentage Cost'])) + '\n'
        else:
            costsDifferenceText = ''
        ax[i].text(-1, -2, 'Total Cost: ' + str(format_with_spaces(costs.loc[adherence, 'Total Cost M CLP'])) + ' M CLP'
        + '\nColonoscopy Costs: ' + str(format_with_spaces(int(costs.loc[adherence, 'Colonoscopy Costs'])) + ' M CLP'
        + '\n' + costsDifferenceText
        ), fontsize=10)

    # Make it horizontal
    fig.legend(loc=(0.15,0.837), labels=costs.columns[3:9], title='Costs', ncols=2 )

    # Add text with PARAMETERS
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig.text(0.7, 0.91, 'FIT Sensitivity: ' + str(FIT_SENSITIVITY) + ' FIT Specificity: ' + str(FIT_SPECIFICITY) 
    + ' \nPeriod: ' + str(STARTING_YEAR) + '-' + str(STARTING_YEAR + YEARS_TO_SIMULATE) + ' Prevalence: ' + str(CRC_PREVALENCE)
    + ' \n Adherence: 80' + str('%') + ' FIT Cost: '  + str(format_with_spaces(FIT_COST)) + ' CLP'
    + ' \n Avg. CRC Cost by Stage\n I:' + str(format_with_spaces(CANCER_TREATMENT_COSTS['I'])) + ' CLP II:' + str(format_with_spaces(CANCER_TREATMENT_COSTS['II'])) + ' CLP III:' + str(format_with_spaces(CANCER_TREATMENT_COSTS['III'])) + ' CLP IV:' + str(format_with_spaces(CANCER_TREATMENT_COSTS['IV'])) + 'CLP', 
    ha='center', va='center', fontsize=10, bbox=props)

    plt.savefig('4.analysis_plots/costs_colonoscopies', dpi=600)
    #plt.show()
    

costs_analysis()