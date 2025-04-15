import numpy as np
from sensitivity_reader import GPTSensitivity, XGPTSensitivity

class ObjectiveFunction:
    def __init__(self, sensitivity):
        self.sensitivity = sensitivity

    def cosine_similarity(self, A, B):
        dot_product = np.dot(A, B)
        norm_A = np.linalg.norm(A)
        norm_B = np.linalg.norm(B)
        similarity = dot_product / (norm_A * norm_B)
        return similarity

    def get_fitness(self, ga_grid):
        raise NotImplementedError

class CosineSimilarityGPT(ObjectiveFunction):
    
    def __init__(self, sensitivity):
        if not isinstance(sensitivity, GPTSensitivity):
             raise ValueError("sensitivity must be of type GPTSensitivity")
        super().__init__(sensitivity)
    
    def process_vectors(self):
        evaluated_gpt = []
        reference_gpt = []

        coarse_vector = self.sensitivity.get_evaluated_sensitivity()
        reference_vector = self.sensitivity.get_reference_sensitivity()

        for label, evaluated_values in coarse_vector.items():
            fine_values = reference_vector[label]
            reference_gpt.append(fine_values)
            evaluated_gpt.append(evaluated_values)

        reference_gpt = np.concatenate(reference_gpt)
        evaluated_gpt = np.concatenate(evaluated_gpt)
        return reference_gpt, evaluated_gpt
    
    def _get_fitness(self, ga_grid):
        self.sensitivity.set_ga_grid(ga_grid)
        self.sensitivity.downbin()
        self.sensitivity.upbin()
        reference_gpt, evaluated_gpt = self.process_vectors()
        return 1 - self.cosine_similarity(reference_gpt, evaluated_gpt)


class CosineSimilarityXGPT(ObjectiveFunction):
    def __init__(self, sensitivity):
        if not isinstance(sensitivity, XGPTSensitivity):
             raise ValueError("sensitivity must be of type XGPTSensitivity")
        super().__init__(sensitivity)

    def get_fitness(self, ga_grid):
        return super().get_fitness(ga_grid)
    
    def project_gpt_onto_eigenbasis(self):
        """
        :param ga_grid: The chromosome encoding the test discretisation
        :return: A numpy vector containing the XGPT-scored sensitivity 
            coefficients evaluated on ga_grid
        """
        self.sensitivity.downbin()
        self.sensitivity.upbin()
        projected_gpt = self.sensitivity.projection()
        return projected_gpt
