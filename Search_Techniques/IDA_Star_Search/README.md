# Iterative Deepening A* Search - Artificial Intelligence

IDA* 15 puzzle is a Python script for finding the solution to a 15 puzzle game by using Iterative Deepening A Star Search algorithm. It can use two types of heuristics. The script will return the following:

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

The following arguments are defined: 

```python
"-s", "--root_state", type= int, required=True, help="array with 16 items. 0 is the blank space"
"-t", "--heuristic_type", type= int, default=1, help="heuristic type. 0: Misplaced tiles, 1: Manhattan"
```

Example of how to run the program

```python

python A-star_15_puzzle.py -s 1 2 0 4 6 7 3 8 5 9 10 12 13 14 11 15 -t 1

```

## Contributing
Pull requests are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)