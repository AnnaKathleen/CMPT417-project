# import numpy as np
import timeit
from node import reshapePuzzle
import argparse
from BFS import BFS
# from DFS import DFS
# from AST import AST
import random

# map sizes:
board_map = {
    # '8Puzzle' : np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]]),
    # '15Puzzle' : np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    '8Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8],
    '15Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
}

# functions:
input()
function_map = {
    'bfs': BFS
    # 'dfs': DFS,
    # 'ast': AST
}

# Randomize the puzzle to get the starting state of the problem
# def getStartState():
#     startState = goalState.ravel()
#     np.random.shuffle(startState)
#     n = np.shape(goalState)
#     return startState.reshape(n[0],n[0])

# get the user to choose the algorithm to solve the puzzle
# def chooseAlgorithm():
#     algorithms = ["BFS","DFS","A*","IDA*"]
#     while True:  
#         choice = input("Choose which of the above algorithms you would like to use to solve the 8-Puzzle ")
#         if(choice.upper() in algorithms):  
#             break 
#     return choice

# solve the algorithm using the specified algorithm 
# def solve(solver, startState, goalState):
#     if solver.upper() == "BFS":
#         output = BFS(startState, goalState)
#     elif solver.upper() == "DFS":
#         output = DFS(startState, goalState)
#     return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('algorithm')
    parser.add_argument('board')
    args = parser.parse_args()

    function = function_map[args.algorithm]
    # print("f: ", str(function))
    board = board_map[args.board]
    # print("b: ", board)
    # input()
    goalState = board
    startState = board
    # # startState = getStartState()
    # random.shuffle(startState)
    # print("Start State: ")
    # reshapePuzzle(startState)
    # print("Goal State: \n")
    # reshapePuzzle(goalState)

    # # function(startState, goalState)

    # # solver = chooseAlgorithm() # not needed anymore.    
    # # solve(solver, startState, goalState) # not needed anymore
