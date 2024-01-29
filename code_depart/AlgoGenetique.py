from Constants import *
import genetic

class AlgoGenetique:

    def Fight_Simulation(self, monster, player):
        simulation = genetic.Genetic()
        loser = True
        run = 0

        while loser:
            run = run + 1
            print(f"RUN : {run}")

            simulation = genetic.Genetic()
            simulation.init_pop()

            for i in range(NUM_GENERATIONS):
                simulation.encode_individuals()

                fitness = []
                for individual in simulation.cvalues:
                    player.set_attributes(individual)
                    fitness_tuple = monster.mock_fight(player)

                    if fitness_tuple[0] > 1:
                        fitness.append(fitness_tuple[0] * fitness_tuple[1])
                    else:
                        fitness.append(fitness_tuple[1])

                    if fitness_tuple[0] == 4:
                        loser = False
                        simulation.bestIndividual = individual
                        # run_won = run_won + 1
                        # if i > 500:
                        #     gen_higher_than_500 = gen_higher_than_500 + 1

                if loser:
                    if (i > 300) and (simulation.bestIndividualFitness < 8):
                        print('ALGO ARRÊTÉ: Fitness trop poche')
                        break
                    simulation.fitness = fitness
                    simulation.eval_fit()

                    if i % 300 == 0:
                        simulation.print_progress()

                    simulation.new_gen()
                    simulation.decode_individuals()

            if loser:
                print('Algo failed : Fitness of the best individual:')
                player.set_attributes(simulation.bestIndividual)
                print(monster.mock_fight(player))
                print('')


        #genetic.display_generations(simulation)
        print('Fitness of the winner:')
        player.set_attributes(simulation.bestIndividual)
        print(monster.mock_fight(player))
        print('')
        print('Nombre de run que ça a pris:')
        print(run)
        print('FIN')

        return simulation.bestIndividual
