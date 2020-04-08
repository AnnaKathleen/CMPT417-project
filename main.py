import numpy as np
# import BFS
# import DFS


eightPuzzle = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
fifteenPuzzle = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])

goalState = eightPuzzle

# Randomize the puzzle to get the starting state of the problem
def getStartState():
    startState = goalState.ravel()
    np.random.shuffle(startState)
    n = np.shape(startState)
    return startState.reshape(n,n)

# get the user to choose the algorithm to solve the puzzle
def chooseAlgorithm():
    algorithms = ["BFS","DFS","A*","IDA*"]
    while True:  
        choice = input("Choose which of the above algorithms you would like to use to solve the 8-Puzzle ")
        if(choice.upper() in algorithms):  
            break 
    return choice

# solve the algorithm using the specified algorithm 
def solve(solver, startState, goalState):
    if solver.upper() == "BFS":
        output = BFS(startState, goalState)
    elif solver.upper() == "DFS":
        output = DFS(startState, goalState)
    return output

if __name__ == "__main__":
    startState = getStartState()
    solver = chooseAlgorithm()
    # solve(solver, startState, goalState)