import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def get_controller():
    # create variables
    resolution = [0.01, 0.01, 0.0001]
    theta = ctrl.Antecedent(np.arange(-1 * np.pi, np.pi, resolution[0]), 'theta')
    dtheta = ctrl.Antecedent(np.arange(-1 * np.pi, np.pi, resolution[1]), 'dtheta')
    force = ctrl.Consequent(np.arange(-1, 1, resolution[2]), 'force')
    theta['vn'] = fuzz.trapmf(theta.universe, [-4.12, -4.04, -1.57, -0.589])
    theta['mn'] = fuzz.trimf(theta.universe, [-0.7854, -0.3927, 0])
    theta['z'] = fuzz.trimf(theta.universe, [-0.1745, 0, 0.1745])
    theta['mp'] = fuzz.trimf(theta.universe, [0, 0.3927, 0.7854])
    theta['vp'] = fuzz.trapmf(theta.universe, [0.5973, 1.579, 4.048, 4.128])
    dtheta['vn'] = fuzz.trapmf(dtheta.universe, [-4.12, -4.04, -1.57, -0.589])
    dtheta['mn'] = fuzz.trimf(dtheta.universe, [-0.7854, -0.3927, 0])
    dtheta['z'] = fuzz.trimf(dtheta.universe, [-0.1745, 0, 0.1745])
    dtheta['mp'] = fuzz.trimf(dtheta.universe, [0, 0.3927, 0.7854])
    dtheta['vp'] = fuzz.trapmf(dtheta.universe, [0.5973, 1.579, 4.048, 4.128])
    force['vn'] = fuzz.trapmf(force.universe, [-1.311, -1.286, -0.5001, -0.1875])
    force['mn'] = fuzz.trimf(force.universe, [-0.25, -0.125, 0])
    force['z'] = fuzz.trimf(force.universe, [-0.0555, 0, 0.05555])
    force['mp'] = fuzz.trimf(force.universe, [0, 0.125, 0.25])
    force['vp'] = fuzz.trapmf(force.universe, [0.1901, 0.5025, 1.289, 1.314])
    rules = []
    rules.append(ctrl.Rule(theta['vn'], force['vp']))
    rules.append(ctrl.Rule(theta['vp'], force['vn']))
    rules.append(ctrl.Rule(theta['mn'] & (dtheta['vn'] | dtheta['mn']), force['vp']))
    rules.append(ctrl.Rule(theta['mn'] & (dtheta['z'] | dtheta['mp']), force['mp']))
    rules.append(ctrl.Rule(theta['mn'] & dtheta['vp'], force['z']))
    rules.append(ctrl.Rule(theta['z'] & dtheta['vn'], force['vp']))
    rules.append(ctrl.Rule(theta['z'] & dtheta['mn'], force['mp']))
    rules.append(ctrl.Rule(theta['z'] & dtheta['z'], force['z']))
    rules.append(ctrl.Rule(theta['z'] & dtheta['mp'], force['mn']))
    rules.append(ctrl.Rule((theta['z'] | theta['mp']) & dtheta['vp'], force['vn']))
    rules.append(ctrl.Rule(theta['mp'] & (dtheta['mn'] | dtheta['z']), force['mn']))
    rules.append(ctrl.Rule(theta['mp'] & dtheta['mp'], force['vn']))
    inverted_pendulum_ctrl = ctrl.ControlSystem(rules)
    baki = ctrl.ControlSystemSimulation(inverted_pendulum_ctrl)
    return baki


