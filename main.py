




import numpy as np
import pandas as pd
from genetic_algorithm import GeneticAlgorithm
import matplotlib.pyplot as plt
 
from pymoo.core.problem import Problem

from pymoo.optimize import minimize

from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from pymoo.visualization.scatter import Scatter
import time 
from pymoo.indicators.hv import HV

ref_point = np.array([1,1])

hv_indicator = HV(ref_point=ref_point)

n_var=32 #Maximum number of groups

class PerformanceMetrics:

    def __init__(self):
        self.generations = []
        self.best_fitness = []
        self.avg_fitness = []
        self.diversity = []
        self.start_time = time.time()
        self.runtime = []
        self.hypervolume=[]

    def record(self, algorithm):
        self.generations.append(len(self.generations))
        fitness_values = algorithm.pop.get("F")[:, 0]
        self.best_fitness.append(np.min(fitness_values))
        self.avg_fitness.append(np.mean(fitness_values))
        self.diversity.append(np.std(fitness_values))
        self.runtime.append(time.time() - self.start_time)
        self.hypervolume.append(hv_indicator(algorithm.pop.get("F")))

# Initialize metrics recorder
metrics = PerformanceMetrics()


class GridDesignMOO(Problem):

    def __init__(self):
        super().__init__(
            n_var=n_var,  # Number of decision variables
            n_obj=2,  # Two objectives: fitness and number of active variables
            n_constr=0,  # No constraints
            xl=1,  # Lower bound of variables
            xu=224,  # Upper bound of variables
            var_type=int  # Integer variables
        )
        # Initialize your genetic algorithm
        self.genetic_algo = GeneticAlgorithm(32, criteria='GPT')

    def _evaluate(self, x, out, *args, **kwargs):
        x = x.astype(np.int32)  # Ensure variables are integers
        fitness = np.zeros(x.shape[0])
        num_active_variables = np.zeros(x.shape[0])

        for individual in range(x.shape[0]):
            # Calculate fitness for the first objective
            fitness[individual] = self.genetic_algo.transfer_fitness(sorted(np.unique(x[individual])))
            # Calculate the number of active variables for the second objective
            num_active_variables[individual] = len(np.unique(x[individual]))/32

        out["F"] = np.column_stack([fitness, num_active_variables])  # Both objectives

problem = GridDesignMOO()

# Function to store convergence metrics
class ConvergenceMetrics:

    def __init__(self):
        self.generations = []
        self.best_fitness = []

    def record(self, algorithm):
        self.generations.append(len(self.generations))
        self.best_fitness.append(min(algorithm.pop.get("F")[:, 0]))

# Initialize metrics recorder
metrics = PerformanceMetrics()

# Modify NSGA-II to record metrics
algorithm = NSGA2(
    pop_size=500,  # Population size
    sampling=IntegerRandomSampling(),  # Random sampling for integer variables
    crossover=SBX(prob=0.8, eta=3.0, vtype=float, repair=RoundingRepair()),  # SBX crossover with rounding repair
    mutation=PM(prob=0.08, eta=3.0, vtype=float, repair=RoundingRepair()),  # Polynomial mutation with rounding repair
    eliminate_duplicates=True,  # Eliminate duplicates in the population
    n_offsprings=1000  # Number of offspring generated per generation
)

# Optimize the problem
res = minimize(
    problem,
    algorithm,
    ('n_gen', 100),  # Number of generations
    seed=333,
    verbose=True,  # Enable verbose output
    callback=metrics.record  # Record metrics at each generation

)

# Plot performance metrics
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.plot(metrics.generations, metrics.best_fitness, label='Best Fitness')
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Best Fitness Over Generations')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(metrics.generations, metrics.avg_fitness, label='Average Fitness', color='orange')
plt.xlabel('Generation')
plt.ylabel('Average Fitness')
plt.title('Average Fitness Over Generations')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(metrics.generations, metrics.diversity, label='Diversity', color='green')
plt.xlabel('Generation')
plt.ylabel('Diversity (Std Dev)')
plt.title('Diversity Over Generations')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(metrics.generations, metrics.hypervolume, label='Hypervolume', color='purple')
plt.xlabel('Generation')
plt.ylabel('Hypervolume')
plt.title('Hypervolume Over Generations')
plt.legend()


# Plot Pareto front
plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()




# Convert each row into a list
rows_as_lists = [list(np.unique(sorted(row))) for row in res.X]

# Convert the list of lists to a pandas DataFrame with a single column
df = pd.DataFrame({"Energy Grid": rows_as_lists})
df_F = pd.DataFrame(res.F, columns=["Fitness", "N_Groups"])
df["Fitness"] = df_F["Fitness"]
df["N_Groups"] = df_F["N_Groups"]*n_var
# Save the DataFrame to a CSV file
df.to_csv("./Results/{}_{}G_results.csv".format('GPT', n_var+1), index=False)

import sys
sys.path.append(r"\Energy_Grid_Design")
import plot_results as p
for row in range(res.X.shape[0]):  

    grid = np.unique(res.X[row,:])
    print(f"plotting grid with {grid.shape[0]} groups, Fitness { res.F[row,0]}")
    sorted_grid = sorted(grid.tolist()) 
    test_grid = {grid.shape[0]: # N groups
             {'test': # name -> prefix = "G" if label == "GPT" else "X" if label == "XGPT" else "V"; default nuclide is U238
              ('red', #color
               sorted_grid # bins
              )}}
    p.plot_grids(test_grid)
    plt.show()