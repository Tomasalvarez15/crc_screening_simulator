import pandas as pd

ccr_risk = pd.read_csv('initial_data/ccr_by_age.csv', sep=',', encoding='utf-8', low_memory=False)

print(ccr_risk.columns)

# Get year column split it and take the first element
ccr_risk['Start Year'] = ccr_risk['Age Group (years)']
ccr_risk['End Year'] = ccr_risk['Age Group (years)']

for row in ccr_risk.iterrows():
    year = row[1]['Age Group (years)']
    year = year.split('-')
    try:
        ccr_risk.loc[row[0], 'Start Year'] = year[0]
        ccr_risk.loc[row[0], 'End Year'] = year[1]
    except:
        ccr_risk.loc[row[0], 'Start Year'] = 0
        ccr_risk.loc[row[0], 'End Year'] = 0

# Convert to int
ccr_risk['Start Year'] = ccr_risk['Start Year'].astype(int)
ccr_risk['End Year'] = ccr_risk['End Year'].astype(int)

# Drop the Year column
ccr_risk.drop('Year', axis=1, inplace=True)

ccr_risk.to_csv('processed_data/ccr_risk.csv', index=False, header=True, sep=';')