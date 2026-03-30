# MiCSS (Micro Colorectal Cancer Screening Simulator)
Copyright (C) 2024 Tomás Álvarez

MiCSS is a microsimulation model designed to evaluate the cost-effectiveness of colorectal cancer (CRC) screening strategies. The model simulates the natural history of CRC and the screening process for individuals in a defined population. MiCSS is intended to assist policymakers and healthcare professionals in making informed decisions regarding CRC screening programs.

## Features
- Simulates the lives of individuals within a specified population.
- Evaluates the cost-effectiveness of CRC screening strategies.
- Allows for the analysis of different screening scenarios and adherence rates.
- Provides insights into the impact of screening on CRC prognosis and healthcare costs.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Folder Structure

Folders with a `1.` prefix contain demographic data:
- `1.initial_data/`: Raw demographic data.
- `1.data_preprocessing_functions/`: Python scripts that preprocess raw data and create plots.
- `1.processed_data/`: Results of preprocessing.

Folders with a `2.` prefix contain the simulation code:
- `2.simulation/`: All simulation code:
  - `population.py`: Population simulation class.
  - `person.py`: Individual characteristics and behaviors.
  - `parameters.py`: Default simulation parameters.
  - `crc_life_expectancy.py`: CRC life expectancy calculations.
  - `life_expectancy.py`: General life expectancy calculations.
  - `1.main.py`: Scenario runner (config-driven).

Folders with a `3.` prefix contain scenario analysis:
- `3.scenario_analysis/`: Scripts for analyzing simulation outputs.

Folders with a `4.` prefix contain outputs:
- `4.simulation_outputs/`: CSV results for each scenario.
- `4.analysis_plots/`: Plots generated from scenario analysis.
- `4.data_plots/`: Plots from demographic data analysis.

## Usage

1. Install dependencies (see Installation above).
2. From the project root, run the simulation:
   ```bash
   python 2.simulation/1.main.py
   ```
   This executes all scenarios and saves results under `4.simulation_outputs/`. Existing scenario folders are skipped automatically.
3. Run analysis scripts in `3.scenario_analysis/` to generate plots.

## Testing

```bash
pytest tests/
```

## Model Validation
The model has undergone partial validation. Further validation is recommended following the techniques described by [Eddy et al., 2012](https://www.valueinhealthjournal.com/article/S1098-3015(12)01656-7/fulltext).

## Reusability
While initially designed for CRC screening in the southern district of Santiago, Chile, the model can be adapted to other healthcare settings. Researchers are encouraged to improve upon and utilize this model.

## Contact
For questions or feedback, please contact Tomás Álvarez at toalvarez@uc.cl.
