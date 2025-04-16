import numpy as np
import pandas as pd
from fitnessFunctions import CosineSimilarityGPT, CosineSimilarityXGPT
import matplotlib.pyplot as plt
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
import seaborn as sns
import time
from pymoo.indicators.hv import HV
import shutil

from sensitivity_reader import GPTSensitivity
import os
import pandas as pd





class Freds:

    def __init__(self):
        self.problem = None
        self.metrics = self.PerformanceMetrics()
        self.sensitivities = None
        self.optimize_groups = False
        self.result = None
        self.df_results = None


    class PerformanceMetrics:
        def __init__(self):
            self.generations = []
            self.best_fitness = []
            self.avg_fitness = []
            self.diversity = []
            self.start_time = time.time()
            self.runtime = []
            self.hypervolume = []

        def record(self, algorithm):
            fitness_values = algorithm.pop.get("F")[:, 0]
            self.generations.append(len(self.generations))
            self.best_fitness.append(np.min(fitness_values))
            self.avg_fitness.append(np.mean(fitness_values))
            self.diversity.append(np.std(fitness_values))
            self.runtime.append(time.time() - self.start_time)

            hv = HV(ref_point=np.ones(algorithm.pop.get("F").shape[1]))
            self.hypervolume.append(hv(algorithm.pop.get("F")))

    class SetProblemMOO(Problem):
        def __init__(self,
                     n_groups=32,
                     sensitivities=None,
                     criteria='GPT',
                     lower_discretization=1,
                     upper_discretization=224,
                     optimize_groups=False):
            n_obj = len(sensitivities) + 1 if optimize_groups else len(sensitivities)
            super().__init__(
                n_var=n_groups - 1,
                n_obj=n_obj,
                n_constr=0,
                xl=lower_discretization,
                xu=upper_discretization,
                type_var=np.int32
            )
            self.criteria = criteria
            self.sensitivities = sensitivities
            self.n_groups = n_groups -1
            self.optimize_groups = optimize_groups
            self.FITNESS_FUNCTIONS = [
                CosineSimilarityGPT(s)._get_fitness if criteria == "GPT" else CosineSimilarityXGPT(s)._get_fitness
                for s in sensitivities
            ]

            print(f'Optimizing for {n_obj} objectives in total:')
            sens_index = 0
            for s in sensitivities:

                print(f'Sensitivity {sens_index}: optimizing  isotope {s.zai} for observable {s.observable} in reactions:')
                print(f'{list(s.perts.keys())}')
                sens_index+=1
            if self.optimize_groups== True:
                print('Minimizing number of groups')

        def _evaluate(self, x, out, *args, **kwargs):
            x = x.astype(np.int32)
            fitness_values = np.zeros([x.shape[0], len(self.FITNESS_FUNCTIONS)])
            num_active_variables = np.zeros(x.shape[0])

            for i in range(x.shape[0]):
                unique_indices = np.unique(sorted(x[i]))
                fitness_values[i, :] = [func(unique_indices) for func in self.FITNESS_FUNCTIONS]
                num_active_variables[i] = len(unique_indices) / (self.n_groups)

            if self.optimize_groups:
                out["F"] = np.column_stack([fitness_values, num_active_variables])
            else:
                out["F"] = fitness_values

    def SetProblem(self, **kwargs):
        self.problem = self.SetProblemMOO(**kwargs)
        self.sensitivities = kwargs.get("sensitivities", [])
        self.optimize_groups = kwargs.get("optimize_groups", False)





    def evaluate_run(self):
        # Plot performance metrics
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 2, 1)
        plt.plot(self.metrics.generations, self.metrics.best_fitness, label='Best Fitness')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(self.metrics.generations, self.metrics.avg_fitness, label='Average Fitness', color='orange')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.plot(self.metrics.generations, self.metrics.diversity, label='Diversity', color='green')
        plt.xlabel('Generation')
        plt.ylabel('Diversity (Std Dev)')
        plt.legend()

        plt.subplot(2, 2, 4)
        plt.plot(self.metrics.generations, self.metrics.hypervolume, label='Hypervolume', color='purple')
        plt.xlabel('Generation')
        plt.ylabel('Hypervolume')
        plt.legend()
        plt.show()

    def run(self):
        if self.problem is None:
            raise ValueError("Problem not set. Use .SetProblem(...) first.")

        algorithm = NSGA2(
            pop_size=500,
            sampling=IntegerRandomSampling(),
            crossover=SBX(prob=0.8, eta=3.0, vtype=float, repair=RoundingRepair()),
            mutation=PM(prob=0.08, eta=3.0, vtype=float, repair=RoundingRepair()),
            eliminate_duplicates=True,
            n_offsprings=1000
        )

        self.result = minimize(
            self.problem,
            algorithm,
            ('n_gen', 10),
            seed=333,
            verbose=True,
            callback=self.metrics.record
        )
        self.evaluate_run()
        self.df_results = self.show_results()
        df_display = self.df_results.copy()
        df_display["Energy Grid"] = df_display["Energy Grid"].apply(
            lambda x: str(x)[:30] + "..." if len(str(x)) > 30 else str(x))
        print('Optimization Results:\n')
        print(df_display)

    def show_results(self):
        if not hasattr(self, "result") or self.result is None:
            raise ValueError("No result available. Run the optimization first with .run().")

        X = self.result.X
        F = self.result.F
        n_var = self.problem.n_var


        # Convert X to lists
        rows_as_lists = [sorted(row) for row in X.tolist()]
        df_results = pd.DataFrame({"Energy Grid": rows_as_lists})

        # Create fitness columns
        fitness_cols = [f"Fitness_{i + 1}" for i in range(F.shape[1])]
        df_F = pd.DataFrame(F, columns=fitness_cols)
        # If optimizing number of groups, extract last fitness, convert to N_Groups, and drop it
        if self.optimize_groups:
            # Use all but the last fitness column
            for col in fitness_cols[:-1]:
                df_results[col] = df_F[col]

            # Convert last fitness to N_Groups
            df_results["N_Groups"] = df_F[fitness_cols[-1]] * n_var
            df_results.sort_values(by="N_Groups", ascending=False, inplace=True)
            df_results.reset_index(drop=True, inplace=True)
        else:
            # Keep all fitness columns as-is
            for col in df_F.columns:
                df_results[col] = df_F[col]
        return df_results
    def save_results(self, filename = None):

        output_dir = "./result_FREDS"
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        default_prefix = self.problem.criteria
        default_filename = f"{default_prefix}_{self.problem.n_var + 1}G_results.csv"
        final_filename = filename if filename is not None else default_filename
        full_path = os.path.join(output_dir, final_filename)
        # Save results
        self.df_results.to_csv(full_path, index=False)
        print(f"Results saved to {full_path}")

    def plot_results(self, index='All'):
        """
        Plots results from self.df_result.

        If `index` is None, plots all rows.
        If `index` is an integer or list of integers, plots only those indices.
        """
        if index == 'All':
            indices = self.df_results.index
        elif isinstance(index, int):
            indices = [index]
        else:
            indices = index  # assume list of indices

        for idx in indices:
            sens_index = 0
            for s in self.problem.sensitivities:

                print(f'Plotting Energy grid {idx} for Sensitivity {sens_index}: optimizing  isotope {s.zai} for observable {s.observable} in reactions:')
                print(f'{list(s.perts.keys())}')

                row = self.df_results.loc[idx]
                res_grids = row["Energy Grid"]
                s.plot(res_grids)
                sens_index += 1

    def plot_pareto_front(self):
        """
        Plots Pareto front from self.df_result.

        - 2D scatter if exactly 2 fitness columns
        - Pairplot matrix if more than 2
        """

        obj_cols = [col for col in self.df_results.columns
                        if col.startswith("Fitness") or col == "N_Groups"]

        if len(obj_cols) == 0:
            print("No fitness columns found.")
            return

        df_fitness = self.df_results[obj_cols]

        if len(obj_cols) == 2:
            # 2D Scatter
            plt.figure(figsize=(6, 5))
            plt.scatter(df_fitness[obj_cols[0]], df_fitness[obj_cols[1]], c='blue', edgecolors='k')
            plt.xlabel(obj_cols[0])
            plt.ylabel(obj_cols[1])
            #plt.title("Pareto Front (2D)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            # Matrix plot
            sns.pairplot(df_fitness)
            #plt.suptitle("Pareto Front Matrix", y=1.02)
            plt.show()




















# Extracting the information on the sensitivity
obj0 = GPTSensitivity( filepath="GPT/BFS_61_0_core_sens0.m",
                                observable="keff",
                                zai=922380,
                                perts=["fission xs", "ela scatt xs", "capture xs"])
obj1 = GPTSensitivity( filepath="GPT/BFS_61_0_core_sens0.m",
                                observable="beff",
                                zai=942390,
                                perts=["fission xs", "capture xs"])







#freds = Freds

freds = Freds()
freds.SetProblem(
    n_groups=33,
    sensitivities=([obj0,obj1]),  # your sensitivity data
    criteria='GPT',
    optimize_groups=True
)
freds.run()
freds.save_results()
freds.plot_results(index = 'All')
freds.plot_pareto_front()
