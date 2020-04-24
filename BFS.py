from node import Node
from collections import deque

nodes_expanded = 0
max_search_depth = 0
max_frontier_size = 0

def getSuccessors(node):

    global nodes_expanded
    nodes_expanded += 1

    neighbors = list()

    neighbors.append(Node(move(node.node, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(Node(move(node.node, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(Node(move(node.node, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(Node(move(node.node, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = [neighbor for neighbor in neighbors if neighbor.node]

    return nodes

def move(node, position):

    new_node = node[:]

    index = new_node.index(0)

    if position == 1:  # Up

        if index not in range(0, board_side):

            temp = new_node[index - board_side]
            new_node[index - board_side] = new_node[index]
            new_node[index] = temp

            return new_node
        else:
            return None

    if position == 2:  # Down

        if index not in range(board_len - board_side, board_len):

            temp = new_node[index + board_side]
            new_node[index + board_side] = new_node[index]
            new_node[index] = temp

            return new_node
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, board_len, board_side):

            temp = new_node[index - 1]
            new_node[index - 1] = new_node[index]
            new_node[index] = temp

            return new_node
        else:
            return None

    if position == 4:  # Right

        if index not in range(board_side - 1, board_len, board_side):

            temp = new_node[index + 1]
            new_node[index + 1] = new_node[index]
            new_node[index] = temp

            return new_node
        else:
            return None

def BFS(startState, goalState):
    print("searching for solution with BFS\n")
    startState = startState.ravel()
    goalState = goalState.ravel()
    goal = Node
    visited, frontier = set(), deque([Node(startState, None, None, 0,0,0)])

    while frontier:
        currNode = frontier.popleft()
        visited.add(currNode.map)

        if currNode.node == goalState:
            goal = currNode
            return frontier
        
        successors = getSuccessors(currNode)

        for nextNode in successors:
            if nextNode.map not in visited:
                frontier.append(nextNode)
                visited.add(nextNode)
                if nextNode > max_search_depth:
                    max_search_depth += 1

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

