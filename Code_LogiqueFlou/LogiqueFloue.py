import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
from Player import *


def createFuzzyControllerObstacle():
    obs_angl = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle0')
    mur_angl = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_mur0')
    obs_dist = ctrl.Antecedent(np.linspace(0, 80, 1000), 'distance_obstacle0')
    mur_dist = ctrl.Antecedent(np.linspace(0, 80, 1000), 'distance_mur0')

    action = ctrl.Consequent(np.linspace(-90, 90, 1000), 'output1', defuzzify_method='centroid')

    action.accumulation_method = np.fmax

    for obj in [obs_angl, mur_angl]:
        obj['gauche'] = fuzz.trapmf(obj.universe, [-71, -40, -25, 0])
        obj['droite'] = fuzz.trapmf(obj.universe, [0, 25, 40, 71])
        obj['gauche_completement'] = fuzz.trapmf(obj.universe, [-90, -90, -80, -38])
        obj['droite_completement'] = fuzz.trapmf(obj.universe, [38, 80, 90, 90])
        obj['centre'] = fuzz.trimf(obj.universe, [-32, 0, 32])

    obs_dist['proche'] = fuzz.trapmf(obs_dist.universe, [0, 0, 35, 45])
    obs_dist['loin'] = fuzz.trapmf(obs_dist.universe, [35, 45, 80, 80])

    mur_dist['proche'] = fuzz.trapmf(mur_dist.universe, [0, 0, 35, 50])
    mur_dist['loin'] = fuzz.trapmf(mur_dist.universe, [35, 50, 80, 80])
    # for obj in [obs_dist, mur_dist]:
    #     obj['proche'] = fuzz.trapmf(obj.universe, [0, 0, 35, 45])
    #     obj['loin'] = fuzz.trapmf(obj.universe, [35, 45, 80, 80])

    action['gauche'] = fuzz.trapmf(action.universe, [-90, -90, -60, 0])
    action['droite'] = fuzz.trapmf(action.universe, [0, 60, 90, 90])
    action['tout_droit'] = fuzz.trimf(action.universe, [-40, 0, 40])

    rules = []

    # Obstacles
    rules.append(ctrl.Rule(antecedent=(obs_angl['droite'] | mur_angl['droite'] | obs_angl['centre'] | mur_angl['centre']),
                  consequent=action['gauche']))

    #rules.append(ctrl.Rule(antecedent=(obs_dist['proche']),
    #              consequent=action['droite']))

    rules.append(ctrl.Rule(antecedent=(obs_angl['gauche'] | mur_angl['gauche']),
                           consequent=action['droite']))

    rules.append(ctrl.Rule(antecedent=((obs_angl['droite_completement'] | obs_angl['gauche_completement']) & obs_dist['loin']),
                  consequent=action['tout_droit']))

    rules.append(ctrl.Rule(antecedent=((mur_angl['droite_completement'] | mur_angl['gauche_completement']) & mur_dist['loin']),
                  consequent=action['tout_droit']))

    # rules.append(ctrl.Rule(antecedent=(mur_dist['loin'] | obs_dist['loin']), consequent=action['tout_droit']))

    # rules.append(ctrl.Rule(antecedent=(obs_angl['gauche'] & mur_angl['droite']), consequent=action['droite']))
    # rules.append(ctrl.Rule(antecedent=(obs_angl['droite'] & mur_angl['gauche']), consequent=action['gauche']))

    # rules.append(ctrl.Rule(antecedent=(mur_angl['gauche']), consequent=cons1['tourneDroite']))
    # rules.append(ctrl.Rule(antecedent=(obs_angl['gauche'] & mur_angl['gauche']), consequent=cons1['tourneDroite'] % 1.3))

    # rules.append(ctrl.Rule(antecedent=(obs_angl['gauche'] & mur_angl['droite']), consequent=cons1['tourneDroite'] % 0.5))
    # rules.append(ctrl.Rule(antecedent=(obs_angl['droite'] & mur_angl['gauche']), consequent=cons1['tourneGauche'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(mur_angl['droite']), consequent=cons1['tourneGauche']))
    # rules.append(ctrl.Rule(antecedent=(obs_angl['droite'] & mur_angl['droite']), consequent=cons1['tourneGauche'] % 1.3))

    # rules.append(ctrl.Rule(antecedent=(mur_angl['droite_completement']), consequent=cons1['tourneGauche'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(obs_angl['gauche_completement']), consequent=cons1['tourneDroite'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(obs_angl['droite_completement'] & mur_angl['gauche_completement']), consequent=cons1['droit']))
    # rules.append(ctrl.Rule(antecedent=(obs_angl['gauche_completement'] & mur_angl['droite_completement']), consequent=cons1['droit']))

    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


class LogiqueFlou:
    def __init__(self):
        self.current_position = 0
        self.angle_joueur = 0
        self.perception = []
        self.list_angle_vu_objet = []
        self.angle_vision_joueur = 0
        self.input_obstacle = []
        self.input_mur = []
        self.input_item = []

        self.fuzz_ctrl = createFuzzyControllerObstacle()

        # Display rules
        print('------------------------ RULES ------------------------')
        for rule in self.fuzz_ctrl.ctrl.rules:
            print(rule)
        print('-------------------------------------------------------')

        # Display fuzzy variables
        # for var in self.fuzz_ctrl.ctrl.fuzzy_variables:
        #     var.view()
        # plt.show()

    def get_position_player(self, player):
        current_position = player.get_rect().center
        return current_position

    def associer_input_flou(self, max_range, list_input, input_name):

        if len(list_input) < max_range:
            angle = 90
            distance = 80

            for i in range(max_range - len(list_input)):
                list_input.append((angle, distance))


        for i in range(max_range):
            self.fuzz_ctrl.input['angle_' + input_name + str(i)] = list_input[i][0]
            self.fuzz_ctrl.input['distance_' + input_name + str(i)] = list_input[i][1]

            print(f"-- Distance de/du {input_name} : {list_input[i][1]}")
            print(f"-- Angle de/du {input_name} : {list_input[i][0]}")



    def run(self, last_direction, last_a_star_direction, player, perception):
        self.angle_vision_joueur = last_direction
        wall_list, obstacle_list, item_list, monster_list, door_list = perception

        # self.fuzz_ctrl.input['next_direction'] = self.angle_vision_joueur - last_a_star_direction

        variables = self.get_variables(obstacle_list, player, 'obstacle')
        self.associer_input_flou(1, variables, 'obstacle')

        variables = self.get_variables(wall_list, player, 'mur')
        self.associer_input_flou(1, variables, 'mur')
        print('')

        self.fuzz_ctrl.compute()
        self.fuzz_ctrl.print_state()
        direction = self.fuzz_ctrl.output['output1']
        print(f"Direction Logique Flou : {direction}")

        has_obstacle = False
        if len(variables) > 0:
            has_obstacle = True
        return direction, has_obstacle

    def get_distance(self, p1, p2):
        #print(f"point 1: {p1}, point 2: {p2}")
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def get_variables(self, liste_perception, player, name):
        variables = []

        for perception in liste_perception:
            point1 = self.get_position_player(player)
            point2 = perception.center

            point1, point2 = self.convert_coordinates(point1, point2)

            angle_rad = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
            angle_deg = np.degrees(angle_rad)

            if angle_deg < 0:
                angle_deg = angle_deg + 360

            #print(f"Angle absolue: {angle_deg}")

            distance = self.get_distance(point1, point2)

            variables.append((angle_deg, distance))

        variables_finales = []

        for i in range(len(variables)):
            angle_relatif = self.angle_vision_joueur - variables[i][0]
            #print(f"Angle de vision: {self.angle_vision_joueur}")
            #print(f"Angle relatif: {angle_relatif}\n")

            if 90 > angle_relatif > -90:
                variables_finales.append((angle_relatif, variables[i][1]))
                # print(f"-- Distance de/du {name} : {variables[i][1]}")
                # print(f"-- Angle de/du {name} : {angle_relatif}")

            # else:
            #     if angle_relatif > 0:
            #         variables_finales.append((90, variables[i][1]))
            #         print(f"-- Distance de/du {name} : {variables[i][1]}")
            #         print(f"-- Angle (par défaut) de/du {name} : 90")
            #     elif angle_relatif < 0:
            #         variables_finales.append((-90, variables[i][1]))
            #         print(f"-- Distance de/du {name} : {variables[i][1]}")
            #         print(f"-- Angle (par défaut) de/du {name} : -90")

        return variables_finales

    def convert_coordinates(self, p1, p2):
        # changement de système de coordonné
        # on veut le point (0, 0) en bas à gauche
        p1_x, p1_y = p1
        p2_x, p2_y = p2

        p1_y = HEIGHT - p1_y
        p2_y = HEIGHT - p2_y

        p1_converted = (p1_x, p1_y)
        p2_converted = (p2_x, p2_y)

        return p1_converted, p2_converted
