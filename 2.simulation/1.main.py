from population import Population
import os

# Start counting the time
import time
start_time = time.time()

adherence_percentage_list = [0, 0.05, 0.1, 0.15, 0.2, 0.4, 0.6, 0.8]

if not os.path.exists('../4.simulation_outputs/default'):
    for adherence_percentage in adherence_percentage_list:
        default = Population(adherence_percentage, 'default')
        default.simulate()


        print("--- %s seconds ---" % int((time.time() - start_time)))
else:
    print('The default folder already exists')

if not os.path.exists('../4.simulation_outputs/default200'):
    for adherence_percentage in adherence_percentage_list:
        default = Population(adherence_percentage, 'default200')
        default.years_to_simulate = 200
        default.simulate()


        print("--- %s seconds ---" % int((time.time() - start_time)))
else:
    print('The default200 folder already exists')

# Defaults
# 1
if not os.path.exists('../4.simulation_outputs/default_1'):
    for adherence_percentage in adherence_percentage_list:
        default_1 = Population(adherence_percentage, 'default_1')
        default_1.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default folder already exists')

# 2
if not os.path.exists('../4.simulation_outputs/default_2'):
    for adherence_percentage in adherence_percentage_list:
        default_2 = Population(adherence_percentage, 'default_2')
        default_2.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default folder already exists')
# 3
if not os.path.exists('../4.simulation_outputs/default_3'):
    for adherence_percentage in adherence_percentage_list:
        default_3 = Population(adherence_percentage, 'default_3')
        default_3.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_3 folder already exists')

# 4
if not os.path.exists('../4.simulation_outputs/default_4'):
    for adherence_percentage in adherence_percentage_list:
        default_4 = Population(adherence_percentage, 'default_4')
        default_4.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_4 folder already exists')

# 5
if not os.path.exists('../4.simulation_outputs/default_5'):
    for adherence_percentage in adherence_percentage_list:
        default_5 = Population(adherence_percentage, 'default_5')
        default_5.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_5 folder already exists')

# 6
if not os.path.exists('../4.simulation_outputs/default_6'):
    for adherence_percentage in adherence_percentage_list:
        default_6 = Population(adherence_percentage, 'default_6')
        default_6.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_6 folder already exists')

# 7
if not os.path.exists('../4.simulation_outputs/default_7'):
    for adherence_percentage in adherence_percentage_list:
        default_7 = Population(adherence_percentage, 'default_7')
        default_7.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_7 folder already exists')

# 8
if not os.path.exists('../4.simulation_outputs/default_8'):
    for adherence_percentage in adherence_percentage_list:
        default_8 = Population(adherence_percentage, 'default_8')
        default_8.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_8 folder already exists')

# 9
if not os.path.exists('../4.simulation_outputs/default_9'):
    for adherence_percentage in adherence_percentage_list:
        default_9 = Population(adherence_percentage, 'default_9')
        default_9.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_9 folder already exists')

# 10
if not os.path.exists('../4.simulation_outputs/default_10'):
    for adherence_percentage in adherence_percentage_list:
        default_10 = Population(adherence_percentage, 'default_10')
        default_10.simulate()


        print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The default_10 folder already exists')
# I. Screening Frequency
# 1. 1 year
if not os.path.exists('../4.simulation_outputs/1year'):
    year1 = Population(0.8, '1year')
    year1.years_to_simulate = 200
    year1.screening_frequency = ['Annual', 50, 75, 1, 0]
    year1.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 1year folder already exists')

# 2. 2 years
if not os.path.exists('../4.simulation_outputs/2year'):
    year2 = Population(0.8, '2year')
    year2.years_to_simulate = 200
    year2.screening_frequency = ['Biennial', 50, 75, 2, 0]
    year2.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 2year folder already exists')

# 3. 3 years
if not os.path.exists('../4.simulation_outputs/3year'):
    year3 = Population(0.8, '3year')
    year3.years_to_simulate = 200
    year3.screening_frequency = ['Triennial', 50, 75, 3, 1]
    year3.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 3year folder already exists')

# 4. 4 years
if not os.path.exists('../4.simulation_outputs/4year'):
    year4 = Population(0.8, '4year')
    year4.years_to_simulate = 200
    year4.screening_frequency = ['Quadrennial', 50, 75, 4, 2]
    year4.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 4year folder already exists')

# 5. 5 years
if not os.path.exists('../4.simulation_outputs/5year'):
    year5 = Population(0.8, '5year')
    year5.years_to_simulate = 200
    year5.screening_frequency = ['Quinquennial', 50, 75, 5, 0]
    year5.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The 5year folder already exists')


# II. First round of intervals
# 1. 50-75
if not os.path.exists('../4.simulation_outputs/interval50_75'):
    interval50_75 = Population(0.8, 'interval50_75')
    interval50_75.years_to_simulate = 200
    interval50_75.screening_frequency = ['Biennial', 50, 75, 2, 0]
    interval50_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-75 folder already exists')

# 2. 45-80
if not os.path.exists('../4.simulation_outputs/interval45_80'):
    interval45_80 = Population(0.8, 'interval45_80')
    interval45_80.years_to_simulate = 200
    interval45_80.screening_frequency = ['Biennial', 45, 80, 2, 1]
    interval45_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 45-80 folder already exists')

# 3. 40-85
if not os.path.exists('../4.simulation_outputs/interval40_85'):
    interval40_85 = Population(0.8, 'interval40_85')
    interval40_85.years_to_simulate = 200
    interval40_85.screening_frequency = ['Biennial', 40, 85, 2, 0]
    interval40_85.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 40-85 folder already exists')

# 4. 35-90
if not os.path.exists('../4.simulation_outputs/interval35_90'):
    interval35_90 = Population(0.8, 'interval35_90')
    interval35_90.years_to_simulate = 200
    interval35_90.screening_frequency = ['Biennial', 35, 90, 2, 1]
    interval35_90.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 35-90 folder already exists')


# III. Second round of intervals
# OG 50-75
# 1. 45-75
if not os.path.exists('../4.simulation_outputs/interval45_75'):
    interval45_75 = Population(0.8, 'interval45_75')
    interval45_75.years_to_simulate = 200
    interval45_75.screening_frequency = ['Biennial', 45, 75, 2, 1]
    interval45_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 45-75 folder already exists')

# 2. 40-75
if not os.path.exists('../4.simulation_outputs/interval40_75'):
    interval40_75 = Population(0.8, 'interval40_75')
    interval40_75.years_to_simulate = 200
    interval40_75.screening_frequency = ['Biennial', 40, 75, 2, 0]
    interval40_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 40-75 folder already exists')

# 3. 50-80
if not os.path.exists('../4.simulation_outputs/interval50_80'):
    interval50_80 = Population(0.8, 'interval50_80')
    interval50_80.years_to_simulate = 200
    interval50_80.screening_frequency = ['Biennial', 50, 80, 2, 0]
    interval50_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-80 folder already exists')

# 4. 50-85
if not os.path.exists('../4.simulation_outputs/interval50_85'):
    interval50_85 = Population(0.8, 'interval50_85')
    interval50_85.years_to_simulate = 200
    interval50_85.screening_frequency = ['Biennial', 50, 85, 2, 0]
    interval50_85.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-85 folder already exists')

# 5. 40-80
if not os.path.exists('../4.simulation_outputs/interval40_80'):
    interval40_80 = Population(0.8, 'interval40_80')
    interval40_80.years_to_simulate = 200
    interval40_80.screening_frequency = ['Biennial', 40, 80, 2, 0]
    interval40_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 40-80 folder already exists')

# 6. 35-80
if not os.path.exists('../4.simulation_outputs/interval35_80'):
    interval35_80 = Population(0.8, 'interval35_80')
    interval35_80.years_to_simulate = 200
    interval35_80.screening_frequency = ['Biennial', 35, 80, 2, 1]
    interval35_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 35-80 folder already exists')

# 7. 45-85
if not os.path.exists('../4.simulation_outputs/interval45_85'):
    interval45_85 = Population(0.8, 'interval45_85')
    interval45_85.years_to_simulate = 200
    interval45_85.screening_frequency = ['Biennial', 45, 85, 2, 1]
    interval45_85.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 45-85 folder already exists')

# 8. 55-75
if not os.path.exists('../4.simulation_outputs/interval55_75'):
    interval55_75 = Population(0.8, 'interval55_75')
    interval55_75.years_to_simulate = 200
    interval55_75.screening_frequency = ['Biennial', 55, 75, 2, 1]
    interval55_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 55-75 folder already exists')

# 9. 50-70
if not os.path.exists('../4.simulation_outputs/interval50_70'):
    interval50_70 = Population(0.8, 'interval50_70')
    interval50_70.years_to_simulate = 200
    interval50_70.screening_frequency = ['Biennial', 50, 70, 2, 0]
    interval50_70.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 50-70 folder already exists')

# 9. 60-75
if not os.path.exists('../4.simulation_outputs/interval60_75'):
    interval60_75 = Population(0.8, 'interval60_75')
    interval60_75.years_to_simulate = 200
    interval60_75.screening_frequency = ['Biennial', 60, 75, 2, 0]
    interval60_75.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 60-75 folder already exists')

# 10. 55-80
if not os.path.exists('../4.simulation_outputs/interval55_80'):
    interval55_80 = Population(0.8, 'interval55_80')
    interval55_80.years_to_simulate = 200
    interval55_80.screening_frequency = ['Biennial', 55, 80, 2, 1]
    interval55_80.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval 55-80 folder already exists')

# IV. Colonoscopy Costs
if not os.path.exists('../4.simulation_outputs/colonoscopy_421005'):
    colonoscopy_421005 = Population(0.8, 'colonoscopy_421005')
    colonoscopy_421005.colonoscopy_cost = 421005
    colonoscopy_421005.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The colonoscopy_421005 folder already exists')

if not os.path.exists('../4.simulation_outputs/colonoscopy_504205'):
    colonoscopy_504205 = Population(0.8, 'colonoscopy_504205')
    colonoscopy_504205.colonoscopy_cost = 504205
    colonoscopy_504205.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval colonoscopy_504205 folder already exists')

if not os.path.exists('../4.simulation_outputs/colonoscopy_425621'):
    colonoscopy_425621 = Population(0.8, 'colonoscopy_425621')
    colonoscopy_425621.colonoscopy_cost = 425621
    colonoscopy_425621.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The colonoscopy_425621 folder already exists')

if not os.path.exists('../4.simulation_outputs/colonoscopy_333190'):
    colonoscopy_333190 = Population(0.8, 'colonoscopy_333190')
    colonoscopy_333190.colonoscopy_cost = 333190
    colonoscopy_333190.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The colonoscopy_333190 folder already exists')


# V. FIT Sensitivity
# 1. Improve Sensitivity
if not os.path.exists('../4.simulation_outputs/improved_sensitivity'):
    improved_sensitivity = Population(0.8, 'improved_sensitivity')
    improved_sensitivity.fit_sensitivity = 0.85
    improved_sensitivity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The improved_sensitivity folder already exists')

# 2. Worse Sensitivity
if not os.path.exists('../4.simulation_outputs/worse_sensitivity'):
    worse_sensitivity = Population(0.8, 'worse_sensitivity')
    worse_sensitivity.fit_sensitivity = 0.73
    worse_sensitivity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The worse_sensitivity folder already exists')


# VI. FIT Specificity
# 1. Improve Specificity
if not os.path.exists('../4.simulation_outputs/improved_specificity'):
    improved_specificity = Population(0.8, 'improved_specificity')
    improved_specificity.fit_specificity = 0.96
    improved_specificity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The improved_specificity folder already exists')

# 2. Worse Specificity
if not os.path.exists('../4.simulation_outputs/worse_specificity'):
    worse_specificity = Population(0.8, 'worse_specificity')
    worse_specificity.fit_specificity = 0.92
    worse_specificity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The worse_specificity folder already exists')

# 3. Super Improved Specificity
if not os.path.exists('../4.simulation_outputs/super_improved_specificity'):
    super_improved_specificity = Population(0.8, 'super_improved_specificity')
    super_improved_specificity.fit_specificity = 0.999
    super_improved_specificity.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The super_improved_specificity folder already exists')

print("--- %s minutes ---" % int((time.time() - start_time)/60))

# VII. FIT Costs
if not os.path.exists('../4.simulation_outputs/fit_5865'):
    fit_5865 = Population(0.8, 'fit_5865')
    fit_5865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_5865 folder already exists')

if not os.path.exists('../4.simulation_outputs/fit_4865'):
    fit_4865 = Population(0.8, 'fit_4865')
    fit_4865.fit_cost_cost = 4865
    fit_4865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The interval fit_4865 folder already exists')

if not os.path.exists('../4.simulation_outputs/fit_3865'):
    fit_3865 = Population(0.8, 'fit_3865')
    fit_3865.fit_cost = 3865
    fit_3865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_3865 folder already exists')

if not os.path.exists('../4.simulation_outputs/fit_6865'):
    fit_6865 = Population(0.8, 'fit_6865')
    fit_6865.fit_cost = 6865
    fit_6865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_6865 folder already exists')

if not os.path.exists('../4.simulation_outputs/fit_2865'):
    fit_2865 = Population(0.8, 'fit_2865')
    fit_2865.fit_cost = 2865
    fit_2865.simulate()
    print("--- %s minutes ---" % int((time.time() - start_time)/60))
else:
    print('The fit_2865 folder already exists')