import gym
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import AIController as controller
from Player import *

def createFuzzyControllerObstacle():
    ant1 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle0')
    # ant2 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle1')
    ant3 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_mur0')
    # ant4 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_mur1')
    # ant5 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_mur2')

    ant6 = ctrl.Antecedent(np.linspace(0, 80, 1000), 'dist_obstacle0')
    # ant7 = ctrl.Antecedent(np.linspace(0, 1.5, 1000), 'dist_obstacle1')
    ant8 = ctrl.Antecedent(np.linspace(0, 80, 1000), 'dist_mur0')
    # ant9 = ctrl.Antecedent(np.linspace(0, 1.5, 1000), 'dist_mur1')
    # ant10 = ctrl.Antecedent(np.linspace(0, 1.5, 1000), 'dist_mur2')

    cons1 = ctrl.Consequent(np.linspace(-90, 90, 1000), 'output1', defuzzify_method='centroid')

    cons1.accumulation_method = np.fmax

    ant1['obsGauche'] = fuzz.trapmf(ant1.universe, [-71, -15, -1, 1])
    ant1['obsDroit'] = fuzz.trapmf(ant1.universe, [0, 1, 15, 71])
    ant1['obsGauche_completement'] = fuzz.trapmf(ant1.universe, [-90, -90, -80, -70])
    ant1['obsDroit_completement'] = fuzz.trapmf(ant1.universe, [70, 80, 90, 90])

    # ant2['obsGauche'] = fuzz.trapmf(ant2.universe, [-90, -25, 0, 0])
    # ant2['obsDroit'] = fuzz.trapmf(ant2.universe, [0, 0, 25, 90])

    ant3['murGauche'] = fuzz.trapmf(ant3.universe, [-71, -15, -1, 0])
    ant3['murDroit'] = fuzz.trapmf(ant3.universe, [0, 1, 15, 71])
    ant3['murGauche_completement'] = fuzz.trapmf(ant3.universe, [-90, -90, -80, -70])
    ant3['murDroit_completement'] = fuzz.trapmf(ant3.universe, [70, 80, 90, 90])

    # ant4['murGauche'] = fuzz.trapmf(ant4.universe, [-40, -25, 0, 0])
    # ant4['murDroit'] = fuzz.trapmf(ant4.universe, [0, 0, 25, 40])
    # ant4['murGauche_completement'] = fuzz.trapmf(ant4.universe, [-90, -90, -45, -20])
    # ant4['murDroit_completement'] = fuzz.trapmf(ant4.universe, [20, 45, 90, 90])

    # ant5['murGauche'] = fuzz.trapmf(ant5.universe, [-40, -25, 0, 0])
    # ant5['murDroit'] = fuzz.trapmf(ant5.universe, [0, 0, 25, 40])
    # ant5['murGauche_completement'] = fuzz.trapmf(ant5.universe, [-90, -90, -45, -20])
    # ant5['murDroit_completement'] = fuzz.trapmf(ant5.universe, [20, 45, 90, 90])

    ant6['obsProche'] = fuzz.trapmf(ant6.universe, [0, 0, 20, 35])
    ant6['obsLoin'] = fuzz.trapmf(ant6.universe, [45, 60, 80, 80])
    ant6['obsCentre'] = fuzz.trimf(ant6.universe, [30, 40, 50])

    # ant7['obsProche'] = fuzz.trapmf(ant7.universe, [0, 0, 0.4, 0.7])
    # ant7['obsLoin'] = fuzz.trapmf(ant7.universe, [0.6, 1, 1.5, 1.5])

    ant8['murProche'] = fuzz.trapmf(ant8.universe, [0, 0, 20, 35])
    ant8['murLoin'] = fuzz.trapmf(ant8.universe, [45, 60, 80, 80])
    ant8['murCentre'] = fuzz.trimf(ant8.universe, [30, 40, 50])

    # ant9['murProche'] = fuzz.trapmf(ant9.universe, [0, 0, 0.4, 0.7])
    # ant9['murLoin'] = fuzz.trapmf(ant9.universe, [0.6, 1, 1.5, 1.5])

    # ant10['murProche'] = fuzz.trapmf(ant10.universe, [0, 0, 0.4, 0.7])
    # ant10['murLoin'] = fuzz.trapmf(ant10.universe, [0.6, 1, 1.5, 1.5])

    cons1['tourneGauche'] = fuzz.trapmf(cons1.universe, [-90,-90, -60, -5])
    cons1['tourneDroit'] = fuzz.trapmf(cons1.universe, [5, 60, 90, 90])
    cons1['droit'] = fuzz.trimf(cons1.universe, [-15, 0, 15])


    # TODO: Define the rules.
    rules = []

    # 1 mur, 1 obstacle
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & (ant6['obsProche'] | ant6['obsCentre'])) & (ant3['murGauche'] & ant8['murProche'])), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & (ant6['obsProche'] | ant6['obsCentre'])) & (ant3['murDroit'] & ant8['murProche'])), consequent=cons1['tourneGauche']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & (ant6['obsProche'] | ant6['obsCentre'])) & (ant3['murGauche'] & ant8['murLoin'])), consequent=cons1['tourneGauche']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & (ant6['obsProche'] | ant6['obsCentre'])) & (ant3['murDroit'] & ant8['murLoin'])), consequent=cons1['tourneDroit']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & (ant6['obsProche'] | ant6['obsCentre'])) & (ant3['murGauche'] & ant8['murLoin'])), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & (ant6['obsProche'] | ant6['obsCentre'])) & (ant3['murDroit'] & ant8['murLoin'])), consequent=cons1['tourneGauche']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsLoin']) & (ant3['murGauche'] & (ant8['murProche'] | ant8['murCentre']))), consequent=cons1['tourneDroit'] % 0.5))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsLoin']) & (ant3['murDroit'] & (ant8['murProche'] | ant8['murCentre']))), consequent=cons1['tourneGauche'] % 0.5))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsLoin']) & (ant3['murDroit'] & (ant8['murProche'] | ant8['murCentre']))), consequent=cons1['tourneGauche']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsLoin']) & (ant3['murGauche'] & (ant8['murProche'] | ant8['murCentre']))), consequent=cons1['tourneDroit']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsLoin']) & (ant3['murGauche'] & ant8['murLoin'])), consequent=cons1['droit']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsLoin']) & (ant3['murDroit'] & ant8['murLoin'])), consequent=cons1['droit']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsLoin']) & (ant3['murDroit'] & ant8['murLoin'])), consequent=cons1['droit']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsLoin']) & (ant3['murGauche'] & ant8['murLoin'])), consequent=cons1['droit']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsProche']) & (ant3['murGauche'] & ant8['murProche'])), consequent=cons1['tourneGauche']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsProche']) & (ant3['murDroit'] & ant8['murProche'])), consequent=cons1['tourneDroit']))

    #centre
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsCentre']) & (ant3['murGauche'] & ant8['murCentre'])), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsCentre']) & (ant3['murDroit'] & ant8['murCentre'])), consequent=cons1['tourneGauche']))

    rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] & ant6['obsCentre']) & (ant3['murGauche'] & ant8['murCentre'])), consequent=cons1['droit']))
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] & ant6['obsCentre']) & (ant3['murDroit'] & ant8['murCentre'])), consequent=cons1['droit']))

    #completement
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche_completement'] | ant1['obsDroit_completement']) & (ant3['murGauche_completement'] | ant3['murDroit_completement'])), consequent=cons1['droit']))
   # rules.append(ctrl.Rule(antecedent=(ant3['murGauche_completement'] | ant3['murDroit_completement']) , consequent=cons1['droit']))
    
    rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] | ant1['obsDroit']) & (ant3['murGauche_completement'] | ant3['murDroit_completement'])), consequent=cons1['droit']))
    rules.append(ctrl.Rule(antecedent=((ant3['murGauche'] | ant3['murDroit']) & (ant1['obsGauche_completement'] | ant1['obsDroit_completement'])), consequent=cons1['droit']))


    rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] & ant3['murGauche_completement']), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] & ant3['murDroit_completement']), consequent=cons1['tourneGauche']))

    rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] & ant3['murDroit_completement']), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] & ant3['murGauche_completement']), consequent=cons1['tourneGauche']))

    rules.append(ctrl.Rule(antecedent=(ant3['murGauche'] & ant1['obsDroit_completement']), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=(ant3['murDroit'] & ant1['obsGauche_completement']), consequent=cons1['tourneGauche']))

    rules.append(ctrl.Rule(antecedent=(ant3['murGauche'] & ant1['obsGauche_completement']), consequent=cons1['tourneDroit']))
    rules.append(ctrl.Rule(antecedent=(ant3['murDroit'] & ant1['obsDroit_completement']), consequent=cons1['tourneGauche']))





    # # Obstacles
    # rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] | ant2['obsGauche']), consequent=cons1['tourneDroit']))
    # rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] | ant2['obsDroit']) , consequent=cons1['tourneGauche']))
    
    # rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] & ant2['obsDroit']), consequent=cons1['droit']))
    # rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] & ant2['obsGauche']), consequent=cons1['droit']))

    # # Murs
    # rules.append(ctrl.Rule(antecedent=(ant3['murGauche'] | ant4['murGauche'] | ant5['murGauche']), consequent=cons1['tourneDroit']))
    # rules.append(ctrl.Rule(antecedent=(ant3['murDroit'] | ant4['murDroit'] | ant5['murDroit']) , consequent=cons1['tourneGauche']))
    #rules.append(ctrl.Rule(antecedent=(ant3['murGauche_completement'] | ant3['murDroit_completement'] | ant4['murGauche_completement'] | ant4['murDroit_completement'] | ant5['murGauche_completement'] | ant5['murDroit_completement']) , consequent=cons1['droit']))
    
    # # Ajout de distances
    # rules.append(ctrl.Rule(antecedent=(ant3['murGauche'] & ant8['murProche']), consequent=cons1['tourneDroit'] % 1.5))
    # rules.append(ctrl.Rule(antecedent=(ant3['murDroit'] & ant8['murProche']), consequent=cons1['tourneGauche'] % 1.5))

    # rules.append(ctrl.Rule(antecedent=(ant4['murGauche'] & ant9['murProche']), consequent=cons1['tourneDroit'] % 1.5))
    # rules.append(ctrl.Rule(antecedent=(ant4['murDroit'] & ant9['murProche']), consequent=cons1['tourneGauche'] % 1.5))

    # rules.append(ctrl.Rule(antecedent=(ant5['murGauche'] & ant10['murProche']), consequent=cons1['tourneDroit'] % 1.5))
    # rules.append(ctrl.Rule(antecedent=(ant5['murDroit'] & ant10['murProche']), consequent=cons1['tourneGauche'] % 1.5))

    # rules.append(ctrl.Rule(antecedent=(ant3['murGauche'] & ant8['murLoin']), consequent=cons1['tourneGauche'] % 0.5))
    # rules.append(ctrl.Rule(antecedent=(ant3['murDroit'] & ant8['murLoin']), consequent=cons1['tourneDroit'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(ant4['murGauche'] & ant9['murLoin']), consequent=cons1['tourneGauche'] % 0.5))
    # rules.append(ctrl.Rule(antecedent=(ant4['murDroit'] & ant9['murLoin']), consequent=cons1['tourneDroit'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(ant5['murGauche'] & ant10['murLoin']), consequent=cons1['tourneGauche'] % 0.5))
    # rules.append(ctrl.Rule(antecedent=(ant5['murDroit'] & ant10['murLoin']), consequent=cons1['tourneDroit'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] & ant6['obsProche']), consequent=cons1['tourneDroit'] % 1.5))
    # rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] & ant6['obsProche']), consequent=cons1['tourneGauche'] % 1.5))

    # rules.append(ctrl.Rule(antecedent=(ant2['obsGauche'] & ant7['obsProche']), consequent=cons1['tourneDroit'] % 1.5))
    # rules.append(ctrl.Rule(antecedent=(ant2['obsDroit'] & ant7['obsProche']), consequent=cons1['tourneGauche'] % 1.5))

    # rules.append(ctrl.Rule(antecedent=(ant1['obsGauche'] & ant6['obsLoin']), consequent=cons1['tourneGauche'] % 0.5))
    # rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] & ant6['obsLoin']), consequent=cons1['tourneDroit'] % 0.5))

    # rules.append(ctrl.Rule(antecedent=(ant2['obsGauche'] & ant7['obsLoin']), consequent=cons1['tourneGauche'] % 0.5))
    # rules.append(ctrl.Rule(antecedent=(ant2['obsDroit'] & ant7['obsLoin']), consequent=cons1['tourneDroit'] % 0.5))

    # # Murs et obstacles
    # rules.append(ctrl.Rule(antecedent=(((ant3['murGauche'] & ant8['murLoin']) | (ant4['murGauche'] & ant9['murLoin']) | (ant5['murGauche'] & ant10['murLoin'])) & ant1['obsDroit']), consequent=cons1['droit']))
    # rules.append(ctrl.Rule(antecedent=(((ant3['murDroit'] & ant8['murLoin']) | (ant4['murDroit'] & ant9['murLoin']) | (ant5['murDroit'] & ant10['murLoin'])) & ant2['obsGauche']), consequent=cons1['droit']))

    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


class LogiqueFlou:
    def __init__(self):
        self.current_position=0
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
    

    def objects_distance(self, player, object):
        return np.sqrt((player[0] - object[0])**2 + (player[1] - object[1])**2)


    def step(self, liste_perception, player):
        angle_entre_perception = []
        distances = []
        for perception in liste_perception:
            distances.append(self.objects_distance(self.get_position_player(player), perception.center))
            angle_entre_perception.append(self.get_angle_between(self.get_position_player(player), perception))
        angles_relatifs = []
        distance_devant = []

        for angle in angle_entre_perception:
            if (self.angle_vision_joueur - angle) < 90 and (self.angle_vision_joueur - angle) > -90 :
                # print(f"angle relatif {self.angle_vision_joueur - angle}")
                distance_devant.append(distances[angle_entre_perception.index(angle)])
                angles_relatifs.append(self.angle_vision_joueur - angle)

        return angles_relatifs, distance_devant
    

    def associer_input_flou(self, max_range, list_input, input_name, default_value):
        print(f"input name {input_name} list input {list_input}")

        for i in range(max_range):
            if i < len(list_input):
                self.fuzz_ctrl.input[input_name+str(i)] = list_input[i]
            else:
                self.fuzz_ctrl.input[input_name+str(i)] = default_value

    
    def run(self, last_direction, player, perception):
        self.angle_vision_joueur = last_direction        
        wall_list, obstacle_list, item_list, monster_list, door_list = perception

        angles_relatifs, distances = self.step(obstacle_list, player)
        self.associer_input_flou(1, angles_relatifs, 'angle_obstacle', 90)
        self.associer_input_flou(1, distances, 'dist_obstacle', 80)

        print(f"nb murs {len(wall_list)}")
        angles_relatifs, distances = self.step(wall_list, player)
        self.associer_input_flou(1, angles_relatifs, 'angle_mur', 90)
        self.associer_input_flou(1, distances, 'dist_mur', 80)
        
        self.fuzz_ctrl.compute()
        direction = self.fuzz_ctrl.output['output1']

        has_obstacle = False
        if len(angles_relatifs) > 0:
            has_obstacle = True
        return direction, has_obstacle
    
    
def angle_between(p1, p2):
    angle_rad = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

    if angle_rad < 0:
        angle_rad += 2 * np.pi

    return np.rad2deg(angle_rad)
