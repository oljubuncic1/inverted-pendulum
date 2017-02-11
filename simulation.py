from math import sin, cos
import qlearning

def simulate_step(state, force, dt):
	x, x_dot, theta, theta_dot = state[0], state[1], state[2], state[3]

	# constants
	GRAVITY=9.8
	MASSCART=1.0
	MASSPOLE=0.1
	TOTAL_MASS = MASSPOLE + MASSCART
	LENGTH = 0.5
	POLEMASS_LENGTH = MASSPOLE * LENGTH
	STEP = dt
	FOURTHIRDS = 1.3333333333333

	costheta = cos(theta)
	sintheta = sin(theta)

	# mathhhh
	temp = (force + POLEMASS_LENGTH * theta_dot  *theta_dot * sintheta)/ TOTAL_MASS

	thetaacc = (GRAVITY * sintheta - costheta* temp)/(LENGTH * (FOURTHIRDS - MASSPOLE * costheta * costheta/ TOTAL_MASS))

	xacc  = temp - POLEMASS_LENGTH * thetaacc* costheta / TOTAL_MASS

	next_state = [x + STEP * x_dot, x_dot + STEP *xacc, theta + STEP * theta_dot, theta_dot + STEP * thetaacc]

	return next_state

# force, x, x_dot, theta, theta_dot
def get_steps(initial_state, step_cnt, dt):
	state = initial_state
	states = [[0] + state]

	MAX_FORCE = 5

	t = 0
	for i in range(STEP_CNT):
		t = t + dt
		force = 0

		state = simulation.simulate_step(state, force, dt)
		states.append([t] + state)

	return array(states)
