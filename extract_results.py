from collections import defaultdict
import os
import fitness_functions
from extract_input_data import ISOTOPE

def read_results(n_groups, select="best", switch = False):
    """
    :param n_groups: A list of integers, defining the few-groups
                grids we wish to extract
    :param select: A string. When set to "best", the function 
            retrieve the best discretisations in the file. When set to
            "reccurent", the function retrieve the most reccurent
            discretisations in the file.
    :param switch: A boolean. If set to True, the function retrieves 
                the energy discretisations found with the optimisation
                with the other nuclide.
    
    """

    results = {}
    isotope = ISOTOPE

    # If switch == True, the energy grids retrieved
    # are the one optimised on the other nuclide
    if switch:
        isotope = "U238" if ISOTOPE == "Pu239" else "Pu239"
    
    # Creating a dictionnary containing the name of the method,
    # the fitness function associated to it and its associated
    # color for the graphs
    methods = [
        ("GPT", fitness_functions.compare_vectors_gpt, "m"),
        ("XGPT", fitness_functions.compare_vectors_gpt_xgpt,"darkgreen" ),
        ("uncertainty", fitness_functions.compare_variance_gpt_xgpt, "red")
    ]
    
    # Iteration on each specified group
    for nGroup in n_groups:
        results[nGroup] = {}
        
        # Iteration on each method and fitness function
        for method, fitness_function, color in methods:
            filepath = "{}_{}G.txt".format(method, nGroup)
            filepath = os.path.join(os.getcwd(),"Results",isotope, filepath)
            
            with open(filepath, "r") as file:
                lines = file.readlines()
            
            # Initialising a dictionnary to count the occurences of each discretisation
            list_count = defaultdict(int)

            # Initialising a dummy best fitness
            min_fitness = float('inf')
            best_list = None
            
            # Iterating over every line of the file 
            for line in lines:

                # Pre-processing the discretisations so that 
                # they are converted from a string to a list
                list_data = eval(line.strip()) 
                
                # Compute the fitness of the discretisation
                fitness_value = fitness_function(list_data)
                
                # If the selection has to retrieve the best 
                # fitness, update the best list when a better 
                # list is found
                if select == "best":
                    if fitness_value < min_fitness:
                        min_fitness = fitness_value
                        best_list = list_data

                # If the selection has to retrieve the most
                # reccuring fitness, update the count
                # for this list    
                elif select == "recurrent":
                    list_count[str(list_data)] += 1
            
            # Selection with the "reccurent" criterion
            if select == "recurrent":
                most_common_list = max(list_count, key=list_count.get)
                best_list = eval(most_common_list)  
            
            # Assign the best discretisation and its color
            # for given ngroup and method
            results[nGroup][method] = (color, best_list)
    
    return results
