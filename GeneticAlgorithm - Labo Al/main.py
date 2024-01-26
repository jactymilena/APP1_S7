# Université de Sherbrooke
# Code for Artificial Intelligence module
# Adapted by Audrey Corbeil Therrien for Artificial Intelligence module

import genetic
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PRINT = False

def fitness_function(x, y):
    # The 2-dimensional function to optimize
    fitness = (1 - x) ** 2 * np.exp(-x ** 2 - (y + 1) ** 2) - \
              (x - x ** 3 - y ** 5) * np.exp(-x ** 2 - y ** 2)
    return fitness


# Produces the 3D surface plot of the fitness function
def init_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Function landscape')
    xymin = -3.0
    xymax = 3.0
    x, y = np.meshgrid(np.linspace(xymin, xymax, 100),
                       np.linspace(xymin, xymax, 100))
    z = fitness_function(x, y)

    ax.plot_surface(x, y, z, cmap=plt.get_cmap('coolwarm'),
                    linewidth=0, antialiased=False)

    e = np.zeros((popsize,))
    sp, = ax.plot(e, e, e, markersize=10, color='k', marker='.', linewidth=0, zorder=10)

    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(-1, 4)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    fig.show()
    return fig, sp

# Displays the progress of the fitness over all the generations
def display_generations(ga_sim):
    fig = plt.figure()
    n = np.arange(numGenerations)
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

def display_population(ga_sim):
    if (PRINT == True):
        print('POPULATION #%d' % ga_sim.current_gen)
        for individual in ga_sim.population:
            print(individual)
        print('')

if __name__ == '__main__':
    # nombres aléatoires seront les mêmes à chaque exécution du programme
    np.random.seed(0)

    # Enables realtime plotting of landscape and population.
    # Disabling plotting is much faster!
    SHOW_LANDSCAPE = True

    # The parameters for encoding the population
    numparams = 2
    popsize = 50
    nbits = 16
    ga_sim = genetic.Genetic(numparams, popsize, nbits)
    ga_sim.init_pop()
    display_population(ga_sim)
    ga_sim.set_fit_fun(fitness_function)

    if SHOW_LANDSCAPE:
        fig, sp = init_plot()

    numGenerations = 30
    mutationProb = 0.08
    crossoverProb = 0.8
    ga_sim.set_sim_parameters(numGenerations, mutationProb, crossoverProb)

    for i in range(ga_sim.num_generations):
        if (ga_sim.num_generations > 15):
            ga_sim.set_sim_parameters(numGenerations, 0.2, crossoverProb)

        if (ga_sim.num_generations > 20):
            ga_sim.set_sim_parameters(numGenerations, mutationProb, crossoverProb)

        ga_sim.decode_individuals()
        ga_sim.eval_fit()
        ga_sim.print_progress()

        if SHOW_LANDSCAPE:
            sp.set_data(ga_sim.cvalues[:, 0], ga_sim.cvalues[:, 1])
            sp.set_3d_properties(ga_sim.fitness)
            fig.canvas.draw()
            plt.pause(0.02)

        ga_sim.new_gen()
        display_population(ga_sim)

    # Display best individual
    print('#########################')
    print('Best individual (encoded values):')
    ga_sim.print_best_individual()
    print('#########################')

    display_generations(ga_sim)
