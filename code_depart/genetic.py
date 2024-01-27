import matplotlib.pyplot as plt
from Constants import *
import numpy as np
PRINT = False


# Displays the progress of the fitness over all the generations
def display_generations(ga_sim):
    fig = plt.figure()
    n = np.arange(NUM_GENERATIONS)
    ax = fig.add_subplot(111)
    ax.plot(n, ga_sim.genBestFitness, '-r', label='Generation Max')
    ax.plot(n, ga_sim.FitnessRecord, '-b', label='Overall Max')
    ax.plot(n, ga_sim.genAvgFitness, '--k', label='Generation Average')
    ax.set_title('Fitness value over generations')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Fitness value')
    ax.legend()
    fig.tight_layout()
    plt.show()

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
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.bestIndividual = []
        self.bestIndividualFitness = -1e10
        self.genBestFitness = np.zeros((num_generations,))
        self.FitnessRecord = np.zeros((num_generations,))
        self.genAvgFitness = np.zeros((num_generations,))
        self.current_gen = 0

    def init_pop(self):
        self.cvalues = np.random.randint(-MAX_ATTRIBUTE, MAX_ATTRIBUTE, size=(self.pop_size, self.num_params))

    def encode_individuals(self):
        list_11bits = int_to_bin(self.cvalues.flatten(), NBITS)
        matrix_11bits = binary_list_to_matrix(list_11bits)

        row = int(self.pop_size)
        column = int(self.nbits * self.num_params)
        self.population = np.reshape(matrix_11bits, (row, column))

    def decode_individuals(self):
        row = int(self.pop_size * self.num_params)
        column = int(self.nbits)
        population_11bits = self.population.reshape((row, column))

        values_1D = bin_to_int(population_11bits)
        self.cvalues = np.reshape(values_1D, (self.pop_size, self.num_params))

    def eval_fit(self):
        if np.max(self.fitness) > self.bestIndividualFitness:
            self.bestIndividualFitness = np.max(self.fitness)
            self.bestIndividual = self.cvalues[self.fitness == np.max(self.fitness)][0]

        self.genBestFitness[self.current_gen] = np.max(self.fitness)
        self.FitnessRecord[self.current_gen] = self.bestIndividualFitness
        self.genAvgFitness[self.current_gen] = np.mean(self.fitness)

    def print_progress(self):
        print('Generation no.%d: best fitness is %f, average is %f' %
              (self.current_gen, self.genBestFitness[self.current_gen],
               self.genAvgFitness[self.current_gen]))
        print('Overall best fitness is %f' % self.bestIndividualFitness)
        print('')

    def doSelection(self):
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
        parents1 = pairs[0]
        parents2 = pairs[1]

        new_population = []
        for index in range(len(parents1)):
            if np.random.rand() < self.crossover_prob:
                child1 = np.concatenate((parents1[index][:CROSSOVER_POINT], parents2[index][CROSSOVER_POINT:]))
                new_population.append(child1)

                child2 = np.concatenate((parents2[index][:CROSSOVER_POINT], parents1[index][CROSSOVER_POINT:]))
                new_population.append(child2)

            else:
                new_population.append(parents1[index])
                new_population.append(parents2[index])

        return np.reshape(new_population, newshape=(self.pop_size, self.num_params * self.nbits))

    def doMutation(self):
        for index in range(len(self.population)):
            if True: #np.random.rand() < self.mutation_prob:
                # todo: 2000
                bit_to_mutate = np.random.randint(self.nbits * self.num_params)
                self.population[index][bit_to_mutate] ^= 1  # XOR

        return self.population

    def new_gen(self):
        pairs = self.doSelection()
        self.population = self.doCrossover(pairs)
        self.doMutation()
        self.current_gen += 1

def int_to_bin(int_list, nbits):
    int_list = int_list + 1000
    bin_list = []

    for value in int_list:
        bin_list.append(bin(value)[2:].zfill(nbits))

    return bin_list

def bin_to_int(binary_matrix):
    ivalue = []
    for row in binary_matrix:
        ivalue.append(int("".join(str(x) for x in row), 2) - 1000)

    return ivalue

def binary_list_to_matrix(list):
    row = POPULATION_SIZE*NUM_ATTRIBUTES
    column = NBITS

    matrix = [[0] * column for _ in range(row)]

    for i in range(row):
        for j in range(column):
            matrix[i][j] = int(list[i][j])

    return matrix