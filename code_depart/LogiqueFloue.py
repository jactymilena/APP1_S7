import gym
import time
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
    #ant2 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input2')
    cons1 = ctrl.Consequent(np.linspace(-90, 90, 1000), 'output1', defuzzify_method='centroid')
    #cons2 = ctrl.Consequent(np.linspace(-1, 1, 1000), 'output2', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    cons1.accumulation_method = np.fmax

    # TODO: Create membership functions
    ant1['obsGauche'] = fuzz.trapmf(ant1.universe, [-90, -25, 0, 0])
    ant1['obsDroit'] = fuzz.trapmf(ant1.universe, [0, 1, 25, 90])
    #ant1['membership3'] = fuzz.trimf(ant1.universe, [-0.1, 0,0.1])

    #ant2['membership1'] = fuzz.trapmf(ant1.universe, [-1, -0.5, 0.5, 1])

    cons1['tourneGauche'] = fuzz.trimf(cons1.universe, [-90, -45, 0])
    cons1['tourneDroit'] = fuzz.trimf(cons1.universe, [0, 45, 90])


  #  cons2['membership1'] = fuzz.trimf(cons1.universe, [-1, 0, 1])

    # TODO: Define the rules.
    rules = []
    #rules.append(ctrl.Rule(antecedent=(ant1['angle_gauche'] & ant2['membership1']), consequent=cons1['membership1']))
    rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] ), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=(ant1['obsDroit']) , consequent=cons1['tourneGauche']))



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
    def __init__(self, maze):
        self.current_position=0
       # self.player = player
        self.angle_joueur = 0
        self.perception = []
        self.list_angle_vu_objet = []
        self.angle_vision_joueur = 0
        self.maze = maze
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
    
    def get_liste_perception(self, player):
        return self.maze.make_perception_list(player)
    
    def get_angle_between(self, pos_joueur, list_obstacle):
        list_angle = []
        for i in list_obstacle:
            list_angle.append(angle_between(pos_joueur, list_obstacle[i]))
        return list_angle    
    
    def step(self, listePerception, player):

        angle_entre_perception =[]
        for perception in listePerception:
            angle_entre_perception.append(self.get_angle_between(self.get_position_player(player), perception))
        angle_relatif_obstacle =[]

        for angle in angle_entre_perception:
            if (self.angle_vision_joueur - angle) < 90 & (self.angle_vision_joueur - angle) > -90 :
                angle_relatif_obstacle.append(self.angle_vision_joueur - angle)

        return angle_relatif_obstacle
    
    def associer_input_flou(self, range, list_input):
        for i in range(range):
            if i < len(list_input):
                self.fuzz_ctrl.input['angle_obstacle'+i] = list_input[i]
            else:
                self.fuzz_ctrl.input['angle_obstacle'+i] = -90

    
    def run(self, last_direction, player):
        self.angle_vision_joueur = last_direction        
        observation = self.get_liste_perception(player)
        wall_list, obstacle_list, item_list, monster_list, door_list = observation

        angle_obstacle_list = self.step(obstacle_list, player)
        self.associer_input_flou(2, angle_obstacle_list)
        
        
        self.fuzz_ctrl.compute()
        direction = self.fuzz_ctrl.output['output1']        
        return direction
        

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


