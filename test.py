from genetic_algorithm import GeneticAlgorithm
from sensitivity_reader import GPTSensitivity


# Extracting the information on the sensitivity
sensitivity = GPTSensitivity( filepath="FREDS/GPT/BFS_61_0_core_sens0.m",
                                observable="keff",
                                zai=922380, 
                                perts=["fission xs", "ela scatt xs", "capture xs"])


# Optimisation through GA
ga = GeneticAlgorithm(33, sensitivity, "GPT")
gen, fitness, chrom = ga.run_genetic_algorithm(seed=1)

#  Plot
sensitivity.set_ga_grid(chrom)
sensitivity.plot()