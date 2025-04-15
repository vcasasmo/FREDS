from genetic_algorithm import GeneticAlgorithm
from sensitivity_reader import GPTSensitivity


# Extracting the information on the sensitivity
sensitivity = GPTSensitivity( filepath="GPT/BFS_61_0_core_sens0.m",
                                observable="keff",
                                zai=922380, 
                                perts=["fission xs", "ela scatt xs", "capture xs"])


# Optimisation through GA
ga = GeneticAlgorithm(33, sensitivity, "GPT")
gen, fitness, chrom = ga.run_genetic_algorithm(seed=1)

# Plot the sensitivities evaluated on the output grid
sensitivity.plot(chrom)