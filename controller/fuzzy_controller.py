from fuzzyinference import FuzzyControl
from math import pi

def get_controller(): 
    ctrl = FuzzyControl()
    theta_memberships = [
            ['trapezoid_left', -1.57 / 4, -0.58 / 4, 'vn'],
            ['triangle', -0.3927 / 4, 0.327 * 2.0 / 4.0, 'mn'],
            ['triangle', 0.0, 0.1745 * 2.0 / 4.0, 'z'],
            ['triangle', 0.3927 / 4, 0.327 * 2.0 / 4.0, 'mp'],
            ['trapezoid_right', 0.58 / 4, 1.57 / 4, 'vp']
    ]
    ctrl.add_input('theta', (-1 * pi / 2, pi / 2), theta_memberships)

    dtheta_memberships = [
        ['trapezoid_left', -1.57 / 4, -0.58 / 4, 'vn'],
        ['triangle', -0.3927 / 4, 2 * 0.327 / 4, 'mn'],
        ['triangle', 0.0, 2 * 0.1745 / 4, 'z'],
        ['triangle', 0.3927 / 4, 2 * 0.327 / 4, 'mp'],
        ['trapezoid_right', 0.58 / 4, 1.57 / 4, 'vp']
    ]
    ctrl.add_input('dtheta', (-1 * 100, 100), dtheta_memberships)

    force_memberships = [
            ['trapezoid_left', -0.99, -0.75, 'vn'],
            ['triangle', -0.6, 0.4, 'sn'],
            ['triangle', -0.3, 0.4, 'mn'],
            ['triangle', 0.0, 0.4, 'z'],
            ['triangle', 0.3, 0.4, 'mp'],
            ['triangle', 0.6, 0.4, 'sp'],
            ['trapezoid_right', 0.75, 0.99, 'vp']
    ]
    ctrl.add_output('force', (-1, 1), force_memberships)

    ctrl.add_rule({'theta': 'vn', 'dtheta': 'vn'}, {'force': 'vp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'mn'}, {'force': 'sp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'z'}, {'force': 'sp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'mp'}, {'force': 'mp'})
    ctrl.add_rule({'theta': 'vn', 'dtheta': 'vp'}, {'force': 'z'})

    ctrl.add_rule({'theta': 'vp', 'dtheta': 'vn'}, {'force': 'z'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'mn'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'z'}, {'force': 'sn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'mp'}, {'force': 'sn'})
    ctrl.add_rule({'theta': 'vp', 'dtheta': 'vp'}, {'force': 'vn'})

    ctrl.add_rule({'theta': 'mn', 'dtheta': 'vn'}, {'force': 'sp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'mn'}, {'force': 'sp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'z'}, {'force': 'mp'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'mp'}, {'force': 'z'})
    ctrl.add_rule({'theta': 'mn', 'dtheta': 'vp'}, {'force': 'mp'})

    ctrl.add_rule({'theta': 'z', 'dtheta': 'vn'}, {'force': 'sp'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'mn'}, {'force': 'mp'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'z'}, {'force': 'z'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'mp'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'z', 'dtheta': 'vp'}, {'force': 'sn'})

    ctrl.add_rule({'theta': 'mp', 'dtheta': 'vn'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'mn'}, {'force': 'z'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'z'}, {'force': 'mn'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'mp'}, {'force': 'sn'})
    ctrl.add_rule({'theta': 'mp', 'dtheta': 'vp'}, {'force': 'sn'})

    return ctrl
