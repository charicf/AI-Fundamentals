# Markov Decision Process - Artificial Intelligence

Markov Decision Process (MDP) is a Python script for finding the value of states and the optimal policy for a given grid world. It aims to resolve a sequential decision problem by incorporating utilities, uncertainty, and sensing. It uses value iteration to print the values of states in each iteration and the final policy. Also, it performs a modified policy iteration to calculate and print the optimal policy. This MDP mini-project is a starting point towards reinforcement learning.

---------------------------------------------

## Usage

The script reads the description of the MDP from a text file. The text file should have the following structure (comas and spaces have to follow the described pattern):

#size of the gridworld

size : 5 4

#list of location of walls

walls : 2 2 , 2 3 

#list of terminal states (row,column,reward)

terminal_states : 5 3 -3 , 5 4 +2, 4 2 +1

#reward in non-terminal states

reward : -0.04

#transition probabilites (Up, Right, Left, Down)

transition_probabilities : 0.8 0.1 0.1 0

discount_rate : 0.85

epsilon : 0.001

---------------------------------------------

##Support package

The script uses some methods defined in the support script. Therefore, support.py must be in the same directory than the main script.

---------------------------------------------

##Running the program

Arguments

```python
"-f", "--description_filerequired=True, help="txt file that contains the description for the MDP"

```

Example of how to run the program

```python

python MDP.py -f mdp_input.txt

```

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)