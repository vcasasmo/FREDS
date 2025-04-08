import numpy as np
from extract_input_data import xgpt_energy_grid, gpt_energy_grid, gpt_vector


def down_binning(gpt_sensitivities, ga_grid, gpt_energy_grid):
    """
    :param gpt_sensitivities: A dictionnary, whose keys
                are "MT2", MT18" and "MT102". The associated values 
                are the fine GPT-scored sensitivity vectors.
    :param ga_energy_grid: The chromosome encoding the test discretisation
    :param gpt_energy_grid: The 226G energy grid on which the fine
                    GPT-scored sensitivity vectors are evaluated
    :return: A dictionnary, whose keys
            are "MT2", MT18" and "MT102". The associated values 
            are the evaluated GPT-scored sensitivity vectors
            whose size is the one defined by the coarse discretisation

    Evaluate the GPT-scored sensitivity vector for each perturbed cross-section
    on the ga_grid
    """

    downbinned = {}
    # Iterating over each reaction
    for reaction, sensitivities in gpt_sensitivities.items():
        downbinned[reaction] = evaluate_on_ga(sensitivities, ga_grid, gpt_energy_grid)
    return downbinned

def evaluate_on_ga(gpt_sensitivity, ga_grid, gpt_energy_grid):
    """
    :param gpt_sensitivity: A numpy array containing the fine GPT-scored 
                    sensitivity coefficients of one perturbed cross section.
    :param ga_grid: The chromosome encoding the test discretisation
    :param gpt_energy_grid: The 226G energy grid on which the fine
                    GPT-scored sensitivity vectors are evaluated
    :return: A numpy array containing the evaluated GPT-scored sensitivity coefficients
            whose size is the one defined by the coarse discretisation

    Evaluate gpt_sensitivity on the ga_grid discretisation
    """


    sensitivities_evaluated = np.zeros((len(ga_grid) + 1,))

    # Defining the index for filling the coarse sensitivity vector
    j = 0

    energies = []

    # Iteration over each sensitivity coefficient
    for i in range(len(gpt_sensitivity)):

        # Defining the current cut. 
        cut = len(gpt_sensitivity) if j >= len(ga_grid) else ga_grid[j]
        prev_cut = 0 if j == 0 else ga_grid[j - 1]

        # If the fine sensitivity coefficient is inside the coarse group 
        # defined by [prev_cut, cut], use it to evaluate the coarse 
        # sensitivity coefficient on that group

        if i >= prev_cut and i < cut:

            # Downbinning involves performing a weighted average, the weights being the energy intervals
            sensitivities_evaluated[j] += gpt_sensitivity[i]*(gpt_energy_grid[i+1]-gpt_energy_grid[i])
            energies.append(gpt_energy_grid[i+1] - gpt_energy_grid[i])

        # If the fine sensitivity coefficient is not inside group [prev_cut, cut], 
        # update prev_cut and cut.
        else :
            sensitivities_evaluated[j] /= np.sum(energies) 
            j += 1
            energies = []
            cut = len(gpt_sensitivity) if j >= len(ga_grid) else ga_grid[j]
            prev_cut = 0 if j == 0 else ga_grid[j - 1]
            sensitivities_evaluated[j] += gpt_sensitivity[i]*(gpt_energy_grid[i+1]-gpt_energy_grid[i])

            energies.append(gpt_energy_grid[i+1] - gpt_energy_grid[i])

    sensitivities_evaluated[-1] /= np.sum(energies) 
    return sensitivities_evaluated


def energy_from_energy_grid(energy_discretisation, ga_grid):
    """
    :param energy discretisation: The fine energy discretisation
                        whose cuts fill the allele pool
    :param ga_grid: The chromosome encoding the test discretisation
    :return: A numpy array containing the ga_grid discretisation as energy values
    Extract the energy discretisation defined by the GA grid
    """
    coarse_energy = np.zeros((len(ga_grid) + 2))
    coarse_energy[0] = energy_discretisation[0]
    i = 1

    for cut in ga_grid:
        #cut = int(cut) #VJCasas temp fix

        coarse_energy[i] = energy_discretisation[cut]
        i += 1
    coarse_energy[-1] = energy_discretisation[-1]

    return coarse_energy

def up_binning(fine_energy_grid, coarse_energy_grid, down_binned_vector):
    """
    :param fine_energy_grid: The energies of the fine discretisation
    we aim at extending the downbinned vector
    :param coarse_energy_grid: The energies of the coarse discretisation
    on which the downbinned vector is evaluated
    :param down_binned_vector: A dictionnary, whose keys
            are "MT2", MT18" and "MT102". The associated values 
            are the sensitivity vectors evaluated on the coarse energy grid
    :return: A dictionnary, whose keys are  "MT2", MT18" and "MT102".
      The associated values are the sensitivity vectors upbinned to the fine energy grid
    """
    upbinned = {}
    for reaction, down_binned_sensitivity in down_binned_vector.items():
        upbinned[reaction] = extend(fine_energy_grid, coarse_energy_grid, down_binned_sensitivity)
    return upbinned

def extend(fine_energy_grid, coarse_energy_grid, down_binned_sensitivity):
    """
    :param fine_energy_grid: The energies of the fine discretisation
    we aim at extending the downbinned vector
    :param coarse_energy_grid: The energies of the coarse discretisation
    on which the downbinned vector is evaluated
    :param down_binned_vector: An array containing the sensitivity coefficients
                evaluated on the coarse energy grid
    :return: A array of the sensitivity vector extended onto the fine energy grid
    """
    up_binned_vector = np.zeros( (len(fine_energy_grid) - 1, ) )
    j = 1
    for i in range(1, len(fine_energy_grid)):
        # Energy on the left side of the coarse group
        prev_energy = coarse_energy_grid[j - 1]
        # Energy on the right side of the coarse group
        energy = coarse_energy_grid[j]

        # If the fine sensitivity coefficients is inside the coarse group [prev_energy, energy],
        # copy the coarse sensitivity coefficient as the fine sensitivity coefficient value
        if fine_energy_grid[i] >= prev_energy and fine_energy_grid[i] <= energy:
            up_binned_vector[i - 1] = down_binned_sensitivity[j - 1]

            # If the fine energy matches the right side 
            # of the coarse group, move on to the next group
            if fine_energy_grid[i] == energy:
                j += 1

    return up_binned_vector

# Projection onto the eigen basis 
def projection(dict_sensitivity, eigenbasis):
    """
    :param dict_sensitivity: A dictionnary, whose keys are "MT2", "MT18" and "MT102",
      containing the evaluated and extended sensitivity profiles.
    :param eigenbasis: A numpy matrix containing as its rows the eigenfunctions of the
      POD of the covariance matrices of MT2, MT18 and MT102?

    """
    projected_sensitivity = []

    # Projecting in the order defined by the perts dictionnary
    for label, index in perts.items():
        if index == 0:
            continue
        _, label, _ = label.split("_")
        sensitivity = dict_sensitivity[label]
        projected_sensitivity.append(np.sum(np.array(sensitivity)*np.array(eigenbasis[index-1])))
        
    return np.array(projected_sensitivity)

def project_gpt_onto_eigenbasis(ga_grid):
    """
    :param ga_grid: The chromosome encoding the test discretisation
    :return: A numpy vector containing the XGPT-scored sensitivity 
        coefficients evaluated on ga_grid
    """
    coarse_gpt = down_binning(gpt_vector, ga_grid, gpt_energy_grid)
    ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, ga_grid)
    extended_gpt_ga = up_binning(xgpt_energy_grid, ga_energy_grid, coarse_gpt)
    projected_gpt = projection(extended_gpt_ga, eigenbasis)
    return projected_gpt

def cosine_similarity(A, B):
    """
    :param A: A numpy vector
    :param B: A numpy vector
    :return: The cosine similarity of A and B
    """
    dot_product = np.dot(A, B)
    norm_A = np.linalg.norm(A)
    norm_B = np.linalg.norm(B)
    similarity = dot_product / (norm_A * norm_B)
    return similarity

