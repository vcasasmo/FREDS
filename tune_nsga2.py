import optuna
import multiprocessing
import pandas as pd
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.repair.rounding import RoundingRepair
from FREDS import FREDS
from sensitivity import GPTSensitivity

# ======================
# Objective factory
# ======================
def make_objective(n_groups, seeds_to_test, sens_filepath, observable, zai, perts, notation_dict):
    def objective(trial):
        # Create sensitivity object
        objective_sens = GPTSensitivity(
            filepath=sens_filepath,
            observable=observable,
            zai=zai,
            perts=perts,
            notation_dict=notation_dict
        )

        # Sample hyperparameters
        pop_size = trial.suggest_int("pop_size", 100, 600)
        crossover_prob = trial.suggest_float("crossover_prob", 0.5, 1.0)
        crossover_eta = trial.suggest_float("crossover_eta", 1.0, 5.0)
        mutation_prob = trial.suggest_float("mutation_prob", 0.01, 0.2)
        mutation_eta = trial.suggest_float("mutation_eta", 1.0, 5.0)
        n_offsprings = trial.suggest_int("n_offsprings", 200, 1200)

        hypervolumes = []

        for seed in seeds_to_test:
            algorithm = NSGA2(
                pop_size=pop_size,
                sampling=IntegerRandomSampling(),
                crossover=SBX(prob=crossover_prob, eta=crossover_eta, vtype=float, repair=RoundingRepair()),
                mutation=PM(prob=mutation_prob, eta=mutation_eta, vtype=float, repair=RoundingRepair()),
                eliminate_duplicates=True,
                n_offsprings=n_offsprings
            )

            FREDS.SetProblem(
                n_groups=n_groups,
                sensitivities=[objective_sens],
                criteria='GPT',
                optimize_groups=True,
                algorithm=algorithm
            )

            hv = FREDS.run(ngen=500, seed=seed, auto_termination=True, verbose=False)
            hypervolumes.append(hv[-1])

        for i, seed in enumerate(seeds_to_test):
            trial.set_user_attr(f"hv_seed_{seed}", hypervolumes[i])

        avg_hv = sum(hypervolumes) / len(hypervolumes)
        print(f"[Groups={n_groups}] Trial {trial.number}: avg HV={avg_hv:.5f} over seeds {seeds_to_test} with params {trial.params}")
        trial.set_user_attr("n_groups", n_groups)
        return avg_hv

    return objective

# ======================
# Run study (global)
# ======================
def run_study(n_groups, seeds, n_trials_per_group, sens_filepath, observable, zai, perts, notation_dict):
    print(f"\n🔁 Starting study for n_groups = {n_groups}")
    study_name = f"freds_xgpt_ngroups_{n_groups}"
    study = optuna.create_study(
        study_name=study_name,
        direction="maximize",
        storage=f"sqlite:///{study_name}.db",
        load_if_exists=True
    )
    study.optimize(
        make_objective(n_groups, seeds, sens_filepath, observable, zai, perts, notation_dict),
        n_trials=n_trials_per_group
    )

    print(f"\n✅ Finished n_groups = {n_groups}")
    print("Best hyperparameters:", study.best_params)
    print("Best hypervolume:", study.best_value)

    df = study.trials_dataframe(attrs=("number", "value", "params"))
    df["n_groups"] = n_groups

    # Extract HV per seed
    hv_data = {f"hv_seed_{s}": [] for s in seeds}
    for trial in study.trials:
        for seed in seeds:
            hv_data[f"hv_seed_{seed}"].append(trial.user_attrs.get(f"hv_seed_{seed}", None))
    for key, values in hv_data.items():
        df[key] = values

    df.to_csv(f"optuna_trials_results_ngroups_{n_groups}.csv", index=False)
    print(f"📝 Results saved to optuna_trials_results_ngroups_{n_groups}.csv")

# ======================
# Global tuning function
# ======================
def tune_freds(
    n_groups_list,
    seeds,
    n_trials_per_group=10,
    sens_filepath=None,
    observable="keff",
    zai=922350,
    perts=None,
    notation_dict=None,
    n_processes=1
):
    if perts is None:
        perts = ["MT2", "MT18", "MT102"]
    if notation_dict is None:
        notation_dict = {
            "total xs": "MT1",
            "ela scatt xs": "MT2",
            "fission xs": "MT18",
            "capture xs": "MT102"
        }

    # Prepare tasks for multiprocessing
    tasks = [(n_groups, seeds, n_trials_per_group, sens_filepath, observable, zai, perts, notation_dict)
             for n_groups in n_groups_list]

    with multiprocessing.get_context("fork").Pool(processes=n_processes) as pool:
        pool.starmap(run_study, tasks)

# ======================
# Example usage
# ======================
if __name__ == "__main__":
    groups_to_test = [33, 40, 72]
    seeds = [1, 42, 123, 256]

    tune_freds(
        n_groups_list=groups_to_test, #pool of maximm number of groups to be tested
        seeds=seeds, #pool of seeds to be tested
        n_trials_per_group=2, #number of iterations per maximum number of group to be tested
        sens_filepath="GPT/godiva.i_sens0.m",
        observable="keff",
        zai=922350,
        perts=["MT2","MT18","MT102"],
        notation_dict={"total xs": "MT1","ela scatt xs":"MT2","fission xs":"MT18","capture xs":"MT102"},
        n_processes=2 #Cores available in your machine for the task
    )
