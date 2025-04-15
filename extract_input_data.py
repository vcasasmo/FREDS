import numpy as np
import os
import serpentTools

"""
#@Emilie, I discarded everything (functions) not used in this branch, everything is called through extract_data. Anyway, I guess all of this:
(gpt_vector, gpt_vector_per_unit_lethargy, xgpt_energy_grid, gpt_energy_grid)
and in the future, if needed, eigenbasis, perts, ...
Should maybe be extracted in the new Class sensitivities so is  checked by the user to fail-proof it. 

"""
main_path = os.path.join(os.getcwd())





def extract_gpt_sensitivity_coefficients(filepath, zai):
    """
    :param filepath: Computer address of where output of the GPT Serpent computation is stored
    :param zai: zai number of the isotope we want to extract the sensitivity vectors
    :return: Two dictionaries. One whose keys are "MT2", "MT18" and "MT102", and that contains
    the fine GPT-scored sensitivity vectors and one with the same keys, but whose fine
    GPT-scored sensitivity vectors are normalised by unit lethargy
    """

    gpt_reader = serpentTools.read(filepath)

    zai_index = gpt_reader.zais[zai]

    fission_index = gpt_reader.perts["fission xs"] # Fission xs perturbation  #for   cefr works with mt, bfs and sneak with nominative fission xs, ela xs ...
    el_scatter_index = gpt_reader.perts["total xs"] # Elastic scattering xs perturbation
    rad_capt_index = gpt_reader.perts["capture xs"] # Radiative capture xs perturbation

    fission_sensitivities = gpt_reader.sensitivities["keff"][0][zai_index][fission_index]
    el_scatter_sensitivities = gpt_reader.sensitivities["keff"][0][zai_index][el_scatter_index]
    rad_capt_sensitivities = gpt_reader.sensitivities["keff"][0][zai_index][rad_capt_index]

    gpt_vector = {"MT2": np.zeros((226,)), "MT18": np.zeros((226,)), "MT102": np.zeros((226,))}
    gpt_vector_lethargy_normalised = {"MT2": np.zeros((226,)), "MT18": np.zeros((226,)), "MT102": np.zeros((226,))}

    for sensitivities, label in [(fission_sensitivities, "MT18"),
                                (el_scatter_sensitivities, "MT2"),
                                (rad_capt_sensitivities, "MT102")]:
        i = 0
        for sensitivity, error in sensitivities:
            gpt_vector[label][i] = sensitivity
            gpt_vector_lethargy_normalised[label][i] = sensitivity
            i += 1


        gpt_vector_lethargy_normalised[label] /= gpt_reader.lethargyWidths

    return gpt_vector, gpt_vector_lethargy_normalised


## VCasas use this one
def extract_data(isotope,reactions):
    """
    :return: A 6-tuple containing :
                        - The 2 fine GPT-scored sensitivity dictionnaries : unnormalised
                           and normalised per unit lethargy
                        - The fine XGPT-scored sensitivity vector
                        - The ordered dictionary perts, that gives the order of the perturbations
                        - A numpy matrix whose rows contain the eigenfunctions of the POD of the covariance matrices
                        - A numpy matrix whose diagonal is filled with the singular values associated with the eigenfunctions
    """
    filepath_gpt = os.path.join(main_path,"GPT", "godiva.i_sens0.m")

    zai = 942390 if isotope == 'Pu239' else 922380 if isotope == 'U238' else 922350
    gpt_vector, gpt_vector_per_unit_lethargy = extract_gpt_sensitivity_coefficients(filepath_gpt, zai)

    #filepath_xgpt =  os.path.join(main_path, "XGPT", ISOTOPE, "FC_Tf_1073_Tc_1073_sens0.m")
    #xgpt_vector, perts = extract_xgpt_sensitivity_coefficients(filepath_xgpt)

   # filepath_eigen_basis =os.path.join(main_path, "XGPT", ISOTOPE)
    #eigenbasis = extract_eigenbasis(filepath_eigen_basis, perts)

    #singular_value_file_name = 'SVs_Pu-239_' if ISOTOPE == "Pu239" else 'SVs_U-238_' if ISOTOPE == "U238" else "SVs_Pu-239"
    #singular_matrix = extract_singular_matrix(singular_value_file_name, perts)
    xgpt_energy_grid = np.zeros((1501,))
    gpt_energy_grid = np.zeros((227,))
#@Emilie: I moved the energy grids reading to here so we make available these two variables to the main.py scope
#We can move now to fitness_functions.py
    with open(os.path.join(main_path, "1500G.txt"), "r") as file:
        i = 0
        for line in file:
            energy, _ = line.split("\n")
            xgpt_energy_grid[i] = float(energy)
            i += 1

    with open(os.path.join(main_path, "226G.txt"), "r") as file:
        line = file.readline()
        energies = line.split(" ")
        for i in range(227):
            gpt_energy_grid[i] = float(energies[i * 2])

    return (gpt_vector, gpt_vector_per_unit_lethargy, xgpt_energy_grid, gpt_energy_grid)



