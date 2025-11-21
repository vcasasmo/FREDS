
from FREDS import FREDS
from sensitivity import GPTSensitivity, XGPTSensitivity



notation_dict = {"total xs":"MT1", "ela scatt xs":"MT2",
                 "fission xs": "MT18",  "capture xs":"MT102"}


sensitivity = GPTSensitivity( filepath        = "GPT/main_sens0.m",
                              observable      = "keff",
                              zai             = 922380,
                              perts           = ["MT2", "MT18", "MT102"],
                              notation_dict   = notation_dict)

# 2. Now, let's set the problem context

# 1. First, definition of the XGPT sensitivities we want to optimize for:

objective_0= XGPTSensitivity(filepath_xgpt   = "XGPT/U238/FC_Tf_1073_Tc_1073_sens0.m",
                              filepath_gpt    = "GPT/main_sens0.m",
                              filepath_eigfct = "XGPT/U238",
                              observable      = "keff",
                              zai             = 922380,  #w.r.t. U238
                              perts           = ["MT2", "MT18", "MT102"],
                              notation_dict   = notation_dict)

objective_1 = XGPTSensitivity(filepath_xgpt   = "XGPT/Pu239/FC_Tf_1073_Tc_1073_sens0.m",
                              filepath_gpt    = "GPT/main_sens0.m",
                              filepath_eigfct = "XGPT/Pu239",
                              observable      = "keff",
                              zai             = 942390, #w.r.t. Pu239
                              perts           = ["MT2", "MT18", "MT102"],
                              notation_dict   = notation_dict)
# FREDS.SetProblem(
#     n_groups=33,  #Maximum number of groups
#     sensitivities=([objective_0]),  # simultaneously optimize
#     criteria='XGPT',
#     optimize_groups=True,  #Making this True, will jointly minimize the defined fitness and the number of groups
# )
# #3. Run FREDS

# FREDS.run()


FREDS.SetProblem(
    n_groups=33,  #Maximum number of groups
    sensitivities=([objective_0,objective_1]),  # simultaneously optimize
    criteria='XGPT',
    optimize_groups=True,  #Making this True, will jointly minimize the defined fitness and the number of groups
)
# #3. Run FREDS

FREDS.run()
#4. For multi-objective problems, we can save and print results
FREDS.save_results('results_demo.csv')  #fi

FREDS.plot_pareto_front()
FREDS.plot_results(index = 0)
FREDS.plot_results(index = "All")



# FREDS.load_results('result_FREDS/results_demo.csv')
# FREDS.plot_pareto_front()