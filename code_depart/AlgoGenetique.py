from Constants import *
import genetic

class AlgoGenetique:

    def Fight_Simulation(self, monster, player):
        simulation = genetic.Genetic()
        loser = True
        run = 0
        run_won = 0
        gen_higher_than_500 = 0

        for j in range(100):
            loser = True
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
                        run_won = run_won + 1
                        simulation.bestIndividual = individual

                        if i > 500:
                            gen_higher_than_500 = gen_higher_than_500 + 1

                if loser:
                    if (i > 300) and (simulation.bestIndividualFitness < 8):
                        print('ALGO ARRÊTÉ: Fitness trop poche')
                        break
                    simulation.fitness = fitness
                    simulation.eval_fit()

                    if i % 299 == 0:
                        simulation.print_progress()

                    simulation.new_gen()
                    simulation.decode_individuals()
                else:
                    print('Fitness of the winner:')
                    player.set_attributes(simulation.bestIndividual)
                    print(monster.mock_fight(player))
                    break

            #genetic.display_generations(simulation)
            print('Algo failed:')
            player.set_attributes(simulation.bestIndividual)
            print(monster.mock_fight(player))
            print('')
            #print('Nombre de run que ça a pris:')
            #print(run)

        print('FIN')
        print(f"Nombre de silumation réussi: {run_won}")
        print(f"Nombre de silumation réussi en haut de 500 génération: {gen_higher_than_500}")

        return simulation.bestIndividual
