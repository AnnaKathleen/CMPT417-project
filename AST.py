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
    sum = 0
    for i in range(1, puzzleSize):
        sum += abs(currState.index(i) % puzzle_side_len - goalState.index(i) % puzzle_side_len) + abs(currState.index(i)//puzzle_side_len - goalState.index(i)//puzzle_side_len)
    # print(sum)
    return sum

def ast(startState, goalState):
    visitedNodes = set()
    priorityQueue = list() # heap implemented as a priority Queue
    heapDict = {}

    key = heuristic(startState, goalState)
    root = Node(startState, None, None, 0, 0, key)
    dictEntry = (key, 0, root) # holds the key, action and current node as a tuple
    heappush(priorityQueue, dictEntry) # add the dictionary entry to the heap called priorityQueue
    heapDict[root.map] = dictEntry

    while priorityQueue:
        currNode = heappop(priorityQueue)
        visitedNodes.add(currNode[2].map) # get the map of the node from the node which is in index pos 2 of the dictEntry tuple
        
        if currNode[2].node == goalState: # check if we have reached the goal node 
            directions = stepBack(startState,currNode[2]) # trace back steps to get directions on how to get from start state to the goal state
            print("path_to_goal: " + str(directions))
            print("cost_of_path: " + str(len(directions)))
            return None
        
        successors = getSuccessors(currNode[2])

        for nextNode in successors:
            nextNode.key = nextNode.cost + heuristic(nextNode.node, goalState)
            dictEntry = (nextNode.key, nextNode.action, nextNode)

            if nextNode.map not in visitedNodes:
                heappush(priorityQueue, dictEntry)
                visitedNodes.add(nextNode.map)
                heapDict[nextNode.map] = dictEntry
            

        


def main():
    global puzzleSize, puzzle_side_len
    startState = [0,8,7,6,5,4,3,2,1]
    goalState = [0,1,2,3,4,5,6,7,8]
    puzzleSize = len(startState)
    puzzle_side_len = int(puzzleSize ** 0.5)
    ast(startState, goalState)

main()
