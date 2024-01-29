import gym
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import AIController as controller
from Player import *


def createFuzzyControllerObstacle():
    obs_angl = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle0')
    mur_angl = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_mur0')

    action = ctrl.Consequent(np.linspace(-90, 90, 1000), 'output1', defuzzify_method='centroid')

    action.accumulation_method = np.fmax

    for obj in [obs_angl, mur_angl]:
        obj['gauche'] = fuzz.trapmf(obs_angl.universe, [-71, -40, -25, -10])
        obj['droite'] = fuzz.trapmf(obs_angl.universe, [10, 25, 40, 71])
        obj['gauche_completement'] = fuzz.trapmf(obs_angl.universe, [-90, -90, -80, -38])
        obj['droite_completement'] = fuzz.trapmf(obs_angl.universe, [38, 80, 90, 90])
        obj['centre'] = fuzz.trimf(obs_angl.universe, [-32, 0, 32])

    action['gauche'] = fuzz.trapmf(action.universe, [-90, -90, -60, -5])
    action['droite'] = fuzz.trapmf(action.universe, [5, 60, 90, 90])
    action['tout_droit'] = fuzz.trimf(action.universe, [-20, 0, 20])

    rules = []

    # Obstacles
    rules.append(
        ctrl.Rule(antecedent=(obs_angl['gauche'] | mur_angl['gauche'] | obs_angl['centre'] | mur_angl['centre']),
                  consequent=action['droite']))

    rules.append(ctrl.Rule(antecedent=(obs_angl['droite'] | mur_angl['droite']), consequent=action['gauche']))

    rules.append(ctrl.Rule(antecedent=(obs_angl['droite_completement'] | obs_angl['gauche_completement']),
                           consequent=action['tout_droit']))
    rules.append(ctrl.Rule(antecedent=(mur_angl['droite_completement'] | mur_angl['gauche_completement']),
                           consequent=action['tout_droit']))
    
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
        for var in self.fuzz_ctrl.ctrl.fuzzy_variables:
           var.view()
        plt.show()

    def get_position_player(self, player):
        current_position = player.get_rect().center
        return current_position

    def associer_input_flou(self, max_range, list_input, input_name, default_value):
        # print(f"input name {input_name} list input {list_input}")
        test = f"--- {input_name} list input"

        if len(list_input) < max_range:
            raise Exception(f"La liste d'input {input_name} est trop petite, elle doit avoir au moins {max_range} valeurs") 

        for i in range(max_range):
            self.fuzz_ctrl.input[input_name + str(i)] = list_input[i]
            test += ' ' + str(list_input[i]) + ', '
            # if i < len(list_input):
                
            #     test += ' ' + str(list_input[i]) + ', '
            # else:
            #     self.fuzz_ctrl.input[input_name + str(i)] = default_value
            #     test += ' ' + str(default_value) + ', '

        print(test)
        

    def run(self, last_direction, last_a_star_direction, player, perception):
        self.angle_vision_joueur = last_direction
        wall_list, obstacle_list, item_list, monster_list, door_list = perception

        # self.fuzz_ctrl.input['next_direction'] = self.angle_vision_joueur - last_a_star_direction

        angles_relatifs = self.get_angles(obstacle_list, player, 'angle_obstacle')

        self.associer_input_flou(1, angles_relatifs, 'angle_obstacle', 90)

        angles_relatifs = self.get_angles(wall_list, player, 'angle_mur')
        self.associer_input_flou(1, angles_relatifs, 'angle_mur', 90)

        self.fuzz_ctrl.compute()
        direction = self.fuzz_ctrl.output['output1']

        has_obstacle = False
        if len(angles_relatifs) > 0:
            has_obstacle = True
        return direction, has_obstacle

    def get_angles(self, liste_perception, player, name):
        angle_entre_perception = []

        for perception in liste_perception:
            point1 = self.get_position_player(player)
            point2 = perception.center

            point1, point2 = self.convert_coordinates(point1, point2)

            angle_rad = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])
            angle_deg = np.degrees(angle_rad)

            if angle_deg < 0:
                angle_deg = angle_deg + 360

            # if name == 'angle_obstacle':
            #     print(angle_deg)

            angle_entre_perception.append(angle_deg)
            # angle_entre_perception.append(self.get_angle_between(self.get_position_player(player), perception, name))

        angles_relatifs = []
        for angle in angle_entre_perception:
            angle_relatif = self.angle_vision_joueur - angle
            if 90 > angle_relatif > -90:
                # if name == 'angle_obstacle':
                #     print(f"Angle vision: {self.angle_vision_joueur}")
                #     print(f"Angle relatif: {self.angle_vision_joueur - angle}")
                angles_relatifs.append(angle_relatif)
            else:
                if angle_relatif > 0:
                   angles_relatifs.append(90)
                elif angle_relatif < 0:
                    angles_relatifs.append(-90) 

        return angles_relatifs

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

    # def angle_between(self, p1, p2):
    #     angle_rad = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
    #     angle_deg = np.degrees(angle_rad)
    #     print(f"angle deg {angle_deg}")
    #
    #     if angle_deg < 0:
    #         angle_deg += 360
    #     print(f"angle deg apres {angle_deg}")
    #     return angle_deg
    #
    #
    # def get_angle_between(self, pos_joueur, obstacle, name):
    #     # print(f"position joueur {pos_joueur} position obstacle {obstacle.center}")
    #
    #     angle = self.angle_between(pos_joueur, obstacle.center)
    #     print(name)
    #     # print(f"angle entre joueur et {name} {angle}"	)
    #     # if obstacle.center[0] < pos_joueur[0]:
    #     #     angle += 180
    #     # elif obstacle.center[0] > pos_joueur[0]:
    #     #     if obstacle.center[1] < pos_joueur[1]:
    #     #         angle += 360
    #
    #     # print(f"angle entre joueur et obstacle {angle}")
    #     return angle
