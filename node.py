import numpy as np
class Node:
    def __init__(self, node, parent, action, movingPiece, cost, heuristicValue):
        self.node = node
        self.parent = parent
        self.action = action
        self.movingPiece = movingPiece
        self.cost = cost
        self.heuristicValue = heuristicValue

        # create a unique Identifier for each node created
        if self.node:
            self.ID = ''.join(str(s) for s in self.node)

    # overloaded the equal and less than operator to work with nodes 
    # taken from https://www.geeksforgeeks.org/operator-overloading-in-python/
    def __eq__(self, other):
        return self.ID == other.ID

    def __lt__(self, other):
        return self.ID < other.ID

def reshapePuzzle(puzzleState):
    n = int(len(np.array(puzzleState)) ** 0.5)
    puzzleState = np.reshape(np.array(puzzleState), (n, n))
    print(puzzleState)