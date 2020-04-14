from node import Node
from collections import deque

def getSuccessors(node):



def BFS(startState, goalState):
    print("searching for solution with BFS\n")
    visited, frontier = set(), deque([Node(startState, None, None, 0,0,0)])

    while frontier:
        currNode = frontier.popleft()
        visited.add(currNode.map)

        if currNode.node = goalState:
            goal = currNode
            return frontier