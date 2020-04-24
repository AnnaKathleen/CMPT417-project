from collections import deque
from node import Node

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0
        
def getSuccessors(currNode):
    global num_nodes_expanded
    num_nodes_expanded += 1
    children = list()
    for i in range(1,5):
        newPosition = currNode.node[:]
        index = newPosition.index(0)
        noneTrue = False
        if i == 1: # move the 0 up
            if index not in range(0, puzzle_side_len):
                tempState = newPosition[index - puzzle_side_len]
                newPosition[index - puzzle_side_len] = newPosition[index]
                newPosition[index] = tempState
            else:
                noneTrue = True
                finalPosition = None

        elif i == 2: # move the 0 down
            if index not in range(puzzleSize - puzzle_side_len, puzzleSize):
                tempState = newPosition[index + puzzle_side_len]
                newPosition[index + puzzle_side_len] = newPosition[index]
                newPosition[index] = tempState
            else:
                noneTrue = True
                finalPosition = None
        
        elif i == 3: # move the 0 left
            if index not in range(0, puzzleSize ,puzzle_side_len):
                tempState = newPosition[index - 1]
                newPosition[index - 1] = newPosition[index]
                newPosition[index] = tempState
            else:
                noneTrue = True
                finalPosition = None

        elif i == 4: # move the 0 right
            if index not in range(puzzle_side_len - 1, puzzleSize, puzzle_side_len):
                tempState = newPosition[index + 1]
                newPosition[index + 1] = newPosition[index]
                newPosition[index] = tempState
            else:
                noneTrue = True
                finalPosition = None
        if noneTrue == True:
            children.append(Node(finalPosition,currNode,i,0))
        else:
            children.append(Node(newPosition,currNode,i,0))
            # print(children)
    
    successors = [children for children in children if children.node]
    # print(successors)
    return successors


def stepBack(startNode,node):
    currNode = node
    directions = list()
    while  currNode.node != startNode:
        if currNode.action == 1:
            currAction = 'move 0 Up'
        elif currNode.action == 2:
            currAction = 'move 0 Down'
        elif currNode.action == 3:
            currAction = 'move 0 Left'
        else:
            currAction = 'move 0 Right'
        
        directions.append(currAction)
        currNode = currNode.parent
    return directions

def heuristic(currState, goalState):
    return sum(abs(b % puzzle_side_len - g % puzzle_side_len) + abs(b//puzzle_side_len - g//puzzle_side_len)
               for b, g in ((currState.index(i), goalState.index(i)) for i in range(1, puzzleSize)))

def ast(startState, goalState):
    pass


def main():
    global puzzleSize, puzzle_side_len
    startState = [0,8,7,6,5,4,3,2,1]
    goalState = [0,1,2,3,4,5,6,7,8]
    puzzleSize = len(startState)
    puzzle_side_len = int(puzzleSize ** 0.5)
    ast(startState, goalState)

main()
