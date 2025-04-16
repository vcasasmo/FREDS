import random
import numpy as np
from fitnessFunctions import CosineSimilarityGPT, CosineSimilarityXGPT
from sensitivity_reader import GPTSensitivity, XGPTSensitivity

allele_pool = range(1, 226)
fitness_library = dict()
fitness_function = None


class GeneticAlgorithm():

    class Individual():
        def __init__(self, chromosome):
            """
            :param chromosome: A list of integers, representing the real coded chromosome, with integers as its allele values.
            """
            self.chromosome = sorted(chromosome)
            self.fitness = self._get_fitness()
            
        def _get_fitness(self):
            """
            :return: A numerical value being the fitness of the individual.
              If the fitness has already been computed, it is retrieved from fitness_library. 
              Else, the fitness is computed and then stored in fitness_library
            """
            if tuple(self.get_chromosome()) not in fitness_library:
                fitness = fitness_function.get_fitness(self.get_chromosome())

                fitness_library[tuple(self.get_chromosome())] = fitness

            return fitness_library[tuple(self.get_chromosome())]
        
        def get_chromosome(self):
            """
            Return the sorted chromosome of the individual. 
            """
            return sorted(self.chromosome)
        
    def __init__(self, nGroups, sensitivity, pop_size = 500,
                  pm = 0.035, pc = 1, no_tournament = False,
                  elitism = 0.027, adaptive = True, soft_mutation = 1, 
                  p = 0.55, NT = 1, multi_parent = 6):
        
        global fitness_function
        fitness_function = CosineSimilarityGPT(sensitivity) if isinstance(sensitivity, GPTSensitivity) else CosineSimilarityXGPT(sensitivity) if isinstance(sensitivity, XGPTSensitivity) else None
        if fitness_function is None:
            raise ValueError("Invalid sensitivity vector")
        
        # Classical Genetic algorithm parametrisation
        self.nGroups = nGroups - 1
        self.pop_size = pop_size
        self.allele_pool = allele_pool
        self.pm = pm
        self.mutation_rate = self.pm
        self.pc = pc
        self.elitism = elitism
        self.no_tournament = no_tournament

        # Stochastic tournament selection parametrisation
        self.NT = NT
        self.p = p
        
        # Adaptive mutation rate parametrisation
        self.adaptive = adaptive
        self.best_fitness = float('inf')
        self.soft_mutation = soft_mutation
        self.best_generation = -1 
        self.mean_fitness = -1

        # Multi-parent reproduction parametrisation
        self.multi_parent = multi_parent

    def new_individual(self):
        """
        :return: a randomly generated instance of the class Individual
        """
        chromosome = [random.choice(self.allele_pool) for
                       _ in range(self.nGroups)]

        return self.Individual(self.repair(chromosome))
    
    def repair(self, chromosome):
        """
        :param chromosome: A list of integer, possibly containing duplicated alleles
        :return: The same chromosome, but repaired from duplicated alleles, 
                these being replaced by random alleles from the allele pool.
        """
        registered = []
        for i in range(len(chromosome)):
            if chromosome[i] not in allele_pool:
                chromosome[i] = self.mutated_allele(exclude = 
                                                    chromosome)
            elif chromosome[i] not in registered:
                registered.append(chromosome[i])
            else:
                # If the allele has already been registered, then
                # it is replaced by a random allele which is not
                # already present in the chromosome
                chromosome[i] = self.mutated_allele(exclude = 
                                                    chromosome)
        
        return sorted(chromosome)
    
    def mutated_allele(self, exclude = list()):
        """
        :param exclude: (Optionnal) A list of integers
        :return: A random integer from the allele pool which is not in the exclude list
        
        """
        allele = random.choice([allele for allele in 
                                self.allele_pool if allele
                                  not in exclude])
        return allele
    
    def transfer_fitness (self, chromosome):
        fitness = self.Individual(chromosome).fitness
        return fitness
    
    def mutation(self, chromosome):
        """
        :param chromosome: A list of integers
        :return: The list of integers after it has undergone mutations
        """

        # Retrieving chromosome fitness before mutation

        fitness = self.Individual(chromosome).fitness
        prob = 0.5

        # If the solution is fitter than the average of the population 
        # and the mutation rate is adaptive, then the probability for 
        # it to undergo a soft-mutation is set to // self.soft_mutation //
        if fitness < self.best_fitness and self.adaptive:
            prob = self.soft_mutation

        # Iteration over all the genes of the chromosome
        for i in range(len(chromosome)):    

            # Each gene has a probability to undergo a mutation
            p = random.random()
            if p < self.mutation_rate:

                # Determining whether the mutation will be random or soft
                if random.random() > prob :
                    chromosome[i] = random.choice(self.allele_pool)
                else:
                    # The cut is shifted to the left or to the right with an equal probability
                    chromosome[i] += -1 if random.random() < 0.5 else 1

        # Chromosome repair because the mutation may have introduced duplicates
        chromosome = self.repair(chromosome)
        return chromosome
    
    def tournament(self, population):
        """
        :param population : A list of Individuals
        :return: A mating pool constructed under stochastic tournament selection
        """

        mating_pool = list()
        tournaments = {key: list() for key in range(self.NT)}

        # Every individual is randomly assigned to a tournament
        for individual in population:
            tournament = random.choice(range(self.NT))
            tournaments[tournament].append(individual)

        # Competition in every tournament
        for tournament, individuals in tournaments.items():

            # Ranking individuals inside of a tournament
            individuals = sorted(individuals, key = lambda x: x.fitness)

            for rank, individual in enumerate(individuals):
                # Fill the mating pool with a certain number of individuals depending on the weight w
                w = self.p * (1 - self.p)**rank
                w*=100
                mating_pool += [individual]* int(w)
        return mating_pool

    def create_offspring(self, parent1, parent2):
        """
        :param parent1: An instance of the class Individual
        :param parent2: An instance of the class Individual
        :return: Two instances of the class Individual, created by single-point crossover.
        """

        p = random.random()
        # There is a probability 1 - pc that no reproduction occurs.
        if p > self.pc:
            # Mutation still occurs
            p1 = self.Individual(self.mutation(parent1.get_chromosome()))
            p2 = self.Individual(self.mutation(parent2.get_chromosome()))
            return [p1,p2]
        
        # The crossover point is randomly decided
        XO = random.choice(range(1, self.nGroups-1))
        # Single-point crossover
        offspring1 = parent1.get_chromosome()[:XO] + parent2.get_chromosome()[XO:]
        offspring2 = parent2.get_chromosome()[:XO] + parent1.get_chromosome()[XO:]
        
        # Mutation of the offsprings
        mutated_offspring1 = self.Individual(self.mutation(offspring1))
        mutated_offspring2 = self.Individual(self.mutation(offspring2))

        return (mutated_offspring1, mutated_offspring2)
    
    def chose_gene_from_parents(self, parent_list, index):
        """
        :param parent_list: A list of parents, instances of the Individual class, sorted inversely according to the fitness
        :param index: An integer, index of the gene which will be transmitted to the offspring
        :return: The allele that will be transmitted to the offsping in "index" 
        """
        p = random.random()
        probability = 0
        n = len(parent_list)

        for j in range(1, n+1):

            # Rank-based selection
            probability += 2*j/(n*(n-1))

            if probability >= p:
                return parent_list[j-1].chromosome[index]
            
        return parent_list[-1].chromosome[index]
    
    
    def create_offspring_from_multiple_parents(self, parent_list):
        """
        :param parent_list: A list of parents, instances of the Individual class
        :return: An offspring instance of the class Individual, created from multi-parent fitness-based reproduction
        """
        offspring = list()
        # Fitness-based reverse sorting
        parent_list = sorted(parent_list, key = lambda x: x.fitness, reverse=True)

        # Iterating over the genes of the offspring
        for i in range(self.nGroups):
            offspring.append(self.chose_gene_from_parents(parent_list, i))

        return self.Individual(self.mutation(offspring))
    
    def update_mean_fitness(self, population):
        """
        :param population: A list of instances of the Individual class
        
        Update the average fitness of the population
        """
        fitness = 0
        for indiv in population:
            fitness += indiv.fitness
        self.mean_fitness = fitness/len(population)
    
    def run_genetic_algorithm(self, seed, max_iter = 100, tol = 0.0,
                               max_stagnating_iter = 50, display = True):
        """
        :param seed: An integer to set the random seed
        :param max_iter: An integer to set the maximal number of iterations
        :param tol: The stopping criterion as a tolerance on the best fitness
        :param max_stagnating_iter: Stopping criterion on the maximal number 
                                    of stagnating iterations
        :param display: A boolean. If True, a recap of the best performing 
                        fitness is displayed at the end of each generation
        
        Run the genetic algorithm
        """

        # Emptying the fitness library from previous runs
        global fitness_library

        fitness_library = dict()

        random.seed(seed)
        population = []
        generation = 0

        # Random generation of the initial population
        for _ in range(self.pop_size):
            population.append(self.new_individual())

        # Fitness-based sorting of the Individuals
        population = sorted(population, key = lambda x:x.fitness)  
        
        stagnating_iter = 0
        while(generation < max_iter and 
            population[0].fitness > tol and stagnating_iter < max_stagnating_iter):
        
            if display:
                print("Best chromosome {} of fitness {}, generation {} \n".format(
                    population[0].get_chromosome(), population[0].fitness, generation))
            
            # A percentage // elitism // of the solutions is passed on to the new population
            new_population = population[:int(self.pop_size*self.elitism)]

            # Creation of the mating pool
            mating_pool = self.tournament(population) if not self.no_tournament else population[:self.pop_size//2]


            # Continuing the breeding process while the population is not renewed
            while len(new_population) < self.pop_size:

                # Multi-parent reproduction
                if self.multi_parent is not None:
                    parent_list =list()
                    for _ in range(self.multi_parent):
                        parent_list.append(random.choice(mating_pool))
                    offspring = self.create_offspring_from_multiple_parents(parent_list)
                    new_population.append(offspring)
                    
                # Single-point crossover reproduction
                else :
                    parent1 = random.choice(mating_pool)
                    parent2 = random.choice(mating_pool)
                    for offspring in self.create_offspring(parent1, parent2):
                        new_population.append(offspring)

            population = new_population
            generation += 1
            population = sorted(population, key=lambda x:x.fitness) 
        
            
            if population[0].fitness < self.best_fitness:
                self.best_fitness = population[0].fitness
                stagnating_iter = 0
            else:
                stagnating_iter += 1

            if self.adaptive :
                # Udpate of the mean fitness
                self.update_mean_fitness(population)

                # Update of the mutation rate
                self.mutation_rate = 2*(1/(1+np.exp(-(generation-self.best_generation))) - 0.5)*self.pm

        return generation, population[0].fitness, population[0].get_chromosome()
