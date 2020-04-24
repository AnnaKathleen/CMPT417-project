from collections import deque
from node import Node, reshapePuzzle
import argparse
import timeit
import random

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0
time_constraint = 15 # seconds

def BFS(startState, goalState):
    global directions
    unvisitedNodes = deque([Node(startState, None, None, 0,0,0)])
    exploredNodes = set()

    while unvisitedNodes:
        currNode = unvisitedNodes.popleft()
        exploredNodes.add(currNode.ID)
        
        if timeit.default_timer() >= time_constraint:
            return 0

        if currNode.node == goalState:
            directions = stepBack(startState,currNode)
            return unvisitedNodes
        
        successors = getSuccessors(currNode)

        for nextNode in successors:
            if nextNode.ID not in exploredNodes:
                unvisitedNodes.append(nextNode)
                exploredNodes.add(nextNode.ID)
        
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
            children.append(Node(finalPosition,currNode,i,0,0,0))
        else:
            children.append(Node(newPosition,currNode,i,0,0,0))
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

def main():
    global puzzleSize, puzzle_side_len, time_constraint

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
    results = BFS(startState, goalState)
    stopTime = timeit.default_timer()
    
    print("********    Result of BFS    ********* ")
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
