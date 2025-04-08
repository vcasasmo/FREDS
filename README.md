# Fast Reactor Energy Grid Design For Sensitivity Calculations (FREDS)

This code was jointly developed from researchers of Belgian Nuclear Centre (SCK CEN), ULB and  UGent based on the early implementation developed by @Emilie3008 and available in  https://github.com/Emilie3008/MScThesis_2023_2024. 

## Pre-requisites

This code was developped using Python version 12.3.0, as well as the following libraries and their versions:
- numpy version 1.26.4
- serpentTools version 0.10.1
- pandas version 1.3.2
- iracepy version 0.0.1, with R 4.4.0 installed
- pymoo 0.6.1.3 

## Abstract

Correctly characterising the sensitivity vectors is a crucial step in obtaining reliable information on the response of a perturbed nuclear system. Ideally, case-specific energy grids should be used, but the difficulty of the design encourages the use of general-purpose energy grids. In this work, we explore the possibility of using genetic algorithms (GA) as a search method for the design of energy grids used in the framework of fast reactors sensitivity calculations.

The main idea behind the three proposed fitness functions is to measure how good a sensitivity vector evaluated on a few-group discretisations is at accurately representing the same sensitivity vector, but scored on a many-group energy discretisations.

On the one hand, the possibility of computing the many-groups sensitivities with Generalised Perturbation Theory (GPT), or with its recently updated version eXtended GPT (XGPT), is explored. On the other hand, we investigate the possibility of assessing the similarity between the many- and few-group scored sensitivity vectors through a cosine similarity or by comparing the variance on the response.

 The algorithm performs Multi-objective Optimization (MOO), where it learns the Pareto front between multiple objective functions. This capability allows the code to explore optimal energy grids for a given number of discretizations. Users can then select the configuration that best fits their applications based on their computational budget. For the moment only a Fitness Function (I) and minimizing the number of discretisations (II) are objective functions supported for MOO.