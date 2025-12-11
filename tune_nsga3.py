import optuna
import multiprocessing
import pandas as pd
import numpy as np
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair

from FREDS import FREDS
from sensitivity import GPTSensitivity

# ======================
# Objective factory
# ======================
def make_objective(pair_name, sensitivities, n_groups, seeds_to_test, criteria):
    """
    Creates an Optuna objective function for NSGA-III tuning.
    """
    def objective(trial):
        # Hyperparameters NSGA-III
        pop_size = trial.suggest_int("pop_size", 90, 300, step=10)
        n_offsprings = trial.suggest_int("n_offsprings", pop_size, 2*pop_size, step=10)
        crossover_prob = trial.suggest_float("crossover_prob", 0.8, 1.0)
        crossover_eta = trial.suggest_int("crossover_eta", 10, 30)
        mutation_prob = trial.suggest_float("mutation_prob", 0.01, 0.2)
        mutation_eta = trial.suggest_int("mutation_eta", 20, 50)

        hypervolumes = []

        for seed in seeds_to_test:
            algorithm = NSGA3(
                ref_dirs=get_reference_directions("energy", n_dim=len(sensitivities)+1, n_points=pop_size, seed=1),
                pop_size=pop_size,
                sampling=IntegerRandomSampling(),
                crossover=SBX(prob=crossover_prob, eta=crossover_eta, vtype=float, repair=RoundingRepair()),
                mutation=PM(prob=mutation_prob, eta=mutation_eta, vtype=float, repair=RoundingRepair()),
                eliminate_duplicates=True,
                n_offsprings=n_offsprings
            )

            FREDS.SetProblem(
                n_groups=n_groups,
                sensitivities=sensitivities,
                criteria=criteria,
                optimize_groups=True,
                algorithm=algorithm
            )

            hv = FREDS.run(ngen=500, seed=seed, auto_termination=True, verbose=False)
            hypervolumes.append(hv[-1])

        # Save HVs per seed
        for i, seed in enumerate(seeds_to_test):
            trial.set_user_attr(f"hv_seed_{seed}", hypervolumes[i])

        avg_hv = np.mean(hypervolumes)
        print(f"[{pair_name}] Groups={n_groups}, Trial {trial.number}: avg HV={avg_hv:.5f}, params={trial.params}")
        trial.set_user_attr("pair", pair_name)
        trial.set_user_attr("n_groups", n_groups)
        return avg_hv

    return objective

# ======================
# Run study (global)
# ======================
def run_study(pair_name, sensitivities, n_groups, seeds, n_trials, criteria):
    study_name = f"freds_nsga3_generic_{pair_name}_ngroups{n_groups}"
    print(f"\n🔁 Starting study {study_name}")
    study = optuna.create_study(
        study_name=study_name,
        direction="maximize",
        storage=f"sqlite:///{study_name}.db",
        load_if_exists=True
    )
    study.optimize(make_objective(pair_name, sensitivities, n_groups, seeds, criteria), n_trials=n_trials)

    df = study.trials_dataframe(attrs=("number", "value", "params"))
    df["pair"] = pair_name
    df["n_groups"] = n_groups
    df["criteria"] = criteria

    # Extract HVs per seed
    hv_data = {f"hv_seed_{s}": [] for s in seeds}
    for trial in study.trials:
        for seed in seeds:
            hv_data[f"hv_seed_{seed}"].append(trial.user_attrs.get(f"hv_seed_{seed}", None))
    for key, values in hv_data.items():
        df[key] = values

    out_csv = f"optuna_results_nsga3_{pair_name}_ngroups{n_groups}.csv"
    df.to_csv(out_csv, index=False)
    print(f"📝 Results saved to {out_csv}")
    print(f"✅ Finished study {study_name}")

# ======================
# Global tuning function
# ======================
def tune_freds_generic(
    sensitivity_pairs,
    n_groups_list,
    seeds,
    n_trials_per_group=250,
    criteria='GPT',
    n_processes=1
):
    """
    Runs FREDS NSGA-III tuning for a generic scenario with user-provided sensitivities.

    Parameters
    ----------
    sensitivity_pairs : dict
        Dictionary of {pair_name: list_of_GPTSensitivity}.
    n_groups_list : list of int
        List of number of energy groups to optimize.
    seeds : list of int
        Random seeds to use.
    n_trials_per_group : int
        Number of Optuna trials per pair/group.
    criteria : str
        Criteria for FREDS ('GPT' or 'XGPT').
    n_processes : int
        Number of parallel processes.
    """
    tasks = []
    for pair_name, sensitivities in sensitivity_pairs.items():
        for n_groups in n_groups_list:
            tasks.append((pair_name, sensitivities, n_groups, seeds, n_trials_per_group, criteria))

    with multiprocessing.get_context("fork").Pool(processes=n_processes) as pool:
        pool.starmap(run_study, tasks)

# ======================
# Example usage
# ======================
if __name__ == "__main__":
    from sensitivity import GPTSensitivity

    # Example sensitivities
    filepath = "GPT/uam.i_sens0.m"
    notation_dict = {
        "total xs": "MT1",
        "ela scatt xs": "MT2",
        "fission xs": "MT18",
        "capture xs": "MT102"
    }

    sens_H1 = GPTSensitivity(filepath=filepath, observable="keff", zai=10010, perts=["MT2"], notation_dict=notation_dict)
    sens_U5 = GPTSensitivity(filepath=filepath, observable="keff", zai=922350, perts=["MT18"], notation_dict=notation_dict)
    sens_U8 = GPTSensitivity(filepath=filepath, observable="keff", zai=922380, perts=["MT102"], notation_dict=notation_dict)

    sensitivity_pairs = {"H1_U5": [sens_H1, sens_U5], "H1_U8": [sens_H1, sens_U8]}

    # Configuración de optimización
    groups_to_test = [33, 40, 72]
    seeds = [1, 42, 123]

    tune_freds_generic(
        sensitivity_pairs=sensitivity_pairs,
        n_groups_list=groups_to_test, #pool of maximm number of groups to be tested
        seeds=seeds, #pool of seed to test
        n_trials_per_group=5, #number of iterations per maximum number of group to be tested
        criteria='GPT',
        n_processes=2 #Cores available in your machine for the task
    )
