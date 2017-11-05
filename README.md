# backtrack
---
Implementation of backtracking search method for constrain propagation problem. Provides options of minimum remaining value heuristic and forward checking heuristic for the search.

## Running backtrack
---
Run from the root of the root of the project directory with the following command: `python my_hw2.py mrv puz-001.txt`

type: Provides the type of the heuristic to run the search with.

file: Provides the name of the puzzle file with the initial state of the sudoku puzzle.

## Dependencies
---
Uses Python version 3.5.3

## Sample Output
---
```
>>> python backtrack.py mrv puz-001.txt
7 8 1 6 3 2 9 4 5
9 5 2 7 1 4 6 3 8
4 3 6 8 9 5 7 1 2
2 4 9 3 7 6 8 5 1
6 7 3 5 8 1 2 9 4
5 1 8 4 2 9 3 6 7
1 9 4 2 6 7 5 8 3
8 6 7 1 5 3 4 2 9
3 2 5 9 4 8 1 7 6

Took 199 guesses
```
