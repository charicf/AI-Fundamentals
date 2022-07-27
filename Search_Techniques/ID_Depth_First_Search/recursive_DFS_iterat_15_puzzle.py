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
	# goal: store the goal as a tuple because is unmutable
	# root_node: The root node from where the search begins
	# number_nodes: Counter that keeps the number of nodes expanded in the search
	# closed_list: It keeps track of the expanded nodes so it does not get into loops or repeat steps when the limit changes. 
class Game:

	__slots__ = ('goal', 'root_node', 'number_nodes', 'closed_list' )
	def __init__(self, root_state):
		#self.goal = (1,2,3,4,5,6,7,8,0)
		#self.goal = (1,2,3,0)
		#self.goal = (1,2,3,8,0,4,7,6,5)
		self.goal = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
		
		self.root_node = Node(root_state)
		self.number_nodes = 0
		self.closed_list = []
		
	# This method create a children from the parent node and the action that is passed as in the parameters. It returns a child node.
	def create_children(self, node, action):
		
		child_node = Node(node.state)
		child_node.parent = node
		getattr(child_node, action)()

		return child_node

	# This method finds the path. To do so, it uses the solution_action attribute to store the actions that should be taken and it uses the parent to
	# move up in the tree until it gets to the root node.
	# Returns the path of actions to find the result.
	def computate_path(self, node):

		path = []
		while node.solution_action != '':
			path.insert(0, node.solution_action)
			node = node.parent

		return path

	# This method executes the recursive depth limit search. First it checks if the goal has been achieved. I it is, it returns the node. If the limit (the 
	# level until where the algorithm will search in the tree) is achieved, it returns 'cutoff'. Else, it will check for every child of the current node. For
	# each of the children it will call the recursive_depth_limit_search method recursively to find the solution. If it reaches the limit (limit == 0) and it
	# has checked all the children, it will return to the previous node and expand it until it finds the goal. If it does not find the goal with the initial
	# limit, it will return cutoff to the depth_limit_search() and iterative_deepening_search() methods to increase the limit. If a solution is not found after
	# exoanding all the nodes, it will return 'failure'.
	def recursive_depth_limit_search(self, node, limit):

		if tuple(node.state) == self.goal: # GOAL TEST
			return node
		elif limit == 0:
			return 'cutoff'
		else:
			cutoff_occured = False
			self.number_nodes += 1 # It counts the nodes that are going to be expanded (Different than the nodes being evaluated (Level 0 has evaluated nodes but no expanded nodes))
			self.closed_list.append(tuple(node.state)) # It adds the node that is going to be expanded

			action_methods = ('move_left', 'move_right', 'move_up', 'move_down')
			#action_methods = ('move_up', 'move_down', 'move_left', 'move_right')

			for action in action_methods:

				child_node = self.create_children(node, action)

				if tuple(child_node.state) in self.closed_list: # Checks if the child_node has already been explored. It it has, it continues with next iterattion. It does not mean that the children of an already explored node will not be generated
					continue

				result = self.recursive_depth_limit_search(child_node, limit-1)
				if result == 'cutoff':
					cutoff_occured = True
				elif result != 'failure':
					return result

			if cutoff_occured:
				return 'cutoff'
			else:
				return 'failure'

	# This method calls the recursive_depth_limit_search() method and send it the root_node and the limit. As recursive_depth_limit_search() is recursive, this
	# method needs to call it the first time with the root node.
	def depth_limit_search(self, limit):
		return self.recursive_depth_limit_search(self.root_node, limit)

	
	# This method controls the iterations. So it increases the limit each time that the solution was not found.
	def iterative_deepening_search(self):

		time_start = time.time()

		depth = 0
		while True:

			if time.time() - time_start > 30:
				print('Solution cannot be found, timeout')
				sys.exit(0)

			self.closed_list = [] # The closed list is reset to allow the tree to be generated again for the new limit
			result = self.depth_limit_search(depth)
			depth += 1 

			if result != 'cutoff':

				time_end = time.time()
				duration = time_end - time_start
				if result == 'failure':
					print('Failure. Result was not found')
					sys.exit(0)
				else:
					path = self.computate_path(result)
				return (result.state, path, self.number_nodes, duration)

# The root state is passed by the command line throuhg the argparse package.
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--root_state", nargs='+', type= int, required=True, help="array with 16 items. 0 is the blank space")

args = vars(ap.parse_args())
root_state = args['root_state']

ps = psutil.Process(os.getpid())
memory_usage_start = ps.memory_info()

puzzle_game = Game(root_state)
result = puzzle_game.iterative_deepening_search() # Starts the game solution

memory_usage = (ps.memory_info()[0] - memory_usage_start[0])/1024

# Display results section
print('Solution: {}'.format(result[0]))
print('Moves: {}'.format(result[1]))
print('Number of Nodes expanded: {}'.format(result[2]))
print('Time taken (s): {}'.format(result[3]))
print('Memory Used: {}'.format(memory_usage))
