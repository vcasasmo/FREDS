import matplotlib.pyplot as plt
from extract_input_data import ECCO33,gpt_energy_grid, xgpt_energy_grid, ISOTOPE, gpt_vector_lethargy_normalised, gpt_vector, extract_myrrha_sensitivities
from fitness_utils import down_binning, up_binning, energy_from_energy_grid, evaluate_on_ga, extend, project_gpt_onto_eigenbasis, projection, cosine_similarity
import numpy as np
import os
from extract_results import read_results

mt2_upper = 26 if ISOTOPE == "Pu239" else 10
mt18_upper = 55 if ISOTOPE == "Pu239" else 23
mt102_upper = 82 if ISOTOPE == "Pu239" else 41

def plot_vectors_xgpt(ga_grid):
    """
    :param ga_grid: A chromosome encoding the discretisation the
            XGPT-scored sensitivity vector is evaluated on
    Plot on a twin axis the fine and evaluated XGPT-scored sensitivity vectors 
    """
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_xlabel("k-th XGPT-scored sensitivity coefficient")

    ax1.set_ylabel('Serpent XGPT-scored coefficients', color="darkblue")
    ax1.step(np.arange(1, len(perts)), xgpt_vector, c="darkblue", where="post")
    plt.title(f"XGPT-scored sensitivity coefficients for {ISOTOPE} (MT= 2, 18, 102)")
    ax2 = ax1.twinx()

    gpt_ga = down_binning(gpt_vector, ga_grid, gpt_energy_grid)
    ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, ga_grid)
    extended_gpt_ga = up_binning(xgpt_energy_grid, ga_energy_grid, gpt_ga)

    projected_gpt = projection(extended_gpt_ga, eigenbasis)
    ax2.axvline(mt2_upper, ymin=-1.5, ymax=1, linestyle=":", color="red")
    ax2.axvline(mt18_upper, ymin=-1.5, ymax=1, linestyle=":", color="red")
    ax2.step(np.arange(1, len(perts)), projected_gpt, c="green", where="post")
    ax2.set_ylabel('Evaluated XGPT-scored coefficients (226G)', color="green")
    plt.show()

def energy_cut_from_energy_grid(gpt_energy_grid, energy_grid):
    """
    :param gpt_energy_grid: A fine energy grid (energies in MeV)
    :param energy_grid: An energy grid whose energies are expressed in MeV and 
    for which we wish to define a chromosomal representation
    :return: The chromosomal encoding of an energy grid expressed in MeV. 
    """
    return [np.abs(gpt_energy_grid - energy).argmin() for energy in energy_grid][1:-1]

def plot_cosine_contribution_xgpt(ga_grid, display =True):
    """
    :param ga_grid: A chromosome encoding the discretisation the
            XGPT-scored sensitivity vector is evaluated on
    :param display: A boolean. Determines whether or not the figure is displayed
    :return: A numpy array containing the contribution (%) of each sensitivity
        coefficient to the total cosine similarity
    Plot the contribution of each evaluated XGPT-scored sensitivity
    vector to the total cosine similarity with the fine XGPT-scored
    sensitivity vector
    """

    # 1. Evaluating the contributions of each coefficient
    evaluated_xgpt = project_gpt_onto_eigenbasis(ga_grid)
    contribution = np.zeros(len(evaluated_xgpt))
    norm_fine = np.linalg.norm(xgpt_vector)
    norm_eval = np.linalg.norm(evaluated_xgpt)
    for i in range(len(evaluated_xgpt)):
        contribution[i] = evaluated_xgpt[i] * xgpt_vector[i] / (norm_eval * norm_fine)

    # Normalising by the total cosine similarity and multiplying by 100 
    contribution /= cosine_similarity(evaluated_xgpt, xgpt_vector) / 100

    # Plotting the results
    if display:
        plt.step(np.arange(1, len(perts)), contribution)
        plt.axvline(mt2_upper, linestyle=":", color="red")
        plt.axvline(mt18_upper, linestyle=":", color="red")
        naming = f"X-Pu9 {len(ga_grid)+1}" if ISOTOPE == "Pu239" else f"X-U8 {len(ga_grid)+1}"
        plt.title(f"({naming}) Contribution to each XGPT-scored coefficient to the total cosine similarity")
        plt.xlabel("k-th XGPT-scored sensitivity coefficient")
        plt.ylabel("Contribution to the total cosine similarity (%)")
        plt.show()

    return contribution

def plot_eb_sens_xgpt(label, tol_contribution):
    """
    :param label: A string defining the reaction for which 
        the eigenbasis x sensitivity vector must be plotted. 
        label must be part of the list : ["MT2", "MT18", "MT102"]
    :param tol_contribution: A number defining the minimal percentage
        of contribution to the total cosine similarity must a sensitivity
        coefficient have to have its information plotted
    
    """
    contribution = plot_cosine_contribution_xgpt(np.arange(1, 226), display = False)

    sorted_indices = np.argsort(contribution)[::-1]
    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax1.set_xscale("log")
    ax2 = ax1.twinx()
    plotted = False
    for i, index in enumerate(sorted_indices):
        if contribution[index] > tol_contribution:
            eigen_label = "MT2" if index < mt2_upper else "MT18" if index < mt18_upper else "MT102"
            if eigen_label != label:
                continue
            color_index = 0 if eigen_label == "MT2" else mt2_upper if eigen_label == "MT18" else mt18_upper
            n = "Pu" if ISOTOPE == "Pu239" else "U"

            # Each eigenfunction has its own pre-defined color attributed
            with open(os.path.join(os.getcwd(), "ColorPalette", f"color{eigen_label}{n}.txt"), "r") as file:
                colors = file.readlines()

            sens = np.concatenate(([0], eigenbasis[index]))
            if not plotted:
                plotted = True
                ax2.step(gpt_energy_grid, np.concatenate(([0], gpt_vector[eigen_label])), c="grey", alpha=0.3, label=f"{eigen_label} GPT-scored sensitivity profile on 226G")
            contrib = contribution[index] / 100
            ax1.step(xgpt_energy_grid, sens * contrib, c=eval(colors[index - color_index]), where="post", label=f"{index}th eigenfunction ({round(contribution[index], 2)} %)")

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    handles = handles1 + handles2
    labels = labels1 + labels2
    ax1.legend(handles, labels, loc='upper left', fontsize=9)

    ax1.set_xlabel("E (MeV)")
    ax1.set_ylabel("Eigenfunctions")
    ax2.set_ylabel("Sensitivity")
    plt.title("Most contributing eigenfunctions and sensitivity profile to the cosine similarity (X-{})".format(n + str(ISOTOPE[-1])))
    plt.xlim(1e-7)
    plt.show()


def plot_variance_graphs(discretizations):
    """
    :param discretisations: A dictionnary with 4 entries.
                Each key defines a number of groups and its associated value
                is the associated discretisation found with the variance 
                comparison fitness function
    """
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 6))
    subplot_indices = list(discretizations.keys())

    for ax, n_group in zip(axes.flatten(), subplot_indices):
        ga_grid = discretizations[n_group]
        index = 0

        for i in range(len(eigenbasis)):
            eigen_function = eigenbasis[i]
            if index == 0 or index == mt2_upper or index == mt18_upper:
                label = "MT2" if index == 0 else "MT18" if index == mt2_upper else "MT102"
                color_index = 0 if label == "MT2" else mt2_upper if label == "MT18" else mt18_upper
                with open(os.path.join(os.getcwd(), "ColorPalette", f"color{label}Pu.txt"), "r") as file:
                    colors = file.readlines()

            gpt_ga = down_binning(gpt_vector, ga_grid, gpt_energy_grid)
            ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, ga_grid)
            sens = up_binning(xgpt_energy_grid, ga_energy_grid, gpt_ga)

            color = eval(colors[index - color_index])
            ax.step(xgpt_energy_grid[:-1], singular_matrix[index][index] * (eigen_function * sens[label])**2, c=color)

            index += 1

        ax.scatter(energy_from_energy_grid(gpt_energy_grid, ga_grid), np.zeros(len(ga_grid) + 2), c="r", zorder=30, s=5, label=f"V-Pu9 {n_group}")
        ax.set_xscale("log")
        ax.set_xlabel("E (MeV)")
        ax.legend()

    plt.tight_layout()
    plt.suptitle("(Eigenfunctions x Sensitivity Profiles)² x Singular Value", y=1.05)
    plt.xlim(left=1e-7)
    plt.show()


def compute_individual_cosine_similarity(label, vector1, vector2, ga_grid,
                                          energies, concat_values,
                                            eval_concat_values):
    """
    Compute the contribution to the total cosine similarity 
    of each GPT-scored sensitivity coefficient
    """
    norm_vector1 = np.linalg.norm(eval_concat_values)
    norm_vector2 = np.linalg.norm(concat_values)
    cos_vector = []
    energy_vector = []
    prev_cut = 0

    for cut in ga_grid:
        dot_product = np.dot(vector1[prev_cut:cut], vector2[prev_cut:cut])
        cos = dot_product / (norm_vector2 * norm_vector1)
        energy_vector += list(energies[prev_cut:cut])
        cos_vector += [cos] * len(energies[prev_cut:cut])
        prev_cut = cut

    dot_product = np.dot(vector1[prev_cut:], vector2[prev_cut:])
    cos = dot_product / (norm_vector2 * norm_vector1)
    energy_vector += list(energies[prev_cut:])
    cos_vector += [cos] * len(energies[prev_cut:])

    total_cosine_similarity = cosine_similarity(eval_concat_values, concat_values)
    color = "navy" if label == "MT18" else "darkolivegreen" if label == "MT102" else "chocolate"
    plt.step(energy_vector, cos_vector / total_cosine_similarity, label=label, c=color, alpha=0.7)

def plot_cosine_contribution_gpt(ga_grid):
    gpt_ga = down_binning(gpt_vector_lethargy_normalised, np.arange(1, 226), gpt_energy_grid)
    ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, np.arange(1, 226))
    extended_gpt_ga = up_binning(gpt_energy_grid, ga_energy_grid, gpt_ga)

    values_to_concatenate = []
    for label, values in gpt_vector_lethargy_normalised.items():
        values_to_concatenate.append(values)
    concatenated_sensitivity = np.concatenate(values_to_concatenate)

    values_to_concatenate = []
    for label, values in extended_gpt_ga.items():
        values_to_concatenate.append(values)
    eval_concatenated_sensitivity = np.concatenate(values_to_concatenate)

    plt.title(f"({ISOTOPE}) Contribution of each sensitivity coefficient to the total cosine similarity ({len(ga_grid) + 1}G)")
    plt.xscale("log")
    plt.xlabel("E (MeV)")
    plt.ylabel("Absolute contribution to the total cosine similarity (%)")

    for label, eval_values in extended_gpt_ga.items():
        compute_individual_cosine_similarity(label, gpt_vector_lethargy_normalised[label], eval_values, np.arange(1, 226), gpt_energy_grid, concatenated_sensitivity, eval_concatenated_sensitivity)

    energy = energy_from_energy_grid(gpt_energy_grid, ga_grid)
    naming = "Pu9" if ISOTOPE == "Pu239" else "U8"
    plt.scatter(energy, np.zeros(len(energy)), zorder=30, s=10, c="r", label=f"G-{naming} {len(ga_grid) + 1}")
    plt.legend(fontsize = 7)
    plt.xlim(left=1e-7)
    plt.show()


def plot_grids(grids):
    """
    :param n_groups: A list of integers, for which we aim
    to plot the discretisations
    Plot the sensitivity profile evaluated on the energy
    grids of the three different fitness functions
    """
    for n_group, grid in grids.items():
        fig, axs = plt.subplots(3, 3, figsize=(12, 12), sharex=True, sharey="row")
        plt.xscale("log")
        reactions = ["MT2", "MT18", "MT102"]

        for i, reaction in enumerate(reactions):
            for j, (label, (color, energy_grid)) in enumerate(grid.items()):
                ax = axs[i, j]
                s_gpt = np.concatenate((np.zeros(1), gpt_vector_lethargy_normalised[reaction]))
                ax.step(gpt_energy_grid, s_gpt, linestyle="-", where="post", color="grey", alpha=0.3)

                gpt_ga = down_binning(gpt_vector_lethargy_normalised, energy_grid, gpt_energy_grid)
                ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, energy_grid)
                evaluated_values = np.concatenate((np.zeros(1), extend(gpt_energy_grid, ga_energy_grid, gpt_ga[reaction])))

                prefix = "G" if label == "GPT" else "X" if label == "XGPT" else "V"
                nuclide = "Pu9" if ISOTOPE == "Pu239" else "U8"
                naming = f"{prefix}-{nuclide} {n_group}"
                ax.step(gpt_energy_grid, evaluated_values, where="post", c=color, label=f"{reaction} evaluated on {naming}", alpha=0.8)

                if j == 0:
                    ax.set_ylabel("Sensitivity per unit lethargy", fontsize=7)

                ax.legend(fontsize=7)
                ax.set_xlim(1e-6)
                ax.set_xlabel("E (MeV)", fontsize=6)

        fig.add_subplot(111, frame_on=False)
        plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
        # plt.xlabel("E (MeV)", fontsize=7)
       
        fig.tight_layout()
        plt.show()


def plot_grids_on_other_nuclide(n_groups):
    """
    :param n_groups: A list of integers, for which we aim 
    to plot the discretisations
    Plot the sensitivity profile evaluated on the energy grids
    optimised for the other nuclide, found with the three 
    different fitness functions
    """
    grids = read_results(n_groups, switch=True)
    for n_group, grid in grids.items():
        fig, axs = plt.subplots(3, 2, figsize=(12, 8), sharex=True, sharey="row")
        plt.xscale("log")
        reactions = ["MT2", "MT18", "MT102"]

        for i, reaction in enumerate(reactions):
            for j, (label, (color, energy_grid)) in enumerate(grid.items()):
                if label == "uncertainty":
                    continue
                ax = axs[i, j]
                s_gpt = np.concatenate((np.zeros(1), gpt_vector_lethargy_normalised[reaction]))
                ax.step(gpt_energy_grid, s_gpt, linestyle="-", where="post", color="grey", alpha=0.3)

                gpt_ga = down_binning(gpt_vector_lethargy_normalised, energy_grid, gpt_energy_grid)
                ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, energy_grid)
                evaluated_values = np.concatenate((np.zeros(1), extend(gpt_energy_grid, ga_energy_grid, gpt_ga[reaction])))

                prefix = "G" if label == "GPT" else "X" if label == "XGPT" else "V"
                nuclide = "U8" if ISOTOPE == "Pu239" else "Pu9"
                naming = f"{prefix}-{nuclide} {n_group}"
                ax.step(gpt_energy_grid, evaluated_values, where="post", c=color, label=f"{reaction} profile of {ISOTOPE} evaluated on {naming}", alpha=0.8)

                if j == 0:
                    ax.set_ylabel("Sensitivity per unit lethargy", fontsize=7)

                ax.legend(fontsize=6)
                                # ax.legend(fontsize=7)
                ax.set_xlim(1e-6)
                ax.set_xlabel("E (MeV)", fontsize=6)

        fig.add_subplot(111, frame_on=False)
        nuclide = "$Pu^{239}$" if ISOTOPE=="Pu239" else "$U^{238}$"
        other = "$Pu^{239}$" if ISOTOPE=="U238" else "$U^{238}$"
        plt.suptitle("Grids optimised on {} applied to {} sensitivity profiles".format(other,nuclide))
        plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
        plt.xlabel("E (MeV)", fontsize=7)
        plt.xlim(1e-5)
        fig.tight_layout()
        plt.show()



def plot_variability_of_cuts(nGroups):
    """
    :param nGroups: the number of groups in the energy 
    discretisation you wish to visualise the variability
    of the cuts

    Plot the variability of the cuts for energy grids 
    containing nGroups groups
    """
    for ff in ["GPT", "XGPT", "uncertainty"]:
        disc = dict((cut,0) for cut in range(1, 226))
        fig, ax1 = plt.subplots(figsize=(8, 6))
        i = 0
        with open(os.path.join(os.getcwd(), "Results",ISOTOPE,
                                    "{}_{}G.txt".format(ff, nGroups)), "r") as file:
            for discretisation in file.readlines():
                i += 1
                cuts = eval(discretisation.strip())
                for cut in cuts:
                    disc[cut] +=1

        histograms = np.array([100*key/i for key in disc.values()])
        # plt.xscale("log")
        print(i)
        ax1.step(gpt_energy_grid[1:-1], histograms, c="red",alpha = 0.6)
        ax1.set_ylim(ymin = 0, ymax = 600)
        ax1.set_xscale("log")
        ax1.set_ylabel("Rate of apparition of the cut (%)")
        # plt.title(ff)
        ax2 = ax1.twinx()
        ax1.set_xlabel("E (MeV)")
        ax2.set_xscale("log")
        plt.xlabel("E (MeV)")
        ax2.set_ylabel("Sensitivity per Unit Lethargy")
        ax2.step(gpt_energy_grid[:-1], gpt_vector_lethargy_normalised["MT18"], c="royalblue", label="MT18 sensitivity profile", alpha = 0.4)
        ax2.step(gpt_energy_grid[:-1], gpt_vector_lethargy_normalised["MT102"], c="darkgreen", linestyle = "-",label="MT102 sensitivity profile", alpha = 0.4)
        n = "U8" if ISOTOPE == "U238" else "Pu9"
        plt.title("Variability of the cuts for {}-{} {} (50 runs)".format("X" if ff=="XGPT" else "G" if ff== "GPT" else "V",n, nGroups, i))
        plt.legend()
        plt.xlim(1e-6)
        plt.show()

def plot_ecco33():
    """
    Plot the sensitivity profiles evaluated on the ECCO 33
    """

    fig, axs = plt.subplots(3, 1, figsize=(4, 6))  # 3 lignes, 1 colonne
    ecco33 = energy_cut_from_energy_grid(gpt_energy_grid, ECCO33)
    down_binned = down_binning(gpt_vector_lethargy_normalised, ecco33, gpt_energy_grid)
    ga_grid = energy_from_energy_grid(gpt_energy_grid, ecco33)
 
    axs[0].step(gpt_energy_grid[:-1], gpt_vector_lethargy_normalised["MT2"], c="grey", alpha=0.5)
    axs[0].set_xscale("log")
    axs[0].step(gpt_energy_grid[:-1], extend(gpt_energy_grid, ga_grid, down_binned["MT2"]), 'b-', label = "ECCO 33")
    axs[0].set_title('($Pu^{239}$) Sensitivity profile of $k_{eff}$, under MT2 cross-section perturbation', fontsize=9)
    axs[0].set_xlabel('E (MeV)', fontsize=7)
    axs[0].set_xlim(1e-5)
    axs[0].set_ylabel('Sensitivity per unit lethargy', fontsize=8)
    axs[0].legend()
    
    axs[1].set_xscale("log")
    axs[1].step(gpt_energy_grid[:-1], gpt_vector_lethargy_normalised["MT18"], c="grey", alpha=0.5)
    axs[1].set_xlim(1e-5)
    axs[1].step(gpt_energy_grid[:-1], extend(gpt_energy_grid, ga_grid, down_binned["MT18"]), 'b-',  label = "ECCO 33")
    axs[1].set_title('($Pu^{239}$) Sensitivity profile of $k_{eff}$, under MT18 cross-section perturbation', fontsize=9)
    axs[1].set_xlabel('E (MeV)', fontsize=7)
    axs[1].set_ylabel('Sensitivity per unit lethargy', fontsize=8)
    axs[1].legend()
   
    axs[2].set_xscale("log")
    axs[2].step(gpt_energy_grid[:-1], gpt_vector_lethargy_normalised["MT102"], c="grey", alpha=0.5)
    axs[2].step(gpt_energy_grid[:-1], extend(gpt_energy_grid, ga_grid, down_binned["MT102"]), 'b-',  label = "ECCO 33")
    axs[2].set_title('($Pu^{239}$) Sensitivity profile of $k_{eff}$, under MT102 cross-section perturbation', fontsize=9)
    axs[2].set_xlabel('E (MeV)', fontsize=7)
    axs[2].set_ylabel('Sensitivity per unit lethargy', fontsize=8)
    axs[2].set_xlim(1e-5)
    axs[2].legend()

    plt.tight_layout()
    
    plt.show()

def compute_representativity(list_grids):
    """
    :param list_grids: a list of the names of energy grids
    we aim at comparing the representativity of ALFRED core
    to MYRRHA core. This list should 
    be filled with strings of the following format :
            - The first letter is V, X, or G
            - U if the grid is optimised on Uranium 238 and
              Pu if the grid is optimised on Plutonium 239
            - The number of groups in the energy discretisation
        As an example, if you want to compute the representativity
        for sensitivities scored on an energy grid optimised with
        the XGPT cosine similarity comparison of the sensitivity
        profiles of Pu239 and containing 33 groups, add "XPu33"
        in the list.

    Print the results of the evaluated representativity and
    their discrepancy with the target repreresentativity (226G)
    """
        
    dict_repres = {}
    myrrha_sens, myrrha_per_unit_leth= extract_myrrha_sensitivities()
    r = compute_representativity(myrrha_sens, gpt_vector, "{}_xs_reduced.csv".format(ISOTOPE))
   
    ecco33 = energy_cut_from_energy_grid(gpt_energy_grid, ECCO33)

    myrrha_rebinned = down_binning(myrrha_sens,ecco33, gpt_energy_grid)
    alfred_rebinned = down_binning(gpt_vector, ecco33, gpt_energy_grid)
    r_eval = compute_representativity(myrrha_rebinned, alfred_rebinned, "ECCO33_{}_xs_reduced.csv".format(ISOTOPE))

    dict_repres["ECCO33"]= (r_eval, abs(r-r_eval)/r)

    dis = read_results([ 33])
   
    for energy_grid_name in list_grids:
    
        method = "uncertainty" if energy_grid_name[0]=="V" else "GPT" if energy_grid_name[0]=="G" else "XGPT"

        alfred_rebinned = down_binning(gpt_vector, dis[int(energy_grid_name[-2:])][method][1], gpt_energy_grid)
        myrrha_rebinned = down_binning(myrrha_sens, dis[int(energy_grid_name[-2:])][method][1], gpt_energy_grid)
        r_eval = compute_representativity(myrrha_rebinned, alfred_rebinned, "{}_{}_xs_reduced.csv".format(energy_grid_name, ISOTOPE))

        dict_repres[energy_grid_name]=(r_eval,abs(r-r_eval)/r)

    sorted_dictionnary = dict(sorted(dict_repres.items(), key=lambda item: item[1][0]))

    print(sorted_dictionnary)
