from queue import LifoQueue
import queue
import numpy as np
import timeit
import random
import io

global num_nodes_expanded
#num_nodes_expanded = 0
max_search_depth = 0
puzzleSize = 0
puzzle_side_len = 0
time_constraint = 10


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
			self.ID = ''.join(str(locs) for locs in self.stateMat)

goal_node = Node 

def matStacker(mat):
	a = np.array(mat[0:3])
	b = np.array(mat[3:6])
	c = np.array(mat[6:10])
	d = np.stack((a,b,c))
	#print("stacked array is: \n", d)
	return d

def findBlank(mat):
	s = matStacker(mat)
	for i in range(0,3):
		for j in range(0,3):
			if(s[i][j]==0):
				return i,j

def getSuccessors(currNode):
    #global num_nodes_expanded
    #num_nodes_expanded += 1
    children = list()
    for i in range(1,5):
        newPosition = currNode.stateMat[:]
        #nindex = findBlank(newPosition)
        #print("newPosition is ", newPosition)
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
        if noneTrue == True: # I might have made mistake here creating new nodes, depth calc off
            children.append(Node(finalPosition,currNode,i,0,0,currNode.cost,currNode.depth))
        else:
            children.append(Node(newPosition,currNode,i,0,0,currNode.cost+1,currNode.depth+1))
            # print(children)
    
    successors = [children for children in children if children.stateMat]
    # print(successors)
    return successors


def stepBack(startNode,node):
    currNode = node
    directions = list()
    while  currNode.stateMat != startNode:
        if currNode.action == 1:
            currAction = 'Up'
        elif currNode.action == 2:
            currAction = 'Down'
        elif currNode.action == 3:
            currAction = 'Left'
        else:
            currAction = 'Right'
        
        directions.append(currAction)
        currNode = currNode.parent
    return directions

def DFS(initialState, goalTest, thisTime, iter):
	
	global goal_node, max_search_depth, num_nodes_expanded
	num_nodes_expanded = 0
	openList = LifoQueue()
	closedList = set()
	#might not need this
	x_origin,y_origin = findBlank(initialState)
	currNode = Node(initialState,None,x_origin,y_origin,0,0,0)
	
	openList.put(currNode)

	while not openList.empty():
		
		currTime = timeit.default_timer()
		if (currTime-thisTime) >= time_constraint:
			#time_acceptable = False
			#break
			return 0	
		
		nodeNode = openList.get()
		closedList.add(nodeNode)
		

		if nodeNode.stateMat == goalTest:
			goal_node.put(nodeNode)
			return openList

		possibleStates = reversed(getSuccessors(nodeNode))

		for state in possibleStates:
			if state.ID not in closedList:
				openList.put(state)
				closedList.add(state.ID)
				num_nodes_expanded += 1

			if state.depth > max_search_depth:
				max_search_depth += 1


def export(initialstate, goalnode, elapsedTime, namefile):

    global tileMoves
    egoalnode = goalnode.get()
    eopenlist = initialstate
    i = namefile
    tileMoves = stepBack(eopenlist,egoalnode)
    file = open("eightpdfs_{0}.txt".format(i), 'w')
    #file = open("namefile.txt", 'w')
    file.write("path_to_goal: " + str(tileMoves))
    #file.write("\ncost_of_path: " + str(len(tileMoves)))
    #file.write("\nnum_nodes_expanded: " + str(num_nodes_expanded))
    file.write("\n" + str(num_nodes_expanded))
    file.write("\n" + str(egoalnode.depth))
    file.write("\n" + format(elapsedTime, '.8f'))
    #file.write("\nsearch_depth: " + str(goal_node.depth))
    #file.write("\nrunning_time: " + format(elapsedTime, '.8f'))    
    file.close()

def main():
	global puzzleSize, puzzle_side_len
	global startState, goalState, goal_node, num_nodes_expanded
	global start_time
	global time_acceptable 
	start = []
	stop = []
	results = []

	startState = [3,1,2,0,4,5,6,7,8]
	goalState = [0,1,2,3,4,5,6,7,8]
	randStart = []
	goal_node = queue.Queue()

	puzzleSize = len(startState)
	puzzle_side_len = int(puzzleSize ** 0.5)
	for each in range(0,4):
		randStart.append(random.sample(startState,puzzleSize))
		print("running dfs on puzzle :\n", matStacker(randStart[each]))
		print("goal puzzle state is :\n", matStacker(goalState))
		start.append(timeit.default_timer())
		#results = DFS(startState, goalState, start[each], each)
		results = DFS(randStart[each], goalState, start[each], each)
		stop.append(timeit.default_timer())

		print("********    Result of DFS    ********* ")
		print("nodes expanded were: \n", num_nodes_expanded)
		#print("time elapsed was: \n", stop-start)
		if results:
			export(randStart[each], goal_node, stop[each]-start[each], each)
			#export(startState,goal_node,stop[each]-start[each],each)
			print("solution found ! \n")
		else:
			print("no solution found :( ")	

main()
