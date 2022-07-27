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
	
	__slots__ = ('parent', 'solution_action', 'state', 'blank_idx', 'board_size' )
	def __init__(self, state, solution_action=''):

		self.parent = ''
		self.solution_action = solution_action
		self.state = state[:]
		self.blank_idx = state.index(0)
		self.board_size = int(len(state)**(1/2)) # defining length/width of the board

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
	# goal: stores the goal as a tuple because is unmutable
	# frontier: stores the calculated paths for expanding and their corresponding heuristic values
	# root_node: The root node from where the search begins
	# number_nodes: Counter that keeps the number of nodes expanded in the search
	# closed_list: It keeps track of the expanded nodes so it does not get into loops or repeat steps when the limit changes. 
class Game:

	__slots__ = ('goal', 'root_node', 'number_nodes', 'closed_list', 'frontier' )
	def __init__(self, root_state):
		#self.goal = (1,2,3,4,5,6,7,8,0)
		#self.goal = (1,2,3,0)
		#self.goal = (1,2,3,8,0,4,7,6,5)
		self.goal = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
		self.frontier = []
		self.root_node = Node(root_state)
		self.number_nodes = 0
		self.closed_list = []
		
	# This method creates the children from the parent node.
	def create_children(self, node):
		
		children = []
		action_methods = ['move_left', 'move_right', 'move_up', 'move_down']

		for action in action_methods:

			temp_node = Node(node.state)
			temp_node.parent = node
			getattr(temp_node, action)()
			if tuple(temp_node.state) not in self.closed_list: children.append(temp_node) # if the node state is not in the closed list, it is considered

		return children

	# This method finds the path. To do so, it uses the solution_action attribute to store the actions that should be taken and it uses the parent to
	# move up in the tree until it gets to the root node.
	# Returns the path of actions to find the result.
	def computate_path(self, node):

		path = []
		while node.solution_action != '':
			path.insert(0, node.solution_action)
			node = node.parent

		return path

	# This function evaluates if each tile in the state is equal to the value of the goal in the same position. If it is not, it increments the 
	# score in one. Therefore, it returns the number of tiles that are not in the right position.
	def misplaced_tiles_heuristic (self, state):

		score = 0
		for idx in range(0, len(state)):
			if state[idx] != self.goal[idx]:
				score += 1

		return score

	# This function returns the sum of the number of steps that each tile has to take to be in the right position. For the position of
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
	
	# This method performs the A* search. Once it finds the best heuristic in the frontier, and the related path, it expands the last node in that 
	# path. Then, for each children, it computes the new path. This new path will contain the new heuristics value and the current path (with the 
	# created child). Finally, it adds each path to the frontier and the expanded node to the closed list. If the goal is founded it returns the 
	# required values.
	def start(self, heuristic_type=1):

		time_start = time.time()

		# Compute Mis. Tiles heuristic
		if heuristic_type == 0:
			heuristic_value = self.misplaced_tiles_heuristic(self.root_node.state)
		# Compute  Manhattan heuristic
		else:
			heuristic_value = self.manhattan_heuristic(self.root_node.state)
			

		self.frontier.append([heuristic_value, self.root_node])

		while self.frontier:

			idx_best_heuristic = 0

			if time.time() - time_start > 30:
				print('Solution cannot be found, timeout')
				sys.exit(0)

			# It finds the index of the best heuristic in the frontier (the one that is smaller than the current best heuristic)
			for i in range(1, len(self.frontier)):
				if self.frontier[i][0] < self.frontier[idx_best_heuristic][0]:
					idx_best_heuristic = i

			# Obtain the value of the current best heuristic and the corresponding path
			best_heuristic = self.frontier[idx_best_heuristic][0]
			current_path = self.frontier[idx_best_heuristic][1:]

			end_node = self.frontier[idx_best_heuristic][-1] # Node that is going to be expanded

			self.frontier.pop(idx_best_heuristic) # The best heuristic node is removed from the frontier

			if tuple(end_node.state) == self.goal: # GOAL TEST
				path = self.computate_path(end_node)

				time_end = time.time()
				duration = time_end - time_start

				return (end_node.state, path, self.number_nodes, duration)

			# If the node is in the closed_list it will not be expanded
			if end_node in self.closed_list:
				continue

			children = self.create_children(end_node)

			for child in children:
				if child in self.closed_list:
					continue
				else:

					# Find the heuristic value for the child and the current node (parent node)
					if heuristic_type == 0:
						child_heuristic = self.misplaced_tiles_heuristic(child.state)
						end_node_heuristic = self.misplaced_tiles_heuristic(end_node.state)
						
					else:
						child_heuristic = self.manhattan_heuristic(child.state)
						end_node_heuristic = self.manhattan_heuristic(end_node.state)

					# It calculates the new heuristic for the new path and appends the child to the current path.
					new_path = [best_heuristic + child_heuristic - end_node_heuristic] + current_path + [child]

					# Adds the new path to the frontier and the expanded node to the closed_list
					self.frontier.append(new_path)
					self.closed_list.append(end_node)

			self.number_nodes += 1 # Increases the number of expanded nodes

# The root state is passed by the command line throuhg the argparse package.
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--root_state", nargs='+', type= int, required=True, help="array with 16 items. 0 is the blank space")
ap.add_argument("-t", "--heuristic", type= int, default=1, help="heuristic type. 0: Misplaced tiles, 1: Manhattan")

args = vars(ap.parse_args())
root_state = args['root_state']
heuristic_type = int(args['heuristic'])

ps = psutil.Process(os.getpid())
memory_usage_start = ps.memory_info()

puzzle_game = Game(root_state)
result = puzzle_game.start(heuristic_type) # Starts the game solution

memory_usage = (ps.memory_info()[0] - memory_usage_start[0])/1024

# Display results section
print('Solution: {}'.format(result[0]))
print('Moves: {}'.format(result[1]))
print('Number of Nodes expanded: {}'.format(result[2]))
print('Time taken (s): {}'.format(result[3]))
print('Memory Used: {}'.format(memory_usage))
