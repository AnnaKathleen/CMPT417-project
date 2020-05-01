import timeit
from math import floor
from node import Node, reshapePuzzle
import random
import argparse

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0
time_constraint = 15 # seconds
maxMemory_constraint =  100000
        
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
            children.append(Node(finalPosition,currNode,i,0,currNode.cost + 1,0))
        else:
            children.append(Node(newPosition,currNode,i,0, currNode.cost + 1,0))
    
    successors = [children for children in children if children.node]
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
    # heuristic is calculated by: in a plane with p1 at (x1, y1) and p2 at (x2, y2), it is |x1 - x2| + |y1 - y2|.
    # x represents the columns and Y represents the rows
    # origin is (0,0) top left corner of grid shown below
    #    0 1 2 
    # 0 |0|1|2|
    # 1 |3|4|5|
    # 2 |6|7|8|
    sum = 0
    for i in range(1, puzzleSize):
        sum += abs(currState.index(i) % puzzle_side_len - goalState.index(i) % puzzle_side_len) + abs(floor(currState.index(i)/puzzle_side_len) - floor(goalState.index(i)/puzzle_side_len))
    return sum


def SMA(startState, goalState):
    pQueue = list()
    memory = 0
    heuristicValue = heuristic(startState, goalState)
    rootNode = Node(startState, None, None, 0, 0, heuristicValue)
    state = (heuristicValue, rootNode)
    pQueue.append(state)

    while pQueue:
        if memory >= maxMemory_constraint:
            print("No solution that fits in the given solution")
            return None
        pQueue.sort(reverse=True) # sort descending by f value
        currNode = pQueue.pop() # pop the last element in the pQueue

        if currNode.node == goalState:
            print("success")
            return None

        successors = getSuccessors(currNode)
        for nextNode in successors:
            if nextNode.node != goalState and  

  

def main():
    global puzzleSize, puzzle_side_len

    parser = argparse.ArgumentParser()
    parser.add_argument('board')
    args = parser.parse_args()
    board = board_map[args.board]

    startState = board
    if len(board) == 9:
        goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    else:
        goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    puzzleSize = len(startState)
    puzzle_side_len = int(puzzleSize ** 0.5)
    
    random.shuffle(startState)
    print("A randomized Starting state: ")
    reshapePuzzle(startState)

    startTime = timeit.default_timer()
    results = SMA(startState, goalState)
    stopTime = timeit.default_timer()
    
    print("********    Result of SMA star    ********* ")
    if results:
        print("solution found! \n")
        print("path_to_goal: " + str(directions))
        print("\ncost_of_path: " + str(len(directions)))
    else:
        print("no solution found, time limit exceeded")	
    print("\ntime taken: ", stopTime - startTime, " seconds")


board_map = {
    '8Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8],
    '15Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
}


main()
