# Both from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3415614/ Table 4
cancer_life_expectancy_by_stage = {
    'male': {'I': 25.3, 'II': 19.2, 'III': 13.6, 'IV': 2.1},
    'female': {'I': 29.8, 'II': 20.9, 'III': 16.8, 'IV': 2.2}
}

cancer_life_expectancy_by_age = {
    'male': [(50, 12.3), (65, 9.4), (85, 5.5)],
    'female': [(50, 13.3), (65, 11.5), (85, 4.1)]
}


def new_interpolate(value, points):
    """Linear interpolation or extrapolation for a value given a list of (x, y) points."""
    # If the value is below the first point, extrapolate using the slope of the first two points
    if value < points[0][0]:
        first_point = points[0]
        second_point = points[1]
        slope = (second_point[1] - first_point[1]) / (second_point[0] - first_point[0])
        return first_point[1] + (value - first_point[0]) * slope
    # For values within the range, interpolate as before
    for i, point in enumerate(points):
        if value < point[0]:
            prev_point = points[i - 1]
            return prev_point[1] + (value - prev_point[0]) * (point[1] - prev_point[1]) / (point[0] - prev_point[0])
    # If the value is above the last point, extrapolate using the slope of the last two points
    last_point = points[-1]
    second_last_point = points[-2]
    slope = (last_point[1] - second_last_point[1]) / (last_point[0] - second_last_point[0])
    return second_last_point[1] + (value - second_last_point[0]) * slope

def calculate_age_weight(age):
    """Calculates weight for age-based expectancy, linearly increasing from 0.5 to 0.8 between ages 50 and 85."""
    # Ensure age is within bounds
    #age = max(50, min(age, 85))
    # Linear interpolation for weight
    return 0.2 + 0.8 * ((age - 0) / 120)
    #return  age / 120

def cancer_life_expectancy_function(age, stage, sex):
    # Define the data
    age_data = cancer_life_expectancy_by_age[sex]
    stage_data = cancer_life_expectancy_by_stage[sex]
    
    # Interpolate life expectancy based on age
    age_le = new_interpolate(age, age_data)
    
    # Get life expectancy based on cancer stage directly
    # Assuming 'stage' is input as 'I', 'II', 'III', or 'IV'
    stage_le = stage_data[stage]
    
    # Combine the two estimates by averaging them
    result = 0
    
    age_weight = calculate_age_weight(age)
    stage_weight = 1 - age_weight

    result = int(age_weight * age_le + stage_weight * stage_le)

    if result < 0:
        result = 0

    return result


def get_crc_life_expectancies():
    etapas = ['I', 'II', 'III', 'IV']
    life_expectancies = {
        'male': { 'I': {}, 'II': {}, 'III': {}, 'IV': {}},
        'female': { 'I': {}, 'II': {}, 'III': {}, 'IV': {}}
    }
    for j in etapas:
        for i in range(120):
            life_expectancies['male'][j][i + 1] = cancer_life_expectancy_function(i + 1, j, 'male')
            life_expectancies['female'][j][i + 1] = cancer_life_expectancy_function(i + 1, j, 'female')
    return life_expectancies

def test_life_expectancy():
    etapas = ['I', 'II', 'III', 'IV']
    life_expectancies = get_crc_life_expectancies()
    print(life_expectancies)


    import matplotlib.pyplot as plt

    for stage, ages in life_expectancies['male'].items():
        plt.plot(list(ages.keys()), list(ages.values()), label=stage)




    plt.xlabel('Age')

    plt.ylabel('Life expectancy')

    # Put a line at 50 and 75
    plt.axvline(x=50, color='k', linestyle='--')

    plt.axvline(x=75, color='k', linestyle='--')

    # Write a text that says "Screening interval" between 50 and 75
    plt.text(45, 26, 'Screening interval')

    

    

    plt.legend()

    plt.savefig('crc_life_expectancies.png')

test_life_expectancy()
