import numpy as np
#@Emilie, this is perhaps the most slaughtered part, I moved all the utils for simplicity inside the class. The idea is that now we can call different metrics and use different tools
# using the same format with data safety.
class FitnessFunctions:
    def __init__(self, gpt_vector, gpt_vector_per_unit_lethargy, xgpt_energy_grid, gpt_energy_grid,eigenbasis,perts):  #eigenbasis, perts
        self.gpt_vector = gpt_vector
        self.gpt_vector_lethargy_normalised = gpt_vector_per_unit_lethargy
        self.xgpt_energy_grid = xgpt_energy_grid
        self.gpt_energy_grid = gpt_energy_grid
        self.eigenbasis = None #  eigenbasis
        self.perts = None # perts

    def compare_vectors_gpt_xgpt(self, ga_grid):
        evaluated_xgpt = self._project_gpt_onto_eigenbasis(ga_grid)
        return 1 - self._cosine_similarity(evaluated_xgpt, self.gpt_vector)

    def compare_vectors_gpt(self, ga_grid):
        gpt_ga = self._down_binning(self.gpt_vector_lethargy_normalised, ga_grid, self.gpt_energy_grid)
        ga_energy_grid = self._energy_from_energy_grid(self.gpt_energy_grid, ga_grid)
        extended_gpt_ga = self._up_binning(self.gpt_energy_grid, ga_energy_grid, gpt_ga)

        evaluated_gpt = []
        fine_gpt = []
        for label, evaluated_values in extended_gpt_ga.items():
            fine_values = self.gpt_vector[label]
            fine_gpt.append(fine_values)
            evaluated_gpt.append(evaluated_values)

        return 1 - self._cosine_similarity(np.concatenate(fine_gpt), np.concatenate(evaluated_gpt))
    @staticmethod
    def _cosine_similarity( a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def _project_gpt_onto_eigenbasis(self, ga_grid):
        coarse_gpt = self._down_binning(self.gpt_vector, ga_grid, self.gpt_energy_grid)
        ga_energy_grid = self._energy_from_energy_grid(self.gpt_energy_grid, ga_grid)
        extended_gpt_ga = self._up_binning(self.xgpt_energy_grid, ga_energy_grid, coarse_gpt)
        return self._projection(extended_gpt_ga, self.eigenbasis)

    def _projection(self, dict_sensitivity, eigenbasis):
        projected_sensitivity = []
        for label, index in self.perts.items():
            if index == 0:
                continue
            _, label, _ = label.split("_")
            sensitivity = dict_sensitivity[label]
            projected_sensitivity.append(np.sum(np.array(sensitivity) * np.array(eigenbasis[index - 1])))
        return np.array(projected_sensitivity)

    def _down_binning(self, gpt_sensitivities, ga_grid, gpt_energy_grid):
        downbinned = {}
        for reaction, sensitivities in gpt_sensitivities.items():
            downbinned[reaction] = self._evaluate_on_ga(sensitivities, ga_grid, gpt_energy_grid)
        return downbinned

    def _evaluate_on_ga(self, gpt_sensitivity, ga_grid, gpt_energy_grid):
        sensitivities_evaluated = np.zeros((len(ga_grid) + 1,))
        j = 0
        energies = []

        for i in range(len(gpt_sensitivity)):
            cut = len(gpt_sensitivity) if j >= len(ga_grid) else ga_grid[j]
            prev_cut = 0 if j == 0 else ga_grid[j - 1]

            if prev_cut <= i < cut:
                sensitivities_evaluated[j] += gpt_sensitivity[i] * (gpt_energy_grid[i + 1] - gpt_energy_grid[i])
                energies.append(gpt_energy_grid[i + 1] - gpt_energy_grid[i])
            else:
                sensitivities_evaluated[j] /= np.sum(energies)
                j += 1
                energies = []
                cut = len(gpt_sensitivity) if j >= len(ga_grid) else ga_grid[j]
                prev_cut = 0 if j == 0 else ga_grid[j - 1]
                sensitivities_evaluated[j] += gpt_sensitivity[i] * (gpt_energy_grid[i + 1] - gpt_energy_grid[i])
                energies.append(gpt_energy_grid[i + 1] - gpt_energy_grid[i])

        sensitivities_evaluated[-1] /= np.sum(energies)
        return sensitivities_evaluated

    def _energy_from_energy_grid(self, energy_discretisation, ga_grid):
        coarse_energy = np.zeros((len(ga_grid) + 2))
        coarse_energy[0] = energy_discretisation[0]
        for i, cut in enumerate(ga_grid):
            coarse_energy[i + 1] = energy_discretisation[cut]
        coarse_energy[-1] = energy_discretisation[-1]
        return coarse_energy

    def _up_binning(self, fine_energy_grid, coarse_energy_grid, down_binned_vector):
        upbinned = {}
        for reaction, down_binned_sensitivity in down_binned_vector.items():
            upbinned[reaction] = self._extend(fine_energy_grid, coarse_energy_grid, down_binned_sensitivity)
        return upbinned

    def _extend(self, fine_energy_grid, coarse_energy_grid, down_binned_sensitivity):
        up_binned_vector = np.zeros((len(fine_energy_grid) - 1,))
        j = 1
        for i in range(1, len(fine_energy_grid)):
            prev_energy = coarse_energy_grid[j - 1]
            energy = coarse_energy_grid[j]
            if prev_energy <= fine_energy_grid[i] <= energy:
                up_binned_vector[i - 1] = down_binned_sensitivity[j - 1]
                if fine_energy_grid[i] == energy:
                    j += 1
        return up_binned_vector
