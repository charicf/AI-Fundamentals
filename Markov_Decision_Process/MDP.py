from support import argmax,vector_add, orientations, turn_right, turn_left, print_table
import random
import argparse

class MDP:

	def __init__(self, init, actlist, terminals, transitions = {}, reward = None, states=None, gamma=.9):
		if not (0 < gamma <= 1):
			raise ValueError("0 < gamma <= 1")

		if states:
			self.states = states
		else:
			self.states = self.get_states_from_transitions(transitions)
			
		
		self.init = init
		
		if isinstance(actlist, list):
			## if actlist is a list, all states have the same actions
			self.actlist = actlist
		elif isinstance(actlist, dict):
			## if actlist is a dict, different actions for each state
			self.actlist = actlist
		
		self.terminals = terminals
		self.transitions = transitions
		if self.transitions == {}:
			print("Transition table is empty.")
		self.gamma = gamma
		if reward:
			self.reward = reward
		else:
			self.reward = {s : 0 for s in self.states}

	def R(self, state):
		return self.reward[state]

	def T(self, state, action):
		"""Transition model. From a state and an action, return a list
		of (probability, result-state) pairs."""
		if(self.transitions == {}):
			raise ValueError("Transition model is missing")
		else:
			return self.transitions[state][action]

	def actions(self, state):

		if state in self.terminals:
			return [None]
		else:
			return self.actlist

	def get_states_from_transitions(self, transitions):
		if isinstance(transitions, dict):
			s1 = set(transitions.keys())
			s2 = set([tr[1] for actions in transitions.values() 
							  for effects in actions.values() for tr in effects])
			return s1.union(s2)
		else:
			print('Could not retrieve states from transitions')
			return None

	def check_consistency(self):
		# check that all states in transitions are valid
		assert set(self.states) == self.get_states_from_transitions(self.transitions)
		# check that init is a valid state
		assert self.init in self.states
		# check reward for each state
		#assert set(self.reward.keys()) == set(self.states)
		assert set(self.reward.keys()) == set(self.states)
		# check that all terminals are valid states
		assert all([t in self.states for t in self.terminals])
		# check that probability distributions for all actions sum to 1
		for s1, actions in self.transitions.items():
			for a in actions.keys():
				s = 0
				for o in actions[a]:
					s += o[0]
				assert abs(s - 1) < 0.001

class GridMDP(MDP):

	def __init__(self, parameters, init=(0, 0), gamma=0.85):
		reward = {}
		states = set()
		gamma = parameters["discount_rate"]
		grid, terminals = self.create_grid(parameters)
		self.rows = len(grid)
		self.cols = len(grid[0])
		self.grid = grid
		self.transition_model = parameters["transition_probabilities"]
		for x in range(self.rows):
			for y in range(self.cols):
				if grid[x][y] is not None:
					states.add((x, y))
					reward[(x, y)] = grid[x][y]
		self.states = states
		actlist = orientations # [(1, 0), (0, 1), (-1, 0), (0, -1)]
		transitions = {}
		for s in states:
			transitions[s] = {}
			for a in actlist:
				transitions[s][a] = self.calculate_T(s, a)
		MDP.__init__(self, init, actlist=actlist,
					 terminals=terminals, transitions = transitions, 
					 reward = reward, states = states, gamma=gamma)

	def create_grid(self, parameters):

		terminals = []

		row = parameters['size'][0]
		column = parameters['size'][1]
		grid = [[0] * row for i in range(column)]

		for wall in parameters['walls']:
			grid[wall[1]-1][wall[0]-1] = None

		for state in parameters['terminal_states']:
			grid[state[1]-1][state[0]-1] = state[2]
			terminals.append((state[1]-1, state[0]-1))

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				if grid[i][j] == 0:
					grid[i][j] = parameters['reward']

		return grid, terminals

	def calculate_T(self, state, action):
		if action is None:
			return [(0.0, state)]
		else:
			return [(self.transition_model[0], self.go(state, action)),
					(self.transition_model[1], self.go(state, turn_right(action))),
					(self.transition_model[2], self.go(state, turn_left(action)))]
	
	def T(self, state, action):
		if action is None:
			return [(0.0, state)]
		else:
			return self.transitions[state][action]
 
	def go(self, state, direction):
		"""Return the state that results from going in this direction."""
		state1 = vector_add(state, direction)
		return state1 if state1 in self.states else state

	def to_grid(self, mapping):
		return list(reversed([[mapping.get((y, x), None)
							   for x in range(self.cols)]
							  for y in range(self.rows)]))

	def to_dir(self, policy):
		chars = {
			(1, 0): 'N', (0, 1): 'E', (-1, 0): 'S', (0, -1): 'W', None: 'T'}
		return self.to_grid({s: chars[a] for (s, a) in policy.items()})

def print_valueiterations(U, row, col):
	a = dict(U)
	
	for r in range(row-1,-1,-1):
		for c in range(col):
			item = (a.get((r,c),'--------------'))
			if item == '--------------':
				print(item,end = '|\t')
			else:
				print(round(item,12),end = '|\t')
		print()

def value_iteration(mdp, epsilon=0.001):
	"""Solving an MDP by value iteration. [Figure 17.4]"""
	U1 = {s: 0 for s in mdp.states}
	R, T, gamma = mdp.R, mdp.T, mdp.gamma
	i=1
	while True:
		U = U1.copy()
		delta = 0
		for s in mdp.states:
			U1[s] = R(s) + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)]) for a in mdp.actions(s)])
			delta = max(delta, abs(U1[s] - U[s]))
		
		print('iteration' + str(i)+ '\n')
		print_valueiterations(U1,mdp.rows,mdp.cols)
		print('\n')
		i=i+1
		if delta < epsilon * (1 - gamma) / gamma:
			break

def expected_utility(a, s, U, mdp):
	"""The expected utility of doing a in state s, according to the MDP and U."""
	return sum([p * U[s1] for (p, s1) in mdp.T(s, a)])

def policy_iteration(mdp):
	"""Solve an MDP by policy iteration [Figure 17.7]"""
	U = {s: 0 for s in mdp.states}
	pi = {s: random.choice(mdp.actions(s)) for s in mdp.states}
	while True:
		U = policy_evaluation(pi, U, mdp)
		unchanged = True
		for s in mdp.states:
			a = argmax(mdp.actions(s), key=lambda a: expected_utility(a, s, U, mdp))
			if a != pi[s]:
				pi[s] = a
				unchanged = False
		if unchanged:
			print_table(mdp.to_dir(pi))
			break

def policy_evaluation(pi, U, mdp, k=20):

	R, T, gamma = mdp.R, mdp.T, mdp.gamma
	for i in range(k):
		for s in mdp.states:
			U[s] = R(s) + gamma * sum(p * U[s1] for (p, s1) in T(s, pi[s]))
	return U

def read_file(description_file):

	#parameters = {'size', 'walls', 'terminal_states', 'reward', 'transition_probabilities', 'discount_rate', 'epsilon'}
	parameters = {}

	for line in open(description_file).readlines():

		if ':' in line:
			idx = line.index(':')

			param = line[:idx].strip()
			values = line[idx+1:].strip()

			if param == 'size':
				parameters['size'] = (int(values.rsplit(' ')[0].strip()), int(values.rsplit(' ')[1].strip()))

			elif param == 'walls':
				walls = values.rsplit(',')
				walls_list = []

				for wall in walls:
					walls_list.append((int(wall.strip().rsplit(' ')[0]),  int(wall.strip().rsplit(' ')[1])))

				parameters ['walls'] = tuple(walls_list)

			elif param == 'terminal_states':
				states = values.rsplit(',')
				states_list = []

				for state in states:
					states_list.append((int(state.strip().rsplit(' ')[0]),  int(state.strip().rsplit(' ')[1]), float(state.strip().rsplit(' ')[2])))

				parameters ['terminal_states'] = tuple(states_list)

			elif param == 'transition_probabilities':
				parameters['transition_probabilities'] = [float(n) for n in values.rsplit(' ')]
			
			elif param == 'reward' or param == 'discount_rate' or param == 'epsilon':
				parameters[param] = float(values)

	return parameters

def main():

	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--description_file", required=True, help="txt file that contains the description for the MDP")

	args = vars(ap.parse_args())

	description_file = args["description_file"]

	parameters = read_file(description_file)

	mdp = GridMDP(parameters)

	value_iteration(mdp, parameters['epsilon'])

	policy_iteration(mdp)

	print('\nParameters: ', parameters)

if __name__ == '__main__':
	main()