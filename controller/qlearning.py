import simulation
import random
from math import pi
import numpy as np



def action(Q, state, k = 2):
	state[0] = int( state[0] / (2 * pi) * Q.shape[0] )
	state[1] = int( state[1] / (2 * pi) * Q.shape[1] )
	state = tuple(state)
	
	actions = Q[state]

	probabilities = []
	total = 0
	for a in actions:
		curr_probability = k ** a
		probabilities.append(total + curr_probability)
		total = total + curr_probability

	probabilities = [p / total for p in probabilities]

	# print probabilities
	# raw_input("stop.")

	chance = random.random()
	for i in range(len(probabilities)):
		if chance < probabilities[i]:
			return i

def update(Q, s, a, next_s, r, gamma = 0.5):
	max_action = max( list(Q[ tuple(next_s) ]) )
	Q[ tuple( s + [a] ) ] = r + gamma * max_action

	# print Q
	# raw_input("hehe")

	return Q
