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
    ant1 = ctrl.Antecedent(np.linspace(0, 360, 1000), 'angle_obstacle')
    #ant2 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input2')
    cons1 = ctrl.Consequent(np.linspace(-180, 180, 1000), 'output1', defuzzify_method='centroid')
    cons2 = ctrl.Consequent(np.linspace(-1, 1, 1000), 'output2', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    cons1.accumulation_method = np.fmax

    # TODO: Create membership functions
    ant1['obsGauche'] = fuzz.trapmf(ant1.universe, [-3, -3, -1, 0])
    ant1['obsDroit'] = fuzz.trapmf(ant1.universe, [0, 1, 3, 3])
    #ant1['membership3'] = fuzz.trimf(ant1.universe, [-0.1, 0,0.1])

    #ant2['membership1'] = fuzz.trapmf(ant1.universe, [-1, -0.5, 0.5, 1])

    cons1['tourneGauche'] = fuzz.trimf(cons1.universe, [-90, -45, 0])
    cons1['tourneDroit'] = fuzz.trimf(cons1.universe, [0, 45, 90])
    
   # cons1['tourneUp'] = fuzz.trimf(cons1.universe, [140, 180, 230])
    #cons1['tourneDown'] = fuzz.trimf(cons1.universe, [-45, 0, 45])


    cons2['membership1'] = fuzz.trimf(cons1.universe, [-1, 0, 1])

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
    def __init__(self, player):
        self.current_position=0
        self.player = player
        self.angle_joueur = 0

        self.fuzzCtrl = createFuzzyControllerObstacle()

        # Display rules
        print('------------------------ RULES ------------------------')
        for rule in self.fuzz_ctrl.ctrl.rules:
            print(rule)
        print('-------------------------------------------------------')

        # Display fuzzy variables
        for var in self.fuzz_ctrl.ctrl.fuzzy_variables:
            var.view()
        plt.show()
        

        def get_position_player():
            current_position = self.player.get_position()
            return current_position
        
        def get_rel_distance_obstacle(liste):
            listeDistance = []
            for i in liste:
                listeDistance.append(i.center - get_position_player())
            return listeDistance
        
        def get_obstacle_proche(liste):
            listeObstacle = get_rel_distance_obstacle(liste)
            for i, y in listeObstacle:
                if i < 0 :
                    #i = i*-1
                    listeObstacle.remove(i)
            proche = min(listeObstacle)
            return proche
        
        def get_angle_obstacle(liste):
            return angle_between(get_position_player, get_obstacle_proche(liste))
            
        
        def run(self):
            
            self.fuzz_ctrl.input['angle_obstacle'] = get_angle_obstacle()
            self.fuzz_ctrl.compute()
            direction = self.fuzz_ctrl.output['output1']

            return direction
        

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


