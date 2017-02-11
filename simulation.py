from math import sin, cos

def simulate(state, force):
	x, x_dot, theta, theta_dot = state[0], state[1], state[2], state[3]

	# constants
	GRAVITY=9.8
	MASSCART=1.0
	MASSPOLE=0.1
	TOTAL_MASS = MASSPOLE + MASSCART
	LENGTH = 0.5
	POLEMASS_LENGTH = MASSPOLE * LENGTH
	STEP = 0.02
	FOURTHIRDS = 1.3333333333333

	costheta = cos(theta)
	sintheta = sin(theta)

	# mathhhh
	temp = (force + POLEMASS_LENGTH * theta_dot  *theta_dot * sintheta)/ TOTAL_MASS

	thetaacc = (GRAVITY * sintheta - costheta* temp)/(LENGTH * (FOURTHIRDS - MASSPOLE * costheta * costheta/ TOTAL_MASS))

	xacc  = temp - POLEMASS_LENGTH * thetaacc* costheta / TOTAL_MASS

	next_state = [x + STEP * x_dot, x_dot + STEP *xacc, theta + STEP * theta_dot, theta_dot + STEP * thetaacc]

	return next_state
