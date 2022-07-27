import argparse
import sys
import time
import os, psutil

# Class that represents a node.
# attributes: 
	# parent: store the parent node of type Node
	# solution_action: stores the action from the paren't perspectiv to get to his node (it will be used to format the path)
	# state: stores the array of tiles
	# blank_idx: stores the position of the blank tile
	# board_size: Keeps the board size so the board can be of different sizes
class Node:
	
	__slots__ = ('parent', 'solution_action', 'state', 'blank_idx', 'board_size', 'cost')
	def __init__(self, state, solution_action=''):

		self.parent = ''
		self.solution_action = solution_action
		self.state = state[:]
		self.blank_idx = state.index(0)
		self.board_size = int(len(state)**(1/2)) # defining length/width of the board
		self.cost = 0

	# ACTIONS

	# Method that exchanges the value between the blank space and the value in its left. As the state is an array, the module is used to find out if the 
	# blank tilde can be moved left
	def move_left(self):

		if (self.blank_idx % self.board_size > 0):
			self.state[self.blank_idx] = self.state[self.blank_idx - 1]
			self.state[self.blank_idx - 1] = 0
			self.blank_idx -= 1
			self.solution_action = 'L'

	# Method that exchanges the value between the blank space and the value in its right. As the state is an array, the module is used to find out if the 
	# blank tilde can be moved right
	def move_right(self):

		if (self.blank_idx % self.board_size < self.board_size - 1):
			self.state[self.blank_idx] = self.state[self.blank_idx + 1]
			self.state[self.blank_idx + 1] = 0
			self.blank_idx += 1
			self.solution_action = 'R'

	# Method that exchanges the value between the blank space and the value "above it". As the state is an array, the blanj position is used to find  
	# out if the blank tilde can be moved up
	def move_up(self):

		if (self.blank_idx >= self.board_size):
			self.state[self.blank_idx] = self.state[self.blank_idx - self.board_size]
			self.state[self.blank_idx - self.board_size] = 0
			self.blank_idx -= self.board_size
			self.solution_action = 'U'

	# Method that exchanges the value between the blank space and the value "below it". As the state is an array, the blanj position is used to find  
	# out if the blank tilde can be moved down
	def move_down(self):

		if (self.blank_idx <= (len(self.state) - self.board_size) - 1):
			self.state[self.blank_idx] = self.state[self.blank_idx + self.board_size]
			self.state[self.blank_idx + self.board_size] = 0
			self.blank_idx += self.board_size
			self.solution_action = 'D'

# Class that represents the puzzle game.
# attributes: 
	# goal: store the goal as a tuple because is unmutable
	# root_node: The root node from where the search begins
	# number_nodes: Counter that keeps the number of nodes expanded in the search 
	# heuristic_type: Stores the type of heuristic used in the current search. 0: Misplaced tiles, 1: Manhattan
class Game:

	__slots__ = ('goal', 'root_node', 'number_nodes', 'heuristic_type')
	def __init__(self, root_state, heuristic_type):
		#self.goal = (1,2,3,4,5,6,7,8,0)
		#self.goal = (1,2,3,0)
		#self.goal = (1,2,3,8,0,4,7,6,5)
		self.goal = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
		
		self.root_node = Node(root_state)
		self.number_nodes = 0
		self.heuristic_type = heuristic_type
		
	# This method creates the children from the parent node.
	def create_children(self, node):
		
		children = []
		action_methods = ['move_left', 'move_right', 'move_up', 'move_down']

		for action in action_methods:

			temp_node = Node(node.state)
			temp_node.parent = node
			getattr(temp_node, action)()
			children.append(temp_node)
		return children

	# This method finds the path. To do so, it uses the solution_action attribute to store the actions that should be taken.
	# Returns the path of actions to find the result.
	def computate_path(self, path):

		actions_path = [n.solution_action for n in path[1:]]

		return actions_path

	# This function evaluates if each value of the goal (different than 0) is equal to the value of the tail in the same position. If it is not, it increments
	# the score in one. Therefore, it returns the number of tiles that are not in the right position.
	def misplaced_tiles_heuristic (self, state):

		score = 0
		for idx in range(1, len(state)):
			if idx != state[idx-1]:
				score += 1

		return score

	# This method returns the sum of the number of steps that each tile has to take to be in the right position. For the position of
	# each tile, both in the current state and in the goal, the coordinates in x and y are found. Then, the distances in x and the distances in y
	# are calculated. Finally, the distances are added to found the number of steps.
	def manhattan_heuristic(self, state):

		score = 0

		for idx_state in range(0, len(state)):
			idx_goal = self.goal.index(state[idx_state])

			if state[idx_state] == 0: # The blank tile is not evaluated
				continue

			idx_state_row = int(idx_state/4)
			idx_goal_row = int(idx_goal/4)

			idx_state_col = idx_state%4
			idx_goal_col = idx_goal%4

			score += abs(idx_goal_col-idx_state_col) + abs(idx_goal_row-idx_state_row)

		return score

	# This method calls the desired heuristic
	def calculate_heuristic(self, state):

		return  self.misplaced_tiles_heuristic (state) if self.heuristic_type == 0 else self.manhattan_heuristic (state)

	# This method calculate the cost from the root node to the current node. It takes the parent cost and adds 1 (cost from parent to one children)
	def calculate_cost(self, node):

		node.cost = node.parent.cost + 1
		return node.cost

	# This method executes the recursive depth limit A* search. First it finds the f value of the current node (cost + heuristic). If this values is bigger 
	# than the limit, f is returned and this node is not expanded anymore. If the current node is not the goal, it checks if the state of the child has 
	# already been expanded. If it has not, it is added to the path and the recursive function is called with the new path, cost and same limit. For each node
	# where the f is bigger than the limit (not expanded), that returned f (temp_f) is compared with the current min_f to find the minimum f of all values
	# that exceeded the current limit. So, if the temp_f is less than the current min_f, the new min_f is the current temp_f. If it is not, min_f is still
	# the same. Finally, when all the nodes with f less than the limit have been explored, the current min_f is returned to change the limit in the next 
	# iteration.
	def recursive_DLA_star(self, path, g, limit):

		node = path[-1]
		f = g + self.calculate_heuristic(node.state) # f = g + h

		if f > limit: # The node will not be expanded because its f is bigger than the current limit. This value is returned to find the next limit.
			return f
		if tuple(node.state) == self.goal: # GOAL TEST
			return 'found'

		min_f = 1000 # Random big value. It wll be replaced by the min f from  of all values of f that exceeded the current limit

		self.number_nodes += 1 # It counts the nodes that are going to be expanded (Different than the nodes being evaluated (Level 0 has evaluated nodes but no expanded nodes))

		states = [n.state for n in path] # The states values are extracted from the path to find out if the current state has been explored already
		for child in self.create_children(node):
			
			if child.state not in states:
				path.append(child)

				temp_f = self.recursive_DLA_star(path, self.calculate_cost(child), limit)
				if temp_f == 'found': return 'found'

				if temp_f < min_f: # If the temp_f is less than the current min_f, min_f is updated to ensure that it will allways store the  min f from  of all values of f that exceeded the current limit
					min_f = temp_f

				del path[-1] # The current child node is deleted from the list to append the new child later

		return min_f

	# This method controls the iterations. First, it sets the first limit as the root node's heuristics. Then it calls the recursive_DLA_star() 
	# with a cost = 0. After all the nodes with f less than the limit have been expanded, the recursive method will return a new value of f (temp_f).
	# This temp_f is the minimum f of all values that exceeded the current limit. Therefore, the limit is updated with this value and the search is 
	# initiated again from the root node. 
	def start(self):

		time_start = time.time()
		path = [self.root_node]
		max_bound = 1000 # Random big value that determines if the search has failed.

		limit = self.calculate_heuristic(self.root_node.state)

		while True:

			if time.time() - time_start > 60:
				print('Solution cannot be found, timeout')
				sys.exit(0)

			temp_f = self.recursive_DLA_star(path, 0, limit)

			if temp_f == 'found': 
				time_end = time.time()
				duration = time_end - time_start
				actions_path = self.computate_path(path)

				return (path[-1].state, actions_path, self.number_nodes, duration)
				
			if temp_f == max_bound:
				print('Failure. Result was not found')
				sys.exit(0)

			limit = temp_f # The limit is updated with the new value of f: min f from  of all values of f that exceeded the current limit

# The root state is passed by the command line throuhg the argparse package.
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--root_state", nargs='+', type= int, required=True, help="array with 16 items. 0 is the blank space")
ap.add_argument("-t", "--heuristic_type", type= int, default=1, help="heuristic type. 0: Misplaced tiles, 1: Manhattan")

args = vars(ap.parse_args())
root_state = args['root_state']
heuristic_type = int(args['heuristic_type'])

ps = psutil.Process(os.getpid())
memory_usage_start = ps.memory_info()

puzzle_game = Game(root_state, heuristic_type)
result = puzzle_game.start() # Starts the game solution

memory_usage = (ps.memory_info()[0] - memory_usage_start[0])/1024

# Display results section
print('Solution: {}'.format(result[0]))
print('Moves: {}'.format(result[1]))
print('Number of Nodes expanded: {}'.format(result[2]))
print('Time taken (s): {}'.format(result[3]))
print('Memory Used: {}'.format(memory_usage))
