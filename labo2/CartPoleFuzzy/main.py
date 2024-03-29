# Université de Sherbrooke
# Code for Artificial Intelligence module
# Adapted by Audrey Corbeil Therrien, Simon Brodeur

# Source code
# Classic cart-pole system implemented by Rich Sutton et al.
# Copied from http://incompleteideas.net/sutton/book/code/pole.c
# permalink: https://perma.cc/C9ZM-652R

# NOTE : The print_state function of the FuzzyController needs
# to be updated with the latest version, available on github
# https://github.com/scikit-fuzzy/scikit-fuzzy/blob/master/skfuzzy/control/controlsystem.py
# Lines 514-572 from github replace lines 493-551 in the 0.4.2 2019 release

import gym
import time
from cartpole import *
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# inputs : force, vitesse chariot, position chariot, angle, vitesse du bout du pendule

def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum

    # inputs
    angle = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'angle')
    # cartVelocity = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'cartVelocity')
    # cartPosition = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'cartPosition')
    # outputs
    force = ctrl.Consequent(np.linspace(-1, 1, 1000), 'force', defuzzify_method='centroid')

    # ant1 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input1')
    # ant2 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'input2')
    # cons1 = ctrl.Consequent(np.linspace(-1, 1, 1000), 'output1', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    force.accumulation_method = np.fmax

    # TODO: Create membership functions
    # angle['membership1'] = fuzz.trapmf(angle.universe, [-1, -0.5, 0.5, 1])
    # cartVelocity['membership1'] = fuzz.trapmf(cartVelocity.universe, [-1, -0.5, 0.5, 1])
    # cartPosition['membership1'] = fuzz.trapmf(cartPosition.universe, [-1, -0.5, 0.5, 1])
    force['droite'] = fuzz.trimf(force.universe, [0, 0, 10])
    force['gauche'] = fuzz.trimf(force.universe, [-10, 0, 0])
    # force['droit'] = fuzz.trimf(force.universe, [0, 0, 0])

    # force['gauche'] = fuzz.trapmf(force.universe, [-10, -5, 0, 0])

    # angle['droite'] = fuzz.trimf(angle.universe, [0, 0, np.pi/2])
    # angle['gauche'] = fuzz.trimf(angle.universe, [-np.pi/2, 0, 0])
    # angle['droit'] = fuzz.trimf(angle.universe, [0, np.pi/2, np.pi])
    angle['gauche'] = fuzz.trapmf(angle.universe, [-1, -1, -0.5,0])
    angle['droit'] = fuzz.trimf(angle.universe, [-0.5, 0, 0.5])
    angle['droite'] = fuzz.trapmf(angle.universe, [0, 0.5, 1, 1])
    

    # TODO: Define the rules.
    rules = []
    rules.append(ctrl.Rule(antecedent=(angle['droite']), consequent=force['droite']))
    rules.append(ctrl.Rule(antecedent=(angle['gauche']), consequent=force['gauche']))
    # rules.append(ctrl.Rule(antecedent=(angle['droit']), consequent=force['droit']))


    # rules.append(ctrl.Rule(antecedent=(force['droit']), consequent=force['gauche']))
    # rules.append(ctrl.Rule(antecedent=(ant1['membership1'] & ant2['membership1']), consequent=cons1['membership1']))

    # Conjunction (and_func) and disjunction (or_func) methods for rules:
    #     np.fmin
    #     np.fmax
    for rule in rules:
        rule.and_func = np.fmin
        rule.or_func = np.fmax

    system = ctrl.ControlSystem(rules)
    sim = ctrl.ControlSystemSimulation(system)
    return sim


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create the environment and fuzzy controller
    env = CartPoleEnv("human")
    fuzz_ctrl = createFuzzyController()

    # Display rules
    print('------------------------ RULES ------------------------')
    for rule in fuzz_ctrl.ctrl.rules:
        print(rule)
    print('-------------------------------------------------------')

    # Display fuzzy variables
    for var in fuzz_ctrl.ctrl.fuzzy_variables:
        var.view()
    plt.show()

    VERBOSE = False

    for episode in range(100):
        print('Episode no.%d' % (episode))
        env.reset()

        isSuccess = True
        action = np.array([0.0], dtype=np.float32)
        for _ in range(100):
            env.render()
            time.sleep(0.01)

            # Execute the action
            observation, _, done, _ = env.step(action)
            if done:
                # End the episode
                isSuccess = False
                break

            # Select the next action based on the observation
            cartPosition, cartVelocity, poleAngle, poleVelocityAtTip = observation

            # TODO: set the input to the fuzzy system
            # fuzz_ctrl.input['input1'] = 0
            # fuzz_ctrl.input['input2'] = 0
            fuzz_ctrl.input['angle'] = poleAngle

            fuzz_ctrl.compute()
            if VERBOSE:
                fuzz_ctrl.print_state()

            # TODO: get the output from the fuzzy system
            # force = fuzz_ctrl.output['output1']
            force = fuzz_ctrl.output['force']

            action = np.array(force, dtype=np.float32).flatten()

    env.close()
