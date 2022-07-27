# Iterative Deepening Depth First Search - Artificial Intelligence
15 puzzle is a sliding puzzle game with numbered squares arranged in 4X4 grid with one tile missing. The puzzle is solved when the numbers are arranged in order. This is a Python script for finding the solution to a 15 puzzle game by using Iterative Deepening Depth First Search algorithm. The script will return the following:

```bash
Solution: Ordered tiles
Moves: Path with list of actions to reach the solution
Number of Nodes expanded: Number of nodes expanded during the search
Time taken (s): Time taken to reach the solution
Memory Used: Memory usage by the process running the script
```

## Packages
The project uses the following packages: argparse, sys, time, os, psutil. It one package is not installed, install it with the following command.

```bash
pip install 'package'
```

## Usage

The script accepts a sequence of number entered from the command line. The number of elements has to be 16.

The following argument is defined: 

```python
"-s", "--root_state", type= int, required=True, help="array with 16 items. 0 is the blank space")
```

Example of how to run the program

```python

python recursive_DFS_iterat_15_puzzle.py -s 1 3 4 8 5 2 0 6 9 10 7 11 13 14 15 12

```

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)