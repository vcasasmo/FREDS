from genetic_algorithm import GeneticAlgorithm
from sensitivity_reader import GPTSensitivity, XGPTSensitivity


# Link between the .m file notation of the different perturbation and their MT format
notation_dict = {"total xs":"MT1", "ela scatt xs":"MT2", 
                 "fission xs": "MT18",  "capture xs":"MT102"}


# ---------------------- EXAMPLE WITH A GPT SENSITIVITY VECTOR ----------------------
# 1. Extracting the information on the sensitivity
sensitivity = GPTSensitivity( filepath        = "GPT/BFS_61_0_core_sens0.m",
                              observable      = "keff",
                              zai             = 942390, 
                              perts           = ["MT2", "MT18", "MT102"],
                              notation_dict   = notation_dict)

# 2. Optimisation through GA
ga = GeneticAlgorithm(33, sensitivity)
gen, fitness, chrom = ga.run_genetic_algorithm(seed=1)
# 3. Plot the sensitivities evaluated on the output grid
sensitivity.plot(chrom)


# ---------------------- EXAMPLE WITH A XGPT SENSITIVITY VECTOR ----------------------
# 1. Extracting the information on the sensitivity and eigenfunctions
sensitivity = XGPTSensitivity(filepath_xgpt   = "XGPT/Pu239/FC_Tf_1073_Tc_1073_sens0.m",
                              filepath_gpt    = "GPT/BFS_61_0_core_sens0.m",
                              filepath_eigfct = "XGPT/Pu239",
                              observable      = "keff",
                              zai             = 942390, 
                              perts           = ["MT2", "MT18", "MT102"],
                              notation_dict   = notation_dict)

# 2. Optimisation through GA
ga = GeneticAlgorithm(33, sensitivity)
gen, fitness, chrom = ga.run_genetic_algorithm(seed=1)

# 3. Plot the sensitivities evaluated on the output grid
sensitivity.plot(chrom)