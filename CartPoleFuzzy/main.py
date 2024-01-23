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


def createFuzzyController():
    # TODO: Create the fuzzy variables for inputs and outputs.
    # Defuzzification (defuzzify_method) methods for fuzzy variables:
    #    'centroid': Centroid of area
    #    'bisector': bisector of area
    #    'mom'     : mean of maximum
    #    'som'     : min of maximum
    #    'lom'     : max of maximum
    ant1 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'angle_pole')
    ant2 = ctrl.Antecedent(np.linspace(-1, 1, 1000), 'vit_pole')
    cons1 = ctrl.Consequent(np.linspace(-10, 10, 1000), 'output1', defuzzify_method='centroid')

    # Accumulation (accumulation_method) methods for fuzzy variables:
    #    np.fmax
    #    np.multiply
    cons1.accumulation_method = np.fmax

    # TODO: Create membership functions
    ant1['angle_gauche'] = fuzz.trapmf(ant1.universe, [-1, -0.9, -0.25, 0])
    ant1['angle_droit'] = fuzz.trapmf(ant1.universe, [0, 0.25, 0.9, 1])
    ant1['droit'] = fuzz.trimf(ant1.universe, [-0.1, 0,0.1])

    ant2['ralenti'] = fuzz.trapmf(ant1.universe, [-1, -0.5, 0.5, 1])

    cons1['ForceDroite'] = fuzz.trimf(cons1.universe, [0, 1, 10])
    cons1['ForceGauche'] = fuzz.trimf(cons1.universe, [-10, -1, 0])

    # TODO: Define the rules.
    rules = []
    #rules.append(ctrl.Rule(antecedent=(ant1['angle_gauche'] & ant2['membership1']), consequent=cons1['membership1']))
    rules.append(ctrl.Rule(antecedent=(ant1['angle_droit'] ), consequent=cons1['ForceDroite']))
    rules.append(ctrl.Rule(antecedent=(ant1['angle_gauche']) , consequent=cons1['ForceGauche']))
    rules.append(ctrl.Rule(antecedent=(ant1['droit'] & ant2['ralenti']), consequent=cons1['ForceDroite']%0.1))
    rules.append(ctrl.Rule(antecedent=(ant1['droit'] & ant2['ralenti']), consequent=cons1['ForceGauche']%0.1))



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

    for episode in range(10):
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
            fuzz_ctrl.input['angle_pole'] = poleAngle
            fuzz_ctrl.input['vit_pole'] = poleVelocityAtTip

            fuzz_ctrl.compute()
            if VERBOSE:
                fuzz_ctrl.print_state()

            # TODO: get the output from the fuzzy system
            force = fuzz_ctrl.output['output1']

            action = np.array(force, dtype=np.float32).flatten()

    env.close()
