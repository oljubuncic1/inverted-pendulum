import simulation
import random
from numpy import array

# force, x, x_dot, theta, theta_dot
def get():
	state = [0, 0, 0, 0]
	states = [[0] + state]

	MAX_FORCE = 5
	STEP_CNT = 500

	t = 0
	dt = 0.02
	for i in range(STEP_CNT):
		t = t + dt
		force = 0

		state = simulation.simulate(state, force)
		states.append([t] + state)

	return array(states)
