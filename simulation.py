from math import sin, cos, pi
from numpy import array
import qlearning
import fuzzy
import matplotlib.pyplot as plt

def scale(x):
	while x > 2 * pi:
		x = x - 2 * pi

	return x

def simulate_step(state, force, dt):
	x, x_dot, theta, theta_dot = state[0], state[1], state[2], state[3]

	theta = scale(theta)
	theta_dot = scale(theta_dot)

	# constants
	GRAVITY=9.8
	MASSCART=5.0
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
	next_state[2] = scale(next_state[2])
	next_state[3] = scale(next_state[2])

	return next_state

def convert_action(a):
	MAX_FORCE = 5.0
	
	return MAX_FORCE * (a / 255.0)

def reward(state):
	theta = state[2]

	print str(round(theta, 2)) + " " + str(pi / 2)

	if abs(theta) < 0.01:
		return 1000.0
	elif theta > pi / 2.0:
		return -1000.0
	else:
		return 0

def is_terminal(state):
	theta = state[2]

	return theta > pi / 2.0

# force, x, x_dot, theta, theta_dot
def get_steps_qlearning(initial_state, step_cnt, dt):
	state = initial_state
	states = [[0] + state]

	Q = qlearning.initial( (10, 10, 10) )

	t = 0
	for i in range(step_cnt):
		t = t + dt
		
		a = qlearning.action(Q, state[2:4])
		force = convert_action(a)
		
		# print a
		# print force
		# print state

		next_state = simulate_step(state, force, dt)
		r = reward(next_state)

		Q = qlearning.update(Q, state[2:4], a, next_state[2:4], r)

		states.append([t] + next_state)
		state = next_state

		if is_terminal(state):
			state = initial_state

	print Q

	# return array(states)
	return [ s[2] for s in states ]

def scale_output(x, factor=1.):
    return x * factor

def get_steps_fuzzy(initial_state, step_cnt, dt):
	# state is x, x_dot, theta, theta_dot
	# step_cnt number of simulation steps
	# dt time interval of simulation
	state = initial_state
	states = [[0] + state]

	controller = fuzzy.get_controller()

	forces = []

	t = 0
	for i in range(step_cnt):
#		print state
		t = t + dt
		
		theta = state[2]
		dtheta = state[3]
		controller.input['theta'] = theta - pi
		controller.input['dtheta'] = dtheta - pi
		controller.compute()

		output_force = controller.output['force']
		output_force = scale_output(output_force, 50)
		forces.append(output_force)
		#print theta-pi, dtheta-pi, output_force
		if theta != dtheta:
			print 'hi', theta, dtheta

		# output_force = 0

		next_state = simulate_step(state, output_force, dt)
		next_state[0] = 0
		states.append([t] + next_state)
		state = next_state
	return [s[2] for s in states]
