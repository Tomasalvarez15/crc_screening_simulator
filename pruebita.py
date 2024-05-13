import json

# Path to your JSON file
file_path = 'simulations/default/parameters/simulation_parameters.json'

# Read from file
with open(file_path, 'r') as file:
    parameters = json.load(file)

# Now `parameters` is a Python dictionary containing your simulation parameters
# You can access your parameters like so:
print(parameters) 