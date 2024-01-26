import gym
import time
import math
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import AIController as controller
from Player import *

def createFuzzyControllerObstacle():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum
    ant1 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle0')
    ant2 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle1')

  #  ant3 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_mur0')

    cons1 = ctrl.Consequent(np.linspace(-90, 90, 1000), 'output1', defuzzify_method='centroid')
    
    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    cons1.accumulation_method = np.fmax

    # TODO: Create membership functions
    ant1['obsGauche'] = fuzz.trapmf(ant1.universe, [-50, -25, 0, 0])
    ant1['obsDroit'] = fuzz.trapmf(ant1.universe, [0, 1, 25, 50])
    ant1['obsGauche_completement'] = fuzz.trapmf(ant1.universe, [-90, -90, -60, -30])
    ant1['obsDroit_completement'] = fuzz.trapmf(ant1.universe, [30, 60, 90, 90])

    ant2['obsGauche'] = fuzz.trapmf(ant1.universe, [-90, -25, 0, 0])
    ant2['obsDroit'] = fuzz.trapmf(ant1.universe, [0, 1, 25, 90])

    cons1['tourneGauche'] = fuzz.trapmf(cons1.universe, [-90,-90, -60, -5])
    cons1['tourneDroit'] = fuzz.trapmf(cons1.universe, [5, 60, 90, 90])
    cons1['droit'] = fuzz.trimf(cons1.universe, [-15, 0, 15])


    # TODO: Define the rules.
    rules = []
    rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] | ant2['obsGauche']), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] | ant2['obsDroit']) , consequent=cons1['tourneGauche']))
    rules.append(ctrl.Rule(antecedent=(ant1['obsGauche_completement'] | ant1['obsDroit_completement']) , consequent=cons1['droit']))



    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    #     np.fmin
    #     np.fmax
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


class LogiqueFlou:
    def __init__(self):
        self.current_position=0
       # self.player = player
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
        current_position = player.get_position()
        return current_position
    
    def get_angle_between(self, pos_joueur, obstacle):
        # print(f"position joueur {pos_joueur} position obstacle {obstacle.center}")

        angle = angle_between(obstacle.center, pos_joueur)

        if obstacle.center[0] < pos_joueur[0]:
            angle += 180
        elif obstacle.center[0] > pos_joueur[0]:
            if obstacle.center[1] < pos_joueur[1]:
                angle += 360

        # print(f"angle entre joueur et obstacle {angle}")
        return angle
    
    def step(self, listePerception, player):
        angle_entre_perception =[]
        for perception in listePerception:
            angle_entre_perception.append(self.get_angle_between(self.get_position_player(player), perception))
        angle_relatif_obstacle =[]

        for angle in angle_entre_perception:
            if (self.angle_vision_joueur - angle) < 90 and (self.angle_vision_joueur - angle) > -90 :
                # print(f"angle relatif {self.angle_vision_joueur - angle}")
                angle_relatif_obstacle.append(self.angle_vision_joueur - angle)

        return angle_relatif_obstacle
    

    def associer_input_flou(self, max_range, list_input):
        for i in range(max_range):
            if i < len(list_input):
                self.fuzz_ctrl.input['angle_obstacle'+str(i)] = list_input[i]
            else:
                self.fuzz_ctrl.input['angle_obstacle'+str(i)] = -90

    
    def run(self, last_direction, player, perception):
        self.angle_vision_joueur = last_direction        
        wall_list, obstacle_list, item_list, monster_list, door_list = perception

        angle_obstacle_list = self.step(obstacle_list, player)
        self.associer_input_flou(2, angle_obstacle_list)
      #  self.associer_input_flou(3, self.step(wall_list, player))
        
        
        self.fuzz_ctrl.compute()
        direction = self.fuzz_ctrl.output['output1']        
        return direction
    
    
def angle_between(p1, p2):
    angle_rad = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

    if angle_rad < 0:
        angle_rad += 2 * np.pi

    return np.rad2deg(angle_rad)
