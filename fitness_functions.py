import numpy as np
from extract_input_data import gpt_energy_grid, gpt_vector, gpt_vector_lethargy_normalised
from fitness_utils import cosine_similarity, down_binning, up_binning, energy_from_energy_grid, project_gpt_onto_eigenbasis

def compare_vectors_gpt_xgpt(ga_grid):
    """

    :param ga_grid: Chromosome encoded discretisation 
                    that we aim to measure the fitness
    Compare through a cosine similarity the evaluated and
    fine XGPT-scored sensitivity coefficients
    """
    
    # Evaluate the XGPT-scored sensitivity on ga_grid

    evaluated_xgpt = project_gpt_onto_eigenbasis(ga_grid)

    # The fitness function is defined as 1 - cosine(A, B)
    #  since the GA minimises the fitnesses

    return  1-cosine_similarity(evaluated_xgpt , xgpt_vector)


def compare_variance_gpt_xgpt(ga_grid):
    """
    :param ga_grid: Chromosome encoded discretisation 
                    that we aim to measure the fitness
    Compare the variance on keff, carried by the evaluated and
    fine XGPT-scored sensitivity coefficients
    """
    # Evaluate the XGPT-scored sensitivity on ga_grid

    evaluated_xgpt = project_gpt_onto_eigenbasis(ga_grid)

    # Compute the variance throught the modified sandwich rule
    variance_evaluated_xgpt = evaluated_xgpt @ singular_matrix @ evaluated_xgpt.T
    variance_fine_xgpt = xgpt_vector @ singular_matrix @ xgpt_vector.T

    # The fitness is defined as the absolute difference of the 
    # variance computed with the fine and evaluated vectors
    return  abs(variance_fine_xgpt - variance_evaluated_xgpt)

def compare_vectors_gpt(ga_grid):
    """
    :param ga_grid: Chromosome encoded discretisation 
                    that we aim to measure the fitness
    Compare through a cosine similarity the evaluated and
    fine GPT-scored sensitivity coefficients
    """

    # Evaluated the fine GPT-scored sensitivity vector on ga_grid
    gpt_ga = down_binning(gpt_vector_lethargy_normalised, ga_grid, gpt_energy_grid)
   
    # Retrieve the energy discretisation defined by ga_grid

    ga_energy_grid = energy_from_energy_grid(gpt_energy_grid, ga_grid)
    
    # Upbinning the evaluated GPT-scored vector to the 226G energy grid
    extended_gpt_ga = up_binning(gpt_energy_grid, ga_energy_grid, gpt_ga)

    evaluated_gpt = []
    fine_gpt = []
    # Concatenating the vectors for each perturbation
    for label, evaluated_values in extended_gpt_ga.items():
        fine_values = gpt_vector[label]
        fine_gpt.append(fine_values)
        evaluated_gpt.append(evaluated_values)

    # The fitness function is defined as 1 - cosine(A, B)
    #  since the GA minimises the fitnesses
    return 1 - cosine_similarity(np.concatenate(fine_gpt), np.concatenate(evaluated_gpt))
