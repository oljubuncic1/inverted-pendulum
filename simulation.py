from math import sin, cos, pi
from numpy import array
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

def convert_action(a):
	return 0

def reward(state):
	return 0

def is_terminal(state):
	return False

# force, x, x_dot, theta, theta_dot
def get_steps_qlearning(initial_state, step_cnt, dt):
	state = initial_state
	states = [[0] + state]

	Q = qlearning.initial([255, 255, 255])

	MAX_FORCE = 5
	t = 0
	for i in range(step_cnt):
		t = t + dt
		
		a = qlearning.action(Q, state)
		force = convert_action(a)
		next_state = simulate_step(state, force, dt)
		r = reward(state)

		Q = qlearning.update(Q, state, a, next_state, r)

		states.append([t] + next_state)
		state = next_state

		if is_terminal(state):
			state = initial_state

	return array(states)
