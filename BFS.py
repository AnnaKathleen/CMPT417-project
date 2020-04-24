from collections import deque
from node import Node

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0


def bfs(startState, goalState):
    unvisitedNodes = deque([Node(startState, None, None, 0)])
    exploredNodes = set()

    while unvisitedNodes:
        currNode = unvisitedNodes.popleft()
        exploredNodes.add(currNode.map)
        
        if currNode.node == goalState:
            directions = stepBack(startState,currNode.node)
            print("path_to_goal: " + str(directions))
            return None
        
        successors = getSuccessors(currNode)

        for nextNode in successors:
            if nextNode.map not in exploredNodes:
                unvisitedNodes.append(nextNode)
                exploredNodes.add(nextNode.map)
        
def getSuccessors(currNode):
    global num_nodes_expanded
    num_nodes_expanded += 1
    children = list()

    for i in range(1,5):
        newPosition = currNode.node[:]
        index = newPosition.index(0)
        if i == 1: # move the 0 up
            if index not in range(0, puzzle_side_len):
                tempState = newPosition[index - puzzle_side_len]
                newPosition[index - puzzle_side_len] = newPosition[index]
                newPosition[index] = tempState

        elif i == 2: # move the 0 down
            if index not in range(0, puzzle_side_len):
                tempState = newPosition[index - puzzle_side_len]
                newPosition[index - puzzle_side_len] = newPosition[index]
                newPosition[index] = tempState
        
        elif i == 3: # move the 0 left
            if index not in range(0, puzzle_side_len):
                tempState = newPosition[index - puzzle_side_len]
                newPosition[index - puzzle_side_len] = newPosition[index]
                newPosition[index] = tempState

        elif i == 4: # move the 0 right
            if index not in range(0, puzzle_side_len):
                tempState = newPosition[index - puzzle_side_len]
                newPosition[index - puzzle_side_len] = newPosition[index]
                newPosition[index] = tempState
        
        children.append(Node(newPosition,currNode,i,0))
    
    successors = [children for children in children if children.node]
    return successors


def stepBack(startNode,node):
    currNode = Node
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
    global puzzleSize, puzzle_side_len
    startState = [0,8,7,6,5,4,3,2,1]
    goalState = [0,1,2,3,4,5,6,7,8]
    puzzleSize = len(startState)
    puzzle_side_len = int(puzzleSize ** 0.5)
    print("he")
    bfs(startState, goalState)

main()
