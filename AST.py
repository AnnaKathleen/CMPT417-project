from collections import deque
from node import Node
from heapq import heappush, heappop, heapify

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

    # keys are the indices of thew array and the tuples represent the position in the grid above
    grid = {
        0: (0,0),
        1: (1,0),
        2: (2,0),
        3: (0,1),
        4: (1,1),
        5: (2,1),
        6: (0,2),
        7: (1,2),
        8: (2,2)
    }
    sum = 0
    for i in range(1, puzzleSize):
        currPos = grid[i]
        goalPos = grid[currState[i]]
        sum += abs(currPos[0] - goalPos[0]) + abs(currPos[1] - goalPos[1])
    return sum

def ast(startState, goalState):
    visitedNodes = set()
    priorityQueue = list() # heap implemented as a priority Queue
    heapify(priorityQueue)
    heapDict = {} # dictionary of all the heaps

    heuristicValue = heuristic(startState, goalState)
    input()
    rootNode = Node(startState, None, None, 0, 0, heuristicValue)

    dictEntry = (heuristicValue, 0, rootNode) # holds the heuristicValue, action and current node as a tuple
    heappush(priorityQueue, dictEntry) # add the dictionary entry to the heap called priorityQueue
    heapDict[rootNode.ID] = dictEntry

    while priorityQueue:
        currNode = heappop(priorityQueue)
        visitedNodes.add(currNode[2].ID) # get the ID of the node from the node which is in index pos 2 of the dictEntry tuple
        
        if currNode[2].node == goalState: # check if we have reached the goal node 
            directions = stepBack(startState,currNode[2]) # trace back steps to get directions on how to get from start state to the goal state
            print("path_to_goal: " + str(directions))
            print("cost_of_path: " + str(len(directions)))
            return None
        
        successors = getSuccessors(currNode[2])

        for nextNode in successors:
            nextNode.heuristicValue = nextNode.cost + heuristic(nextNode.node, goalState)
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
    startState = [0,8,7,6,5,4,3,2,1]
    goalState = [0,1,2,3,4,5,6,7,8]
    puzzleSize = len(startState)
    puzzle_side_len = int(puzzleSize ** 0.5)
    ast(startState, goalState)

main()
