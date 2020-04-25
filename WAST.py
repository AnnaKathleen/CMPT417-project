from collections import deque
import timeit
from math import floor
from node import Node, reshapePuzzle
from heapq import heappush, heappop, heapify
import random
import argparse

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0
time_constraint = 15 # seconds
        
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
    # WEIGHTING FOR HEURISTIC
    W = 2
    for i in range(1, puzzleSize):
        sum += abs(currState.index(i) % puzzle_side_len - goalState.index(i) % puzzle_side_len) + abs(floor(currState.index(i)/puzzle_side_len) - floor(goalState.index(i)/puzzle_side_len))
    return W*sum

def WAST(startState, goalState):
    global directions
    visitedNodes = set()
    priorityQueue = list() # heap implemented as a priority Queue
    heapify(priorityQueue)
    heapDict = {} # dictionary of all the heaps

    heuristicValue = heuristic(startState, goalState)
    rootNode = Node(startState, None, None, 0, 0, heuristicValue)

    dictEntry = (heuristicValue, 0, rootNode) # holds the heuristicValue, action and current node as a tuple
    heappush(priorityQueue, dictEntry) # add the dictionary entry to the heap called priorityQueue
    heapDict[rootNode.ID] = dictEntry

    while priorityQueue:
        #print("PRIORITYQUEUE:", priorityQueue)
        #print("heapDICT:", heapDict)
        currNode = heappop(priorityQueue)
        visitedNodes.add(currNode[2].ID) # get the ID of the node from the node which is in index pos 2 of the dictEntry tuple
        
        if timeit.default_timer() >= time_constraint:
            return 0

        if currNode[2].node == goalState: # check if we have reached the goal node 
            directions = stepBack(startState,currNode[2]) # trace back steps to get directions on how to get from start state to the goal state
            # print("path_to_goal: " + str(directions))
            # print("cost_of_path: " + str(len(directions)))
            return priorityQueue
        
        successors = getSuccessors(currNode[2])

        for nextNode in successors:
            nextNode.heuristicValue = nextNode.cost + (heuristic(nextNode.node, goalState))
            dictEntry = (nextNode.heuristicValue, nextNode.action, nextNode)

            if nextNode.ID not in visitedNodes:
                heappush(priorityQueue, dictEntry)
                visitedNodes.add(nextNode.ID)
                heapDict[nextNode.ID] = dictEntry

            # updating the heap if the node is in the dictionary and its new 
            elif nextNode.ID in heapDict:
                if nextNode.heuristicValue < heapDict[nextNode.ID][2].heuristicValue:
                    tup = (heapDict[nextNode.ID][2].heuristicValue, heapDict[nextNode.ID][2].action, heapDict[nextNode.ID][2])
                    heuristicIndex = priorityQueue.index(tup)
                    priorityQueue[int(heuristicIndex)] = dictEntry
                    heapDict[nextNode.ID] = dictEntry
                    heapify(priorityQueue)
  

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
    results = WAST(startState, goalState)
    stopTime = timeit.default_timer()
    
    print("********    Result of WA*    ********* ")
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
