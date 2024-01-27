from Constants import *
import Genetic

class AlgoGenetique:

    def Fight_Simulation(self, monster, player):
        simulation = Genetic.Genetic()
        loser = True
        run = 0

        while loser:
            run = run + 1

            simulation = Genetic.Genetic()
            simulation.init_pop()

            for i in range(NUM_GENERATIONS):
                simulation.encode_individuals()

                fitness = []
                for individual in simulation.cvalues:
                    player.set_attributes(individual)
                    fitness_tuple = monster.mock_fight(player)

                    # if fitness_tuple[0] > 1:
                    fitness.append(fitness_tuple[0] + fitness_tuple[1])
                    # else:
                    #    fitness.append(fitness_tuple[1])

                    if fitness_tuple[0] == 4:
                        loser = False
                        simulation.bestIndividual = individual

                if loser:
                    if (i > 300) and (simulation.bestIndividualFitness < 8):
                        break
                    simulation.fitness = fitness
                    simulation.eval_fit()

                    if (i % 10 == 0):
                        simulation.print_progress()

                    simulation.new_gen()
                    simulation.decode_individuals()
                else:
                    break

        Genetic.display_generations(simulation)
        print('FIGHHHHHHHHHHHHHHHHHHHHHHT')
        player.set_attributes(simulation.bestIndividual)
        print(monster.mock_fight(player))
        print('Nombre de run que ça a pris:')
        print(run)

        return simulation.bestIndividual
