import numpy as np
import os
import serpentTools
import pandas as pd

main_path = os.path.join(os.getcwd())

# ________ Defining the nuclide the optimisation will be performed on ________
with open(os.path.join(main_path, "isotope.txt"), "r") as file:
    ISOTOPE = file.readlines()[0]

# ________ Extracting the GPT and XGPT fine energy grids ________
xgpt_energy_grid = np.zeros((1501,))
gpt_energy_grid = np.zeros((227,))

with open(os.path.join(main_path, "1500G.txt"), "r") as file:
    i = 0
    for line in file:
        energy, _= line.split("\n")
        xgpt_energy_grid[i] = float(energy)
        i += 1

with open(os.path.join(main_path, "226G.txt"), "r") as file:
    line = file.readline()
    energies = line.split(" ")
    for i in range(227):
        gpt_energy_grid[i] = float(energies[i*2])

def extract_xgpt_sensitivity_coefficients(filepath):
    """
    :param filepath: Computer address where the output of the XGPT Serpent computation is localised
    :return: The fine XGPT-scored vector and an OrderedDict containing the order of the perturbations
    """
    xgpt_reader = serpentTools.read(filepath)

    sensitivities = xgpt_reader.energyIntegratedSens["keff"][0][0]
    perts = xgpt_reader.perts
    xgpt_vector = np.zeros((len(perts)-1,))

    i = -1
    for sensitivity, error in sensitivities:
        if i==-1:
            i+= 1
            continue
        xgpt_vector[i] = sensitivity
        i += 1

    return xgpt_vector, perts

def extract_eigenbasis(filepath, perts):
    """
    :param filepath: Computer address of the folder where the eigenfunctions are stored
    :param perts: an OrderedDict containing the order of the perturbations
    :return: A numpy matrix whose rows are filled with the eigenfunctions of the POD of 
        the covariance matrices
    """
    eigenbasis = np.zeros((len(perts)-1, len(xgpt_energy_grid)-1))
    for label, index in perts.items():
        if index == 0:
            continue
        filename = os.path.join(filepath, label+'.txt')
        with open(filename) as file:
            lines = file.readlines()
            i = 0
            # First two lines are useless
            for line in lines[2:]:
                energy, basis_coeff = line.split(" ")
                basis_coeff, _ = basis_coeff.split("\n")
                eigenbasis[index - 1][i] = float(basis_coeff)
                i += 1

    return eigenbasis


def extract_gpt_sensitivity_coefficients(filepath, zai):
    """
    :param filepath: Computer address of where output of the GPT Serpent computation is stored
    :param zai: zai number of the isotope we want to extract the sensitivity vectors
    :return: Two dictionnaries. One whose keys are "MT2", "MT18" and "MT102", and that contains 
    the fine GPT-scored sensitivity vectors and one with the same keys, but whose fine 
    GPT-scored sensitivity vectors are normalised by unit lethargy
    """

    gpt_reader = serpentTools.read(filepath)

    zai_index = gpt_reader.zais[zai] 

    fission_index = gpt_reader.perts["fission xs"] # Fission xs perturbation  #for   cefr works with mt, bfs and sneak with nomiative fission xs, ela xs ... 
    el_scatter_index = gpt_reader.perts["ela scatt xs"] # Elastic scattering xs perturbation
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


def extract_singular_matrix(filename, perts):
    """
    :param filepath: Computer address of the folder where the singular values are stored
    :param perts: an OrderedDict containing the order of the perturbations
    :return: A numpy matrix whose diagonal is filled with the singular values of the eigenbasis.
    """
    m = len(perts) - 1
    singular_matrix = np.zeros((m, m))
    
    # Filling the matrix in the order defined by perts
    for label, index in perts.items():
        if index > 0:
            index = index - 1
            zai, mt, number = label.split("_")
            _, MT_num = mt.split("MT")
            file_name = os.path.join(main_path, "XGPT", ISOTOPE, filename + ".txt") if ISOTOPE =="Pu239_full_cov" else os.path.join(main_path, "XGPT", ISOTOPE, filename + MT_num + ".txt") 


            with open(file_name, 'r') as file:
                lines = file.readlines()
                sv, _ = lines[ int(number) - 1 ].split("\n")
                singular_matrix[index][index] = float(sv)

    return singular_matrix


def extract_covariance_matrix(single = False, name = None):
    """
    :param single : A boolean. If set to True, the extracted covariance is a 
    single-covariance matrix. Else, it is the full covariance matrix
    :return: A DataFrame containing the covariance matrice of the perturbed 
    cross sections for reactions MT2, MT18 and MT18
    """
    filename = "{}_xs_reduced.csv".format(ISOTOPE) if name is None else name
    csv_file = os.path.join(main_path, "CovarianceMatrices", filename)
    covariance_matrix = pd.read_csv(csv_file, header=[0,1,2], index_col=[0,1,2])

    # Filtrering out MT4 data
    covariance_matrix = covariance_matrix.loc[covariance_matrix.index.get_level_values(1) != 4]
    cov_matrix = covariance_matrix.loc[:, covariance_matrix.columns.get_level_values(1) != '4']

    # If the single covariance approach is adoptedn filtering out
    # the inter-reaction contributions
    if single:
        levels_2 = cov_matrix.index.get_level_values(1).unique()
        new_cov_matrix = pd.DataFrame(
            np.zeros_like(cov_matrix), 
            index=cov_matrix.index, 
            columns=cov_matrix.columns
        )

       
        for level_2 in levels_2:
            
            idx = (cov_matrix.index.get_level_values(1) == level_2)
            col = (cov_matrix.columns.get_level_values(1) == str(level_2))
            
            filtered_index = cov_matrix.index[idx]
            filtered_column = cov_matrix.columns[col]

            sub_cov_matrix = cov_matrix.loc[filtered_index, filtered_column]
            new_cov_matrix.loc[filtered_index, filtered_column] = sub_cov_matrix
        cov_matrix = new_cov_matrix

    return cov_matrix
## VCasas use this one
def extract_data():
    """
    :return: A 6-tuple containing :
                        - The 2 fine GPT-scored sensitivity dictionnaries : unnormalised
                           and normalised per unit lethargy
                        - The fine XGPT-scored sensitivity vector
                        - The ordered dictionnary perts, that gives the order of the pertubations
                        - A numpy matrix whose rows contain the eigenfunctions of the POD of the covariance matrices
                        - A numpy matrix whose diagonal is filled with the singular values associated with the eigenfunctions
    """
    filepath_gpt = os.path.join(main_path,"GPT", "sneak_4A_sens0.m")
    
    zai =  942390 if ISOTOPE == 'Pu239' else 922380
    gpt_vector, gpt_vector_per_unit_lethargy = extract_gpt_sensitivity_coefficients(filepath_gpt, zai)

    #filepath_xgpt =  os.path.join(main_path, "XGPT", ISOTOPE, "FC_Tf_1073_Tc_1073_sens0.m")
    #xgpt_vector, perts = extract_xgpt_sensitivity_coefficients(filepath_xgpt)

   # filepath_eigen_basis =os.path.join(main_path, "XGPT", ISOTOPE)
    #eigenbasis = extract_eigenbasis(filepath_eigen_basis, perts)

    #singular_value_file_name = 'SVs_Pu-239_' if ISOTOPE == "Pu239" else 'SVs_U-238_' if ISOTOPE == "U238" else "SVs_Pu-239"
    #singular_matrix = extract_singular_matrix(singular_value_file_name, perts)

    return (gpt_vector, gpt_vector_per_unit_lethargy)

gpt_vector, gpt_vector_lethargy_normalised = extract_data()


def compute_variance_gpt(single=True):
    """
    :param single: A boolean. Defines wether the covariance is full of single
    Compute the variance of the GPT-scored fine vector through the classical sandwich rule
    """
    sens_vec = np.concatenate( [gpt_vector["MT2"], gpt_vector["MT18"], gpt_vector["MT102"] ])
    covariance_matrix = extract_covariance_matrix(single)
    covariance_mat = covariance_matrix.values
    variance = sens_vec.T @ covariance_mat @ sens_vec
    return variance

def extract_myrrha_sensitivities():
    gpt_reader = serpentTools.read(os.path.join(os.getcwd(), "sneak_4A_sens0.m"))
    zai = 942390 if ISOTOPE == 'Pu239' else 922380
    zai_index = gpt_reader.zais[zai] 

    fission_index = gpt_reader.perts["capture xs"] # "it was capture xs before,Fission xs perturbation  #VCasas changed because of Serpent2, sometimes comes swap.
    el_scatter_index = gpt_reader.perts["ela scatt xs"] # Elastic scattering xs perturbation
    rad_capt_index = gpt_reader.perts["mt 18 xs"] # Radiative capture xs perturbation

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

ECCO33 = sorted([1.9640330000E+01,1.0000000000E+01, 6.0653070000E+00, 3.6787940000E+00,
           2.2313020000E+00, 1.3533530000E+00, 8.2085000000E-01, 4.9787070000E-01, 3.0197380000E-01,
           1.8315640000E-01, 1.1109000000E-01, 6.7379470000E-02, 4.0867710000E-02, 2.4787520000E-02,
           1.5034390000E-02, 9.1188200000E-03, 5.5308440000E-03, 3.3546260000E-03, 2.0346840000E-03, 
           1.2340980000E-03, 7.4851830000E-04, 4.5399930000E-04, 3.0432480000E-04, 1.4862540000E-04,
           9.1660880000E-05, 6.7904050000E-05, 4.0169000000E-05, 2.2603290000E-05, 1.3709590000E-05,
           8.3152870000E-06, 4.0000000000E-06, 5.4000000000E-07, 1.0000000000E-07, 1.0000100000E-11])
