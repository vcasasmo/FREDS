import matplotlib.pyplot as plt
import numpy as np

def plot_grids(grids,reactions):
    """
    :param n_groups: A list of integers, for which we aim
    to plot the discretisations
    Plot the sensitivity profile evaluated on the energy
    grids of the three different fitness functions
    """
    for n_group, grid in grids.items():
        fig, axs = plt.subplots(1, reactions, figsize=(6, 12), sharex=True, sharey="row")
        plt.xscale("log")

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


