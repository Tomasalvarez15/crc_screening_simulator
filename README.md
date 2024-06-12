# MiCSS (Micro Colorectal Cancer Screening Simulator)

MiCSS is a microsimulation model designed to evaluate the cost-effectiveness of colorectal cancer (CRC) screening strategies. The model simulates the natural history of CRC and the screening process for individuals in a defined population. MiCSS is intended to assist policymakers and healthcare professionals in making informed decisions regarding CRC screening programs.

## Features
- Simulates the lives of individuals within a specified population.
- Evaluates the cost-effectiveness of CRC screening strategies.
- Allows for the analysis of different screening scenarios and adherence rates.
- Provides insights into the impact of screening on CRC prognosis and healthcare costs.

## Usage
0. Before running new simulations, delete all folders within the `simulations` folder. If these folders are not removed, the program will detect them as completed simulations and will not rerun them.
1. Run the `1.simulation.py` file. This script executes multiple scenarios and saves each scenario's results in its own folder within the `simulations` directory.
2. Run the remaining numbered scripts to analyze the outcomes of the scenarios. These scripts will generate plots and save them in the `plots` folder.

## Model Validation
The model has undergone partial validation by the researcher. Further validation is recommended following the techniques described in the study by [Eddy et al. ,2012](https://www.valueinhealthjournal.com/article/S1098-3015(12)01656-7/fulltext?_returnURL=https%3A%2F%2Flinkinghub.elsevier.com%2Fretrieve%2Fpii%2FS1098301512016567%3Fshowall%3Dtrue)

## Reusability
While initially designed for CRC screening in the southern district of Santiago, Chile, the model holds potential for adaptation to other healthcare settings and conditions. Researchers are encouraged to improve upon and utilize this model for various diseases and locations.

## Contact
For questions or feedback, please contact Tomás Álvarez at toalvarez@uc.cl .
