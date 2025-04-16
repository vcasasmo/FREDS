import serpentTools
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt

class Sensitivity:
    def __init__(self, filepath, zai, perts = list(), observable = "keff"):
        """
        """
        self.reader =  serpentTools.read(filepath)
        self.observable = observable
        self.energy_grid = self.extract_energy_grid()
        self.nEnergyGroups = len(self.energy_grid) - 1
        self.perts = self.extract_perts(perts)
        self.zai_index = self.reader.zais[zai]
        self.zai = zai
        self.reference_sensitivities = self.extract_sensitivity_coefficients()
        self.sensitivities = self.reference_sensitivities
        self.ga_grid = None

    def get_evaluated_sensitivity(self):
        return self.sensitivities
    
    def get_reference_sensitivity(self):
        return self.reference_sensitivities
    
    def extract_sensitivity_coefficients(self):
        raise NotImplementedError
    
    def set_ga_grid(self, ga_grid):
        self.reset_sensitivities()
        self.ga_grid = ga_grid
    
    def reset_sensitivities(self):
        self.sensitivities = self.reference_sensitivities
    
    def extract_energy_grid(self):
        return self.reader.energies
    
    def extract_perts(self, perts):
        filtered_perts = OrderedDict((k, v)  for k, v in self.reader.perts.items() if k in perts) if perts != list() else self.reader.perts
        return filtered_perts
    
    def downbin(self):
        downbinned = {}
        for reaction, sensitivity in self.sensitivities.items():
            downbinned[reaction] = self.evaluate_on_ga(sensitivity)
        self.sensitivities = downbinned

    def upbin(self):
        upbinned = {}
        for reaction, sensitivity in self.sensitivities.items():
            upbinned[reaction] = self.extend(sensitivity)
        self.sensitivities = upbinned
    
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

            # prefix = "G" if label == "GPT" else "X" if label == "XGPT" else "V"
            # nuclide = "Pu9" if ISOTOPE == "Pu239" else "U8"
            naming = f"GU-33"
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


class GPTSensitivity(Sensitivity):

    def __init__(self, filepath, zai, observable="keff",  perts=list()):
        super().__init__(filepath, zai, perts, observable)

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
    


class XGPTSensitivity(Sensitivity):
 
    def __init__(self, filepath, zai, perts = list(), observable="keff"):
        super().__init__(filepath, zai, perts, observable)

    def extract_sensitivity_coefficients(self):
        nPerts = len(self.perts)
        xgpt_vector = np.zeros((nPerts-1,))
        sensitivities = self.reader.energyIntegratedSens[self.observable][0][0]
        for index, item in enumerate(sensitivities):
            sensitivity, _ = item
            if index == 0:
                continue
            xgpt_vector[index] = sensitivity
        return xgpt_vector
    
    def projection(self):
        pass