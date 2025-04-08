
from irace import irace
import numpy as np
from genetic_algorithm import GeneticAlgorithm

parameters_table = '''
pm "--mutation_rate" r (0.001, 0.05)
soft_mutation "--soft_mutation" r (0.5, 1)
pc "--crossover_rate" r (0.75, 1) 
p "--parameter p" r (0.001, 1)
elitism "--elitism" r (0.01, 0.1)
multiparent "--multiparent" c (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
adaptiveMR "--adaptive" c (1, 0)
popsize "--popsize" c (50, 100, 150, 200, 250, 400, 450, 500)
no_tournaments "--no_tournaments" c (1, 0)
NT "--NT" c (1, 5, 10, 50, 100)
'''
#Reconfigure for Pymoo NSGA-II/III?
instances = np.arange(10)

scenario = dict(
    instances = instances,
    maxExperiments = 500,
    debugLevel = 3,
    digits = 5,
    parallel= 4, 
    logFile = "")

def target_runner(experiment, scenario):
    experiment = experiment["configuration"]
    seed = experiment["seed"]
    nGroup = 33
    popsize = experiment["popsize"]
    pm = experiment["pm"]
    pc = experiment["pc"]
    no_tournament = True if int(experiment["no_tournaments"])==1 else False
    soft_mutation = experiment["soft_mutation"]
    p = experiment["p"]
    NT = int(experiment["NT"])
    elitism = experiment["elitism"]
    multi_parent = None if int(experiment["multiparent"]) == 1 else int(experiment["multiparent"])
    adaptive = True if int(experiment["adaptiveMR"])==1 else False

    GA = GeneticAlgorithm(nGroup, criteria = "GPT", pop_size=popsize, 
                          pm = pm, pc = pc, no_tournament=no_tournament,
                            elitism = elitism, adaptive = adaptive,
                              soft_mutation = soft_mutation, p=p, NT=NT,
                                multi_parent = multi_parent  )

    _, best_fitness, _ = GA.run_genetic_algorithm(seed)
    return dict(cost=best_fitness)

tuner = irace(scenario, parameters_table, target_runner)    
best_confs = tuner.run()

print(best_confs)