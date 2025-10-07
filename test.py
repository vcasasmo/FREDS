import numpy as np


def evaluate_on_ga(sensitivity, ga_grid):
        
        nSens = len(sensitivity)
        nGASens = len(ga_grid)

        sensitivities_evaluated = np.zeros((nGASens + 1,))

        # Defining the index for filling the coarse sensitivity vector
        j = 0

        # Iteration over each sensitivity coefficient
        for i in range(nSens):

            # Defining the current cut. 
            cut = nSens if j >= nGASens else ga_grid[j]
            prev_cut = 0 if j == 0 else ga_grid[j - 1]

            # If the fine sensitivity coefficient is inside the coarse group 
            # defined by [prev_cut, cut], use it to evaluate the coarse 
            # sensitivity coefficient on that group

            if i >= prev_cut and i < cut:
                sensitivities_evaluated[j] += sensitivity[i]
                
            # If the fine sensitivity coefficient is not inside group [prev_cut, cut], 
            # update prev_cut and cut.
            else :
                j += 1
                cut = len(sensitivity) if j >= len(ga_grid) else ga_grid[j]
                prev_cut = 0 if j == 0 else ga_grid[j - 1]
                sensitivities_evaluated[j] += sensitivity[i]
        return sensitivities_evaluated

a_energies = [0, 0.1, 1, 10, 20]
b_energies = [0, 0.1, 10, 20]





from fitness_functions import CosineSimilarityGPT
from sensitivity import GPTSensitivity

notation_dict = {"total xs":"MT1", "ela scatt xs":"MT2",
                 "fission xs": "MT18",  "capture xs":"MT102"}

sens = GPTSensitivity("GPT/main_sens0.m", 942390, notation_dict,  perts = ["MT2", "MT18", "MT102"])
# sens.set_ga_grid(range(1, 200, 3))
# print(sens.get_integral_sensitivity())
# print(sens.get_integral_sensitivity(True))
# sens.plot(range(1, 200, 10), True)

ff = CosineSimilarityGPT(sens)
print(ff.get_fitness(range(1, 200, 10)))



#  New version of the upbinning : 0.060601243190966825
#  Old version                  : 0.22994652159656814

# New version, new ff :           0.397625489554401
# Old version, new ff :           0.1988065314198758