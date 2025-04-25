
# Fast Reactor Energy Grid Design For Sensitivity Calculations (FREDS)

This code was jointly developed by researchers from the Belgian Nuclear Research Centre (SCK CEN), ULB, and UGent, based on the early implementation developed by Emilie3008 and available at [Emilie3008/MScThesis_2023_2024](https://github.com/Emilie3008/MScThveloped using Python version 3.12.0, as well as the following libraries and their versions:
- `numpy` version 1.26.4
- `serpentTools` version 0.10.1
- `pandas` version 1.3.2
- `iracepy` version 0.0.1 (with R 4.4.0 installed)
- `pymoo` version 0.6.1.3

## Abstract

Correctly characterizing the sensitivity vectors is crucial for obtaining reliable information on the response of a perturbed nuclear system. Ideally, case-specific energy grids should be used, but the difficulty of the design encourages the use of general-purpose energy grids. In this work, we explore the possibility of using genetic algorithms (GA) as a search method for the design of energy grids used in the framework of fast reactors sensitivity calculations.

The main idea behind the three proposed fitness functions is to measure how well a sensitivity vector evaluated on a few-group discretization represents the same sensitivity vector scored on a many-group energy discretization.

On the one hand, we explore the possibility of computing the many-group sensitivities with Generalized Perturbation Theory (GPT) or its recently updated version, eXtended GPT (XGPT). On the other hand, we investigate the possibility of assessing the similarity between the many- and few-group scored sensitivity vectors through cosine similarity.

The algorithm performs Multi-objective Optimization (MOO), learning the Pareto front between multiple objective functions. This capability allows the code to explore optimal energy grids for a given number of discretizations. Users can then select the configuration that best fits their applications based on their computational budget. The MOO is performed by setting a problem context where the user defines:
1. The number of sensitivities for which the optimization should be made.
2. Whether minimizing the number of discretizations (Number of Groups) is required.
3. The problem context, i.e., max number of generations, seed, criteria (XGPT or GPT), etc.

For single-objective problems, i.e., minimizing the dissimilarity between a fine and a coarser grid, the in-house GA is employed by default. For two objective functions, FREDS uses the powerful NSGA-II implemented in `pymoo`. For three or more fitness functions, FREDS defaults to the NSGA-III algorithm implemented in `pymoo`. However, users are free to customize the algorithm and its parameters in any case by calling a different algorithm from the `pymoo` suite. In principle, more than three objective functions can be added to the context. However, the developers cannot guarantee satisfactory results for problems with more than three objective functions. In any case, FREDS will yield a collection of convergence and performance metrics to assess a particular run.

## Usage
To get started with FREDS, you can use the `test.ipynb` notebook provided in the repository. This notebook will guide you through the functionalities of the software, demonstrating how to set up and run sensitivity calculations and optimizations.
