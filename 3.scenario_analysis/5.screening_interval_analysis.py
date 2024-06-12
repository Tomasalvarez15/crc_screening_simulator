import json

def format_with_spaces(n):
    n_str = str(n)[::-1]
    formatted_str = ' '.join(n_str[i:i+3] for i in range(0, len(n_str), 3))
    return formatted_str[::-1]


def costs_analysis():
    import pandas as pd
    file_names = [
        ['4.simulation_outputs/interval60_75/costs/costs_0_8.csv', '60-75\n(15)'],
        ['4.simulation_outputs/interval50_70/costs/costs_0_8.csv', '50-70\n(20)'],
        ['4.simulation_outputs/interval55_75/costs/costs_0_8.csv', '55-75\n(20)'],
        ['4.simulation_outputs/interval50_75/costs/costs_0_8.csv', '50-75\n(25)'],
        ['4.simulation_outputs/interval55_80/costs/costs_0_8.csv', '55-80\n(25)'],
        ['4.simulation_outputs/interval50_80/costs/costs_0_8.csv', '50-80\n(30)'], 
        ['4.simulation_outputs/interval45_75/costs/costs_0_8.csv', '45-75\n(30)'],
        ['4.simulation_outputs/interval45_80/costs/costs_0_8.csv', '45-80\n(35)'], 
        ['4.simulation_outputs/interval40_85/costs/costs_0_8.csv', '40-85\n(45)'],
        ['4.simulation_outputs/interval35_90/costs/costs_0_8.csv', '35-90\n(55)']
        ]

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
    file_path = '4.simulation_outputs/interval50_75/parameters/simulation_parameters.json'

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
    
    base_cost = costs.loc['50-75\n(25)']['Total Cost M CLP']
    base_years = costs.loc['50-75\n(25)']['YearsGained']
    base_daly = costs.loc['50-75\n(25)']['DALYGained']
    for f in file_names:
        costs.loc[f[1],'Percentage Cost'] = costs.loc[f[1]]['Total Cost M CLP']/base_cost
        costs.loc[f[1], 'Inverted Percentage Cost'] = 1-costs.loc[f[1],'Percentage Cost']
        costs.loc[f[1],'DifferenceCosts'] = costs.loc[f[1]]['Total Cost M CLP'] - base_cost


        costs.loc[f[1], 'Percentage Years'] = costs.loc[f[1]]['YearsGained']/base_years
        costs.loc[f[1], 'Percentage DALY'] = costs.loc[f[1]]['DALYGained']/base_daly

        costs.loc[f[1], 'Inverted Percentage Years'] = 1-costs.loc[f[1], 'Percentage Years']
        costs.loc[f[1], 'Inverted Percentage DALY'] = 1-costs.loc[f[1], 'Percentage DALY']

        if costs.loc[f[1], 'Inverted Percentage DALY'] == 0:
            pass
        elif costs.loc[f[1], 'Percentage DALY'] > 1:
            costs.loc[f[1], 'Efficacy Ratio'] = (1 - costs.loc[f[1], 'Percentage DALY'])/(1 - costs.loc[f[1],'Percentage Cost'])
        else:
            print(costs.loc[f[1], 'Inverted Percentage DALY'])
            print(costs.loc[f[1], 'Inverted Percentage Cost'])
            costs.loc[f[1], 'Efficacy Ratio'] = costs.loc[f[1], 'Inverted Percentage DALY']/costs.loc[f[1], 'Inverted Percentage Cost']

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

    # Reorder columns in this order
    # Interval, Total Cost M CLP, Percentage Cost, Inverted Percentage Cost, DALY Gained, Percentage DALY, Inverted Percentage DALY, Efficacy Ratio
    costs = costs[['Total Cost M CLP', 'Percentage Cost', 'Inverted Percentage Cost', 'DifferenceCosts', 'DALYGained', 'Percentage DALY', 'Inverted Percentage DALY', 'Efficacy Ratio', 'YearsGained', 'Percentage Years', 'Inverted Percentage Years', 'AsymptomaticTreatments', 'SymptomaticTreatments', 'Cancer Treatments', 'StageI', 'StageII', 'StageIII', 'StageIV', 'StageI%', 'StageII%', 'StageIII%', 'StageIV%', 'HYearsGained', 'DFYearsGained']]

    # Round percentages to 3 decimals
    costs['Percentage Cost'] = costs['Percentage Cost'].apply(lambda x: '{:.2%}'.format(x))
    costs['Inverted Percentage Cost'] = costs['Inverted Percentage Cost'].apply(lambda x: '{:.2%}'.format(x))
    costs['Percentage DALY'] = costs['Percentage DALY'].apply(lambda x: '{:.2%}'.format(x))
    costs['Inverted Percentage DALY'] = costs['Inverted Percentage DALY'].apply(lambda x: '{:.2%}'.format(x))
    
    # Round Efficacy Ratio but no percentage
    costs['Efficacy Ratio'] = costs['Efficacy Ratio'].apply(lambda x: '{:.2f}'.format(x))

    # Format Total Cost M CLP with format_with_spaces
    costs['Total Cost M CLP'] = costs['Total Cost M CLP'].apply(lambda x: format_with_spaces(x))

    # Format DALY Gained into int and with format_with_spaces
    costs['DALYGained'] = costs['DALYGained'].apply(lambda x: format_with_spaces(str(int(x))))


    costs.to_csv('4.simulation_outputs/interval50_75/costs_summary.csv', sep=';', encoding='utf-8', index=True)

    
    

costs_analysis()