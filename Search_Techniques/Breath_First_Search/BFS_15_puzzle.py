import argparse
import sys
import queue
import time
import os, psutil

# Class that represents a node.
# attributes: 
	# parent: store the parent node of type Node
	# solution_action: stores the action from the paren't perspectiv to get to his node (it will be used to format the path)
	# state: stores the array of tiles
	# blank_idx: stores the position of the blank tile

class Node:
 	
	__slots__ = ('parent', 'solution_action', 'state', 'blank_idx' )
	def __init__(self, state, solution_action=''):

		self.parent = ''
		self.solution_action = solution_action
		self.state = state[:]
		self.blank_idx = state.index(0)

	# ACTIONS

	# Method that exchanges the value between the blank space and the value in its left. As the state is an array, the module is used to find out if the 
	# blank tilde can be moved left
	def move_left(self):

		#if (self.blank_idx % 2 != 0):
		#if (self.blank_idx % 3 != 0):
		if (self.blank_idx % 4 != 0):
			self.state[self.blank_idx] = self.state[self.blank_idx - 1]
			self.state[self.blank_idx - 1] = 0
			self.blank_idx -= 1

	# Method that exchanges the value between the blank space and the value in its right. As the state is an array, the module is used to find out if the 
	# blank tilde can be moved right
	def move_right(self):

		if (self.blank_idx % 4 != 3):
			self.state[self.blank_idx] = self.state[self.blank_idx + 1]
			self.state[self.blank_idx + 1] = 0
			self.blank_idx += 1

	# Method that exchanges the value between the blank space and the value "above it". As the state is an array, the blanj position is used to find  
	# out if the blank tilde can be moved up
	def move_up(self):

		if (self.blank_idx >= 4):
			self.state[self.blank_idx] = self.state[self.blank_idx - 4]
			self.state[self.blank_idx - 4] = 0
			self.blank_idx -= 4

	# Method that exchanges the value between the blank space and the value "below it". As the state is an array, the blanj position is used to find  
	# out if the blank tilde can be moved down
	def move_down(self):

		if (self.blank_idx <= 11):
			self.state[self.blank_idx] = self.state[self.blank_idx + 4]
			self.state[self.blank_idx + 4] = 0
			self.blank_idx += 4

# Class that represents the puzzle game.
# attributes: 
	# goal: store the goal as a tuple because is unmutable
	# open_list: stores the frontier. As it is a BFS, the queue data structure allows to analyze the node that was enqueued first (First In First Out)
	# closed_list: store the already visited nodes. It is a list of tuples (unmutable)
	# blank_idx: stores the position of the blank tile
class Game:

	def __init__(self, root_state):

		self.goal = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
		self.open_list = queue.Queue ()
		self.root_node = Node(root_state)
		self.closed_list = []

		self.open_list.put(self.root_node)

	# This method expands the frontier from the node that is passed as an argument. It creates the new nodes and sends the action to be stored in 
	# node.solution_action. Also, it sets the parent node and executes the action (left, right, up, down). Finally, if the node state is not in
	# the closed_list, it is added to the open_list queue to be explored latter on. This method repeats the proces four times for each action.
	# If the action is not possible, the state will not change. Therefore, the condition ensures that this node will not be added to the frontier.
	# It also ensures that already visited nodes will not be in the frontier.
	def create_children(self, node):
		
		# Move left Action
		temp_node = Node(node.state, 'L')
		temp_node.parent = node
		temp_node.move_left()
		#if tuple(temp_node.state) not in self.closed_list: children.append(temp_node)
		if tuple(temp_node.state) not in self.closed_list: self.open_list.put(temp_node) # if the node state is not in the closed list, it is added to the open list

		# Move right Action
		temp_node = Node(node.state, 'R')
		temp_node.parent = node
		temp_node.move_right()
		if tuple(temp_node.state) not in self.closed_list: self.open_list.put(temp_node) # if the node state is not in the closed list, it is added to the open list

		# Move up Action
		temp_node = Node(node.state, 'U')
		temp_node.parent = node
		temp_node.move_up()
		if tuple(temp_node.state) not in self.closed_list: self.open_list.put(temp_node) # if the node state is not in the closed list, it is added to the open list

		#Move down Action
		temp_node = Node(node.state, 'D')
		temp_node.parent = node
		temp_node.move_down()
		if tuple(temp_node.state) not in self.closed_list: self.open_list.put(temp_node) # if the node state is not in the closed list, it is added to the open list

	# This method finds the path. To do so, it uses the solution_action attribute to store the actions that should be taken and it uses the parent to
	# move up in the tree until it gets to the root node.
	# Returns the path of actions to find the result.
	def computate_path(self, node):

		path = []
		while node.solution_action != '':
			path.insert(0, node.solution_action)
			node = node.parent

		return path

	# This method executes the solution (BFS search). It gets the first node in the queue to be analyzed. After that, is executes the goal test to determine
	# if the node contains the goal. If it does it returns the state, path and number of expanded nodes. It it does not contains the goal, it adds the 
	# node to the closed_list and calls the create_children method 
	def start(self):

		timeout_start = time.time()
		while self.open_list.qsize() > 0:

			if time.time() - timeout_start > 30:
				print('Solution cannot be found')
				sys.exit(0)

			node = self.open_list.get()

			if tuple(node.state) == self.goal: # GOAL TEST

				path = self.computate_path(node)

				return (node.state, path, len(self.closed_list))

			else:
				self.closed_list.append(tuple(node.state)) # Adds state to the closed list
				self.create_children(node)			

# The root state is passed by the command line throuhg the argparse package.
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--root_state", nargs='+', type= int, required=True, help="array with 16 elements. 0 is the blank space")

args = vars(ap.parse_args())
root_state = args['root_state']

# It checks for the correct size of the root node.
if len(root_state) == 16: 

	time_start = time.time()

	ps = psutil.Process(os.getpid())
	memory_usage_start = ps.memory_info()

	puzzle_game = Game(root_state)
	result = puzzle_game.start() # Starts the game solution
	
	time_end = time.time()

	memory_usage = (ps.memory_info()[0] - memory_usage_start[0])/1024

	duration = time_end - time_start

	# Display results section
	print('Solution: {}'.format(result[0]))
	print('Moves: {}'.format(result[1]))
	print('Number of Nodes expanded: {}'.format(result[2]))
	print('Time taken (s): {}'.format(duration))
	print('Memory Used: {}'.format(memory_usage))


else:
	print('The correct number of tiles is 16')
	sys.exit(0)