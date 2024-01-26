import numpy as np
PRINT = False
class Genetic:
    num_params = 0
    pop_size = 0
    nbits = 0
    population = []

    def __init__(self, num_params, pop_size, nbits):
        self.num_params = num_params
        self.pop_size = pop_size
        self.nbits = nbits
        self.fitness = np.zeros((self.pop_size, 1))
        self.fit_fun = np.zeros
        self.cvalues = np.zeros((self.pop_size, num_params))
        self.num_generations = 1
        self.mutation_prob = 0
        self.crossover_prob = 0
        self.bestIndividual = []
        self.bestIndividualFitness = -1e10
        self.genBestFitness = np.zeros((self.num_generations,))
        self.FitnessRecord = np.zeros((self.num_generations,))
        self.genAvgFitness = np.zeros((self.num_generations,))
        self.current_gen = 0

    def set_sim_parameters(self, num_generations, mutation_prob, crossover_prob):
        # set the simulation/evolution parameters to execute the optimization
        # initialize the result matrices
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.bestIndividual = []
        self.bestIndividualFitness = -1e10
        self.genBestFitness = np.zeros((num_generations,))
        self.FitnessRecord = np.zeros((num_generations,))
        self.genAvgFitness = np.zeros((num_generations,))
        self.current_gen = 0

    def set_fit_fun(self, fun):
        # Set the fitness function
        self.fit_fun = fun

    def init_pop(self):
        self.population = np.random.randint(2, size=(self.pop_size, self.num_params * self.nbits))

    def encode_individuals(self):
        binary_16bits = ufloat2bin(self.cvalues.flatten(), self.nbits)

        row = int(self.pop_size)
        column = int(self.nbits * self.num_params)
        self.population = binary_16bits.reshape(row, column)

    def decode_individuals(self):
        row = int(len(self.cvalues) * self.num_params)  # 20
        column = int(self.nbits)  # 16
        population_16bits = self.population.reshape((row, column))

        values_1D = bin2ufloat(population_16bits, self.nbits)
        self.cvalues = values_1D.reshape((self.pop_size, self.num_params))

    def eval_fit(self):
        # WARNING, number of arguments need to be adjusted if fitness function changes
        self.fitness = self.fit_fun(self.cvalues[:, 0], self.cvalues[:, 1])

        if np.max(self.fitness) > self.bestIndividualFitness:
            self.bestIndividualFitness = np.max(self.fitness)
            self.bestIndividual = self.population[self.fitness == np.max(self.fitness)][0]

        self.genBestFitness[self.current_gen] = np.max(self.fitness)
        self.FitnessRecord[self.current_gen] = self.bestIndividualFitness
        self.genAvgFitness[self.current_gen] = np.mean(self.fitness)

    def print_progress(self):
        # Prints the results of the current generation in the console
        print('Generation no.%d: best fitness is %f, average is %f' %
              (self.current_gen, self.genBestFitness[self.current_gen],
               self.genAvgFitness[self.current_gen]))
        print('Overall best fitness is %f' % self.bestIndividualFitness)
        print('')

    def print_best_individual(self):
        # Prints the best individual for all of the simulated generations
        print('Encoded value:')
        print(self.bestIndividual)

        print('Decoded value:')
        bestIndividual_16bits = np.reshape(self.bestIndividual, newshape=(self.num_params, self.nbits))
        print(bin2ufloat(bestIndividual_16bits, self.nbits))


    def doSelection(self):
        # Output:
        # - PAIRS, a list of two ndarrays [IND1 IND2]  each encoding one member of the pair
        NUMPAIRS = int(self.pop_size / 2)

        lowest_value = 0
        for fitness in self.fitness:
            if fitness < lowest_value:
                lowest_value = fitness

        positive_fitness = []

        if lowest_value < 0:
            for fitness in self.fitness:
                positive_fitness.append(fitness - lowest_value)

        else:
            positive_fitness = self.fitness

        sum = np.sum(positive_fitness)
        probability = []

        for fitness in positive_fitness:
            probability.append(fitness / sum)


        if (round(np.sum(probability), 6) != 1.0):
            raise Exception('Probability inside wheel selection incorrect!')

        idx1 = np.random.choice(np.arange(self.pop_size), size=NUMPAIRS, replace=True, p=probability)
        idx2 = np.random.choice(np.arange(self.pop_size), size=NUMPAIRS, replace=True, p=probability)

        if (PRINT == True):
            print('Wheel Selection')
            print('Probablitité:')
            print(probability)
            print('Liste d\'index 1')
            print(idx1)
            print('Liste d\'index 2')
            print(idx2)
            print('')

        return [self.population[idx1, :], self.population[idx2, :]]

    def doCrossover(self, pairs):
        # Input:
        # - PAIRS, a list of two ndarrays [IND1 IND2] each encoding one individu of the pair
        # - CROSSOVER_PROB, the crossover probability.
        # - CROSSOVER_POINT, a modulo-constraint on the cutting point. For example, to only allow cutting
        #   every 4 bits, set value to 4.
        # Output:
        # - POPULATION, a binary matrix with each row encoding an individual.
        crossover_point = int(self.nbits * self.num_params / 2)
        parents1 = pairs[0]
        parents2 = pairs[1]

        new_population = []
        for index in range(len(parents1)):
            if (PRINT == True):
                print('Crossover')
                print('Maman: ')
                print(parents1[index])
                print('Papa: ')
                print(parents2[index])

            if np.random.rand() < self.crossover_prob:
                if (PRINT == True):
                    print('Cossover : oui')
                child1 = np.concatenate((parents1[index][:crossover_point], parents2[index][crossover_point:]))
                new_population.append(child1)

                child2 = np.concatenate((parents2[index][:crossover_point], parents1[index][crossover_point:]))
                new_population.append(child2)
                if (PRINT == True):
                    print('Bébé1: ')
                    print(child1)
                    print('Bébé2: ')
                    print(child2)
            else:
                if (PRINT == True):
                    print('Cossover : non')
                new_population.append(parents1[index])
                new_population.append(parents2[index])

            if (PRINT == True):
                print('')

        return np.reshape(new_population, newshape=(self.pop_size, self.num_params * self.nbits))

    def doMutation(self):
        # Input:
        # - POPULATION, the binary matrix representing the population. Each row is an individual.
        # - MUTATION_PROB, the mutation probability.
        # Output:
        # - POPULATION, the new population.
        for index in range(len(self.population)):
            if np.random.rand() < self.mutation_prob:
                if (PRINT == True):
                    print('Mutation: oui')
                    print('Avant mutation:')
                    print(self.population[index])
                bit_to_mutate = np.random.randint(self.nbits * self.num_params)
                self.population[index][bit_to_mutate] ^= 1 # XOR

                if (PRINT == True):
                    print('Après mutation:')
                    print(self.population[index])
                    print('')

        return self.population


    def new_gen(self):
        pairs = self.doSelection()
        self.population = self.doCrossover(pairs)
        self.doMutation()
        self.current_gen += 1


# Binary-Float conversion functions
# usage: [BVALUE] = ufloat2bin(CVALUE, NBITS)
# Convert floating point values into a binary vector
# Input:
# - CVALUE, a scalar or vector of continuous values representing the parameters.
#   The values must be a real non-negative float in the interval [0,1]!
# - NBITS, the number of bits used for encoding.
# Output:
# - BVALUE, the binary representation of the continuous value. If CVALUES was a vector,
#   the output is a matrix whose rows correspond to the elements of CVALUES.
def ufloat2bin(cvalue, nbits):
    if nbits > 64:
        raise Exception('Maximum number of bits limited to 64')
    ivalue = np.round(cvalue * (2 ** nbits - 1)).astype(np.uint64)  # convertion en entier non signé
    bvalue = np.zeros((len(cvalue), nbits))

    # Overflow
    bvalue[ivalue > 2 ** nbits - 1] = np.ones((nbits,))

    # Underflow
    bvalue[ivalue < 0] = np.zeros((nbits,))

    bitmask = (2 ** np.arange(nbits)).astype(np.uint64)
    bvalue[np.logical_and(ivalue >= 0, ivalue <= 2 ** nbits - 1)] = (
                np.bitwise_and(np.tile(ivalue[:, np.newaxis], (1, nbits)),
                               np.tile(bitmask[np.newaxis, :], (len(cvalue), 1))) != 0)
    return bvalue


# usage: [CVALUE] = bin2ufloat(BVALUE, NBITS)
# Convert a binary vector into floating point values
# Input:
# - BVALUE, the binary representation of the continuous values. Can be a single vector or a matrix whose
#   rows represent independent encoded values.
#   The values must be a real non-negative float in the interval [0,1]!
# - NBITS, the number of bits used for encoding.
# Output:
# - CVALUE, a scalar or vector of continuous values representing the parameters.
#   the output is a matrix whose rows correspond to the elements of CVALUES.
def bin2ufloat(bvalue, nbits):
    if nbits > 64:
        raise Exception('Maximum number of bits limited to 64')
    ivalue = np.sum(bvalue * (2 ** np.arange(nbits)[np.newaxis, :]), axis=-1)
    cvalue = ivalue / (2 ** nbits - 1)
    return cvalue
