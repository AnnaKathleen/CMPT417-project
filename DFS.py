from collections import deque

class Node():
	def __init__(self,parent,stateMat,x_loc,y_loc,cost,depth):
		self.parent
		self.stateMat
		self.x_loc
		self.y_loc
		self.cost
		self.depth

		if self.stateMat:
			self.map = ''.join(str(locs) for locs in self.stateMat)

	def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map


def findBlank(mat):
	for i in range(0,N+1):
		for j in range(0,N+1):
			if(mat[i][j]==0):
				return x,y

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

def DFS(initialState, goalTest):
	
	global goal_node
	# max_search_depth, max_stack_size
	openList = deque()
	closedList = set()
	#this should be outside, before?
	x_origin,y_origin = findBlank(initialState)
	currNode = Node(None,initialState,x_origin,y_origin,0,0)
	
	openList.append(currNode)

	# if time_elapsed < time_constraint:
	# 	continue

	while not openList.empty():
		nodeNode = openList.pop()
		closedList.add(nodeNode)

		if nodeNode.stateMat == goalState:
			goal_node = nodeNode
			return openList

		possibleStates = reversed(getSuccessors(nodeNode))

		for state in possibleStates:
			if state.map not in closedList:
				openList.append(state)
				closedList.add(state.map)

		# 		if state.depth > max_search_depth:
		# 			max_search_depth += 1 #iterative deepening

		# if len(openList) > max_stack_size:
		# 	max_stack_size += 1
