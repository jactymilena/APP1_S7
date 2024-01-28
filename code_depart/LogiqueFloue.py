import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np


def createFuzzyControllerObstacle():
    #ant1 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_obstacle')
    ant1 = ctrl.Antecedent(np.linspace(-180, 180, 1000), 'angle_obstacle')
    #ant2 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_wall1')
    #ant3 = ctrl.Antecedent(np.linspace(-90, 90, 1000), 'angle_wall2')

    cons1 = ctrl.Consequent(np.linspace(-90, 90, 1000), 'direction', defuzzify_method='centroid')
    cons1.accumulation_method = np.fmax

    trapeze_left = [-75, -50, -30, 0]
    trapeze_right = [0, 30, 50, 75]
    #ant1['obstacle_left'] = fuzz.trapmf(ant1.universe, abcd=trapeze_left)
    #ant1['obstacle_right'] = fuzz.trapmf(ant1.universe, abcd=trapeze_right)
    ant1['obstacle_left'] = fuzz.trapmf(ant1.universe, abcd=trapeze_left)
    ant1['obstacle_right'] = fuzz.trapmf(ant1.universe, abcd=trapeze_right)
    ant1['other1'] = fuzz.trapmf(ant1.universe, [-180, -180, -75, -75])
    ant1['other2'] = fuzz.trapmf(ant1.universe, [75, 75, 180, 180])

    #ant2['wall_left'] = fuzz.trapmf(ant3.universe, abcd=trapeze_left)
    #ant2['wall_right'] = fuzz.trapmf(ant3.universe, abcd=trapeze_right)

    #ant3['wall_left'] = fuzz.trapmf(ant3.universe, abcd=trapeze_left)
    #ant3['wall_right'] = fuzz.trapmf(ant3.universe, abcd=trapeze_right)

    cons1['go_left'] = fuzz.trapmf(cons1.universe, [-85, -85, -30, 0])
    cons1['go_right'] = fuzz.trapmf(cons1.universe, [0, 30, 85, 85])
    cons1['go_straight'] = fuzz.trimf(cons1.universe, [-20, 0, 20])

    rules = []

    # todo: il faudrait avoir une entrée pour tous les murs qui pourraient potentiellement être dans notre champ de vision
    # todo: question, heuuu jcomprends pas la perception
    rules.append(ctrl.Rule(antecedent=(ant1['obstacle_left']), consequent=cons1['go_right']))
    rules.append(ctrl.Rule(antecedent=(ant1['obstacle_right']), consequent=cons1['go_left']))
    rules.append(ctrl.Rule(antecedent=((ant1['other1']) | (ant1['other2'])), consequent=cons1['go_straight']))


    # rules.append(ctrl.Rule(antecedent=(ant1['obstacle_left'] | ant1['obsGauche_completement']) | (ant3['murGauche'] | ant3['murGauche_completement']), consequent=cons1['tourneDroit']))
    # rules.append(ctrl.Rule(antecedent=(ant1['obsDroit'] | ant1['obsDroit_completement']) | (ant3['murDroit'] | ant3['murDroit_completement']), consequent=cons1['tourneGauche']))
    #
    # rules.append(ctrl.Rule(antecedent=((ant1['obsGauche'] | ant1['obsGauche_completement']) & (ant3['murDroit'] | ant3['murDroit_completement'])), consequent=cons1['droit']))
    # rules.append(ctrl.Rule(antecedent=((ant1['obsDroit'] | ant1['obsDroit_completement']) & (ant3['murGauche'] | ant3['murGauche_completement'])), consequent=cons1['droit']))
    #
    # rules.append(ctrl.Rule(antecedent=(ant1['obsGauche_completement'] | ant1['obsDroit_completement'] | ant3['murGauche_completement'] | ant3['murDroit_completement'] ), consequent=cons1['droit']))
    #
    # rules.append(ctrl.Rule(antecedent=((ant1['obsGauche_completement']) & (ant3['murDroit'])), consequent=cons1['tourneGauche']))
    # rules.append(ctrl.Rule(antecedent=((ant1['obsDroit_completement']) & (ant3['murGauche'])), consequent=cons1['tourneDroit']))


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
        #for var in self.fuzz_ctrl.ctrl.fuzzy_variables:
            #var.view()
        #plt.show()
        

    def get_position_player(self, player):
        current_position = player.get_position()
        return current_position
    
    def get_angle_between(self, pos_joueur, obstacle):
        angle = angle_between(obstacle.center, pos_joueur)

        if obstacle.center[0] < pos_joueur[0]:
            angle += 180
        elif obstacle.center[0] > pos_joueur[0]:
            if obstacle.center[1] < pos_joueur[1]:
                angle += 360

        #print(f"angle entre joueur et obstacle {angle}")
        return angle
    

    def objects_distance(self, player, object):
        return np.sqrt((player[0] - object[0])**2 + (player[1] - object[1])**2)


    def step(self, liste_perception, player):
        angle_entre_perception = []
        for perception in liste_perception:
            angle_entre_perception.append(self.get_angle_between(self.get_position_player(player), perception))

        angles_relatifs = []
        for angle in angle_entre_perception:
            if 90 > (self.angle_vision_joueur - angle) > -90:
                # print(f"angle relatif {self.angle_vision_joueur - angle}")
                angles_relatifs.append(self.angle_vision_joueur - angle)

        return angles_relatifs
    

    def associer_input_flou(self, max_range, list_input, input_name, default_value):
        #print(f"input name {input_name} list input {list_input}")

        for i in range(max_range):
            if i < len(list_input):
                #self.fuzz_ctrl.input[input_name+str(i)] = list_input[i]
                self.fuzz_ctrl.input[input_name] = list_input[i]
            else:
                #self.fuzz_ctrl.input[input_name+str(i)] = default_value
                self.fuzz_ctrl.input[input_name] = default_value

    
    def run(self, last_direction, player, perception):
        self.angle_vision_joueur = last_direction        
        wall_list, obstacle_list, item_list, monster_list, door_list = perception

        angles_relatifs = self.step(obstacle_list, player)

        #print('Angle relatifs entre la liste d\'objets perçue et le joueur')
        #print(angles_relatifs)
            #print('')

        self.associer_input_flou(1, angles_relatifs, 'angle_obstacle', 90)

        #print(f"nb murs {len(wall_list)}")
        #angles_relatifs = self.step(wall_list, player)
        #self.associer_input_flou(1, angles_relatifs, 'angle_wall1', 90)
        
        self.fuzz_ctrl.compute()
        direction = self.fuzz_ctrl.output['direction']

        has_obstacle = False
        if len(angles_relatifs) > 0:
            has_obstacle = True
        return direction, has_obstacle
    
    
def angle_between(p1, p2):
    angle_rad = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])

    if angle_rad < 0:
        angle_rad += 2 * np.pi

    print('Angle pure et dure entre obj et joueur')
    print(np.rad2deg(angle_rad))
    print('')

    return np.rad2deg(angle_rad)
