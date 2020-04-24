from queue import LifoQueue
import numpy as np
import timeit

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0

class Node:
	def __init__(self,stateMat,parent,action,x_loc,y_loc,cost,depth):
		self.stateMat = stateMat
		self.parent = parent
		self.x_loc = x_loc
		self.y_loc = y_loc
		self.action = action
		self.cost = cost
		self.depth = depth

		if self.stateMat:
			self.map = ''.join(str(locs) for locs in self.stateMat)


def matStacker(mat):
	a = np.array(mat[0:3])
	b = np.array(mat[3:6])
	c = np.array(mat[6:10])
	d = np.stack((a,b,c))
	print("stacked array is: \n", d)
	return d

def findBlank(mat):
	s = matStacker(mat)
	for i in range(0,3):
		for j in range(0,3):
			if(s[i][j]==0):
				return i,j

def getSuccessors(currNode):
    global num_nodes_expanded
    num_nodes_expanded += 1
    children = list()
    for i in range(1,5):
        newPosition = currNode.stateMat[:]
        index = newPosition.index(0)
        noneTrue = False
        if i == 1: # move the 0 up
            if index not in range(0, puzzle_side_len):
            	#print("moving 0 up is out of range")
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
        #might be mistake here
        if noneTrue == True:
            children.append(Node(finalPosition,currNode,i,0,0,0,0))
        else:
            children.append(Node(newPosition,currNode,i,0,0,0,0))
            # print(children)
    
    successors = [children for children in children if children.stateMat]
    # print(successors)
    return successors


def stepBack(startNode,node):
    currNode = node
    directions = list()
    while  currNode.stateMat != startNode:
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
	openList = LifoQueue()
	closedList = set()
	#this should be outside, before?
	x_origin,y_origin = findBlank(initialState)
	currNode = Node(initialState,None,x_origin,y_origin,0,0,0)
	
	openList.put(currNode)

	# if time_elapsed < time_constraint:
	# 	continue

	while not openList.empty():
		nodeNode = openList.get()
		closedList.add(nodeNode)

		if nodeNode.stateMat == goalTest:
			goal_node = nodeNode
			return openList

		possibleStates = reversed(getSuccessors(nodeNode))

		for state in possibleStates:
			if state.map not in closedList:
				openList.put(state)
				closedList.add(state.map)

		# 		if state.depth > max_search_depth:
		# 			max_search_depth += 1 #iterative deepening

		# if len(openList) > max_stack_size:
		# 	max_stack_size += 1

def export(frontier, time):

    #global moves

    moves = stepBack(startState,goal_node)

    file = open('output.txt', 'w')
    file.write("path_to_goal: " + str(moves))
    file.write("\ncost_of_path: " + str(len(moves)))
    file.write("\nnum_nodes_expanded: " + str(num_nodes_expanded))
    #file.write("\nfringe_size: " + str(len(frontier)))
    #file.write("\nmax_fringe_size: " + str(max_frontier_size))
    file.write("\nsearch_depth: " + str(goal_node.depth))
    #file.write("\nmax_search_depth: " + str(max_search_depth))
    file.write("\nrunning_time: " + format(time, '.8f'))
    #file.write("\nmax_ram_usage: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.8f'))    
    file.close()

def main():
    global puzzleSize, puzzle_side_len
    global startState 
    startState = [1,2,0,3,4,5,6,7,8]
    goalState = [0,1,2,3,4,5,6,7,8]
    puzzleSize = len(startState)
    puzzle_side_len = int(puzzleSize ** 0.5)
    res = DFS(startState, goalState)
    
    start = timeit.default_timer()
    #frontier = function(initial_state)
    res = DFS(startState, goalState)
    stop = timeit.default_timer()

    #export(res, stop-start)
    print("result of DFS: ")
    if res:
    	export(res, stop-start)
    	unstacked = goal_node.stateMat
    	stacked = matStacker(unstacked)
    	print("goal state found : \n", stacked)
    else:
    	print("no solution found :( ")	

main()
