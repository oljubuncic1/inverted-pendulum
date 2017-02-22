from fuzzyinference import FuzzyControl
from math import pi

def get_controller(): 
    ctrl = FuzzyControl()
    all_memberships = [
            ['trapezoid_left', -1.57, -0.58, 'vn'],
            ['triangle', -0.327, 2 * 0.327, 'mn'],
            ['triangle', 0.0, 2 * 0.1745, 'z'],
            ['triangle', 0.3927, 2 *0.3927, 'mp'],
            ['trapezoid_right', 0.59, 1.579, 'vp'],
            ]
    ctrl.add_input('theta', (-1 * pi/2, pi/2), all_memberships)
    ctrl.add_input('dtheta', (-1 * 100, 100), list(all_memberships))

    force_memberships = [
            ['trapezoid_left', -0.5, -0.1875, 'vn'],
            ['triangle', -0.125, 2 * 0.125, 'mn'],
            ['triangle', 0.0, 2 *0.0555, 'z'],
            ['triangle', 0.125, 2 *0.25, 'mp'],
            ['trapezoid_right', 0.19101, 0.5025, 'vp'],
            ]
    ctrl.add_output('force', (-1, 1), force_memberships)

    ctrl.add_rule({'theta': 'vn', 'dtheta': 'vn'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'mn'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'z'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'mp'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'vp'}, {'force': 'vp'})

    ctrl.add_rule({'theta': 'vp', 'dtheta': 'vn'}, {'force': 'vn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'mn'}, {'force': 'vn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'z'}, {'force': 'vn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'mp'}, {'force': 'vn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'vp'}, {'force': 'vn'})

    ctrl.add_rule({'theta': 'mn', 'dtheta': 'vn'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'mn'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'z'}, {'force': 'mp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'mp'}, {'force': 'mp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'vp'}, {'force': 'z'})

    ctrl.add_rule({'theta': 'z', 'dtheta': 'vn'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'mn'}, {'force': 'mp'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'z'}, {'force': 'z'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'mp'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'vp'}, {'force': 'vn'})

    ctrl.add_rule({'theta': 'mp', 'dtheta': 'vn'}, {'force': 'z'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'mn'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'z'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'mp'}, {'force': 'vn'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'vp'}, {'force': 'vn'})

    return ctrl
