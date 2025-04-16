import serpentTools
from collections import OrderedDict
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

zai_to_nuclide = {
    922380 : "U",
    942390 : "Pu"
}

class Sensitivity:
    def __init__(self, filepath, zai, notation_dict, perts = list(), observable = "keff"):
        """
        """
        self.reader =  serpentTools.read(filepath)
        self.observable = observable
        self.notation_dict = notation_dict
        self.zai = zai
        self.zai_index = self.reader.zais[zai]
        self.ga_grid = None
        self.energy_grid = self.extract_energy_grid()
        self.nEnergyGroups = len(self.energy_grid) - 1
        self.perts = self.extract_perts(perts)
        self.reference_gpt_sensitivities = self.extract_sensitivity_coefficients()
        self.gpt_sensitivities = self.reference_gpt_sensitivities
    
    def extract_sensitivity_coefficients(self):
        gpt_vector = dict()

        for reaction, reaction_index in self.perts.items():
            sensitivities = self.reader.sensitivities[self.observable][0][self.zai_index][reaction_index]
            gpt_vector[reaction] = np.zeros((self.nEnergyGroups,))

            for index, item in enumerate(sensitivities):
                sensitivity, _ = item
                gpt_vector[reaction][index] = sensitivity

            gpt_vector[reaction] /= self.reader.lethargyWidths

        return gpt_vector
    
    def set_ga_grid(self, ga_grid):
        self.reset_sensitivities()
        self.ga_grid = ga_grid
    
    def reset_sensitivities(self):
        self.gpt_sensitivities = self.reference_gpt_sensitivities
    
    def extract_energy_grid(self):
        return self.reader.energies
    
    def extract_perts(self, perts):
        pert = [k for k, v in self.notation_dict.items() if v in perts]
        filtered_perts = OrderedDict((k, v)  for k, v in self.reader.perts.items() if k in pert) if perts != list() else self.reader.perts
        if len(filtered_perts)==0:
            raise ValueError("No perturbation match in the GPT file.\nThe problem might come form the notation dictionnaru")
        return filtered_perts
    
    def downbin(self):
        downbinned = {}
        for reaction, sensitivity in self.gpt_sensitivities.items():
            downbinned[reaction] = self.evaluate_on_ga(sensitivity)
        self.gpt_sensitivities = downbinned
        
    def get_ga_energy_grid(self):
        """
        """
        coarse_energy = np.zeros((len(self.ga_grid) + 2))
        coarse_energy[0] = self.energy_grid[0]
        i = 1
        for cut in self.ga_grid:
            coarse_energy[i] = self.energy_grid[cut]
            i += 1
        coarse_energy[-1] = self.energy_grid[-1]
        return coarse_energy
    
    def evaluate_on_ga(self, sensitivity):

        nSens = len(sensitivity)
        nGASens = len(self.ga_grid)

        sensitivities_evaluated = np.zeros((nGASens + 1,))

        # Defining the index for filling the coarse sensitivity vector
        j = 0

        energies = []

        # Iteration over each sensitivity coefficient
        for i in range(nSens):

            # Defining the current cut. 
            cut = nSens if j >= nGASens else self.ga_grid[j]
            prev_cut = 0 if j == 0 else self.ga_grid[j - 1]

            # If the fine sensitivity coefficient is inside the coarse group 
            # defined by [prev_cut, cut], use it to evaluate the coarse 
            # sensitivity coefficient on that group

            if i >= prev_cut and i < cut:

                # Downbinning involves performing a weighted average, the weights being the energy intervals
                sensitivities_evaluated[j] += sensitivity[i]*(self.energy_grid[i+1] - self.energy_grid[i])
                energies.append(self.energy_grid[i+1] - self.energy_grid[i])

            # If the fine sensitivity coefficient is not inside group [prev_cut, cut], 
            # update prev_cut and cut.
            else :
                sensitivities_evaluated[j] /= np.sum(energies) 
                j += 1
                energies = []
                cut = len(sensitivity) if j >= len(self.ga_grid) else self.ga_grid[j]
                prev_cut = 0 if j == 0 else self.ga_grid[j - 1]
                sensitivities_evaluated[j] += sensitivity[i]*(self.energy_grid[i+1]-self.energy_grid[i])

                energies.append(self.energy_grid[i+1] - self.energy_grid[i])

        sensitivities_evaluated[-1] /= np.sum(energies) 
        return sensitivities_evaluated


class GPTSensitivity(Sensitivity):

    def __init__(self, filepath, zai, notation_dict, observable="keff",  perts=list()):
        super().__init__(filepath, zai, notation_dict, perts, observable)

    def extend(self, sensitivity):
        nSens = len(self.energy_grid)
        up_binned_vector = np.zeros( (nSens - 1, ) )
        coarse_energy_grid = self.get_ga_energy_grid()
        j = 1

        for i in range(1, nSens):
            # Energy on the left side of the coarse group
            prev_energy = coarse_energy_grid[j - 1]
            # Energy on the right side of the coarse group
            energy = coarse_energy_grid[j]

            # If the fine sensitivity coefficients is inside the coarse group [prev_energy, energy],
            # copy the coarse sensitivity coefficient as the fine sensitivity coefficient value
            if self.energy_grid[i] >= prev_energy and self.energy_grid[i] <= energy:
                up_binned_vector[i - 1] = sensitivity[j - 1]

                # If the fine energy matches the right side 
                # of the coarse group, move on to the next group
                if self.energy_grid[i] == energy:
                    j += 1

        return up_binned_vector
    
    def upbin(self):
        upbinned = {}
        for reaction, sensitivity in self.gpt_sensitivities.items():
            upbinned[reaction] = self.extend(sensitivity)
        self.gpt_sensitivities = upbinned

    def get_evaluated_sensitivity(self):
        return self.gpt_sensitivities
    
    def get_reference_sensitivity(self):
        return self.reference_gpt_sensitivities
    
    def plot(self, grid):
        
        self.set_ga_grid(grid)

        nPerts = len(self.perts)
        fig, axs = plt.subplots(1, nPerts, figsize=(4*nPerts, 4), sharex=True, sharey="row")
        plt.xscale("log")

        for i, perturbation in enumerate(self.perts):
            ax = axs[i]
            reference_sensitivity = np.concatenate((np.zeros(1), self.get_reference_sensitivity()[perturbation]))
            ax.step(self.energy_grid, reference_sensitivity, linestyle="-", where="post", color="grey", alpha=0.3)

            self.downbin()
            self.upbin()
            evaluated_sensitivity = np.concatenate((np.zeros(1),self.get_evaluated_sensitivity()[perturbation]))

            # naming to fix !
            naming = f"G{zai_to_nuclide[self.zai]}-{len(self.ga_grid) + 1}"
            ax.step(self.energy_grid, evaluated_sensitivity, where="post", label=f"{naming} evaluated on {perturbation}", alpha=0.8)

       
            ax.set_ylabel("Sensitivity per unit lethargy", fontsize=7)

            ax.legend(fontsize=7)
            ax.set_xlim(1e-6)
            ax.set_xlabel("E (MeV)", fontsize=6)

        fig.add_subplot(111, frame_on=False)
        plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
        # plt.xlabel("E (MeV)", fontsize=7)
    
        fig.tight_layout()
        plt.show()
    

class XGPTSensitivity(Sensitivity):
 
    def __init__(self, filepath_xgpt, filepath_gpt , filepath_eigfct, zai, notation_dict,  perts = list(), observable="keff"):
        super().__init__(filepath_gpt, zai, notation_dict, perts, observable)
        self.filepath_eigfct = filepath_eigfct
        self.xgpt_reader = serpentTools.read(filepath_xgpt)
        self.fine_energy_grid = self.extract_fine_grid()
        self.xgpt_perts = self.extract_xgpt_perts(perts)
        self.reference_xgpt_sensitivities = self.extract_xgpt_sensitivity_coefficients()
        self.xgpt_sensitivities = self.reference_xgpt_sensitivities
        self.eigenbasis = self.extract_eigenbasis()
        self.invert_notation_dict = {v: k for k, v in self.notation_dict.items()}

    def extract_xgpt_perts(self, perts):
        filtered_perts = OrderedDict((k, v) for k, v in self.xgpt_reader.perts.items() 
                                     if any(p in k for p in perts)) if perts else self.xgpt_reader.perts
        return filtered_perts

    def extract_xgpt_sensitivity_coefficients(self):
        nPerts = len(self.xgpt_perts)
        xgpt_vector = np.zeros((nPerts,))
        sensitivities = self.xgpt_reader.energyIntegratedSens[self.observable][0][0]
        for index, item in enumerate(sensitivities):
            sensitivity, _ = item
            if index == 0:
                continue
            xgpt_vector[index - 1] = sensitivity
        return xgpt_vector
    
    def extract_fine_grid(self):
        for pert in self.perts:
            MT_notation = self.notation_dict[pert]
            eigfct_pattern = f"{self.filepath_eigfct}/{self.zai}_{MT_notation}_*.txt"
            eigfct_path = glob.glob(eigfct_pattern)
            if eigfct_path != []:
                break

        with open(eigfct_path[0], "r") as file:
            lines = file.readlines()
            nFineGroups, _ = lines[1].split(" \n")
            fine_energy_grid = np.zeros((int(nFineGroups)+1,))
            for i, line in enumerate(lines[2:]):
                sens_coeff, _ = line.split(" ")
                fine_energy_grid[i] = float(sens_coeff)

        fine_energy_grid[-1] = self.energy_grid[-1]
        return fine_energy_grid
    
    def extract_eigenbasis(self):
        """
        :param filepath: Computer address of the folder where the eigenfunctions are stored
        :param perts: an OrderedDict containing the order of the perturbations
        :return: A numpy matrix whose rows are filled with the eigenfunctions of the POD of 
            the covariance matrices
        """
        eigenbasis = np.zeros((len(self.xgpt_perts), len(self.fine_energy_grid)-1))
        for label, index in self.xgpt_perts.items():
            if index == 0:
                continue
            filename = os.path.join(self.filepath_eigfct, label+'.txt')
            with open(filename) as file:
                lines = file.readlines()
                for i, line in enumerate(lines[2:]):
                    _, basis_coeff = line.split(" ")
                    basis_coeff, _ = basis_coeff.split("\n")
                    eigenbasis[index - 1][i] = float(basis_coeff)
        return eigenbasis
    
    def upbin(self, plot = False):
        upbinned = {}
        for reaction, sensitivity in self.gpt_sensitivities.items():
            upbinned[reaction] = self.extend(sensitivity, plot)
        self.gpt_sensitivities = upbinned

    def extend(self, sensitivity, plot = False):
        if plot: 
            self.fine_energy_grid = self.energy_grid

        nSens = len(self.fine_energy_grid)
        up_binned_vector = np.zeros( (nSens - 1, ) )
        coarse_energy_grid = self.get_ga_energy_grid()
        j = 1

        for i in range(1, nSens):
            # Energy on the left side of the coarse group
            prev_energy = coarse_energy_grid[j - 1]
            # Energy on the right side of the coarse group
            energy = coarse_energy_grid[j]

            # If the fine sensitivity coefficients is inside the coarse group [prev_energy, energy],
            # copy the coarse sensitivity coefficient as the fine sensitivity coefficient value
            if self.fine_energy_grid[i] >= prev_energy and self.fine_energy_grid[i] <= energy:
                up_binned_vector[i - 1] = sensitivity[j - 1]

                # If the fine energy matches the right side 
                # of the coarse group, move on to the next group
                if self.fine_energy_grid[i] == energy:
                    j += 1

        return up_binned_vector
    
    def projection(self):
        projected_sensitivity = []
        # Projecting in the order defined by the perts dictionnary
        for label, index in self.xgpt_perts.items():
            if index == 0:
                continue
            _, label, _ = label.split("_")
            sensitivity = self.gpt_sensitivities[self.invert_notation_dict.get(label)]
            projected_sensitivity.append(np.sum(np.array(sensitivity)*np.array(self.eigenbasis[index-1])))
        
        self.xgpt_sensitivities = projected_sensitivity

    def get_evaluated_sensitivity(self):
        return self.xgpt_sensitivities
    
    def get_reference_sensitivity(self):
        return self.reference_xgpt_sensitivities
    
    def plot(self, grid):
        
        self.set_ga_grid(grid)

        nPerts = len(self.perts)
        fig, axs = plt.subplots(1, nPerts, figsize=(4*nPerts, 4), sharex=True, sharey="row")
        plt.xscale("log")

        for i, perturbation in enumerate(self.perts):
            ax = axs[i]
            reference_sensitivity = np.concatenate((np.zeros(1), self.reference_gpt_sensitivities[perturbation]))
            ax.step(self.energy_grid, reference_sensitivity, linestyle="-", where="post", color="grey", alpha=0.3)

            self.downbin()
            self.upbin(plot=True)
            evaluated_sensitivity = np.concatenate((np.zeros(1),self.gpt_sensitivities[perturbation]))

            # prefix = "G" if label == "GPT" else "X" if label == "XGPT" else "V"
            # nuclide = "Pu9" if ISOTOPE == "Pu239" else "U8"

            # naming to fix !
            naming = f"X{zai_to_nuclide[self.zai]}-{len(self.ga_grid) + 1}"
            ax.step(self.energy_grid, evaluated_sensitivity, where="post", label=f"{naming} evaluated on {perturbation}", alpha=0.8)

       
            ax.set_ylabel("Sensitivity per unit lethargy", fontsize=7)

            ax.legend(fontsize=7)
            ax.set_xlim(1e-6)
            ax.set_xlabel("E (MeV)", fontsize=6)

        fig.add_subplot(111, frame_on=False)
        plt.tick_params(labelcolor="none", top=False, bottom=False, left=False, right=False)
        # plt.xlabel("E (MeV)", fontsize=7)
    
        fig.tight_layout()
        plt.show()