from queue import LifoQueue
import queue
import numpy as np
import timeit
import random
import io
import argparse
import matplotlib.pyplot as plt 

global num_nodes_expanded
max_search_depth = 0
puzzleSize = 0
puzzle_side_len = 0
time_constraint = 10

eighttestset = [[5, 1, 7, 0, 8, 3, 6, 4, 2],[8, 7, 2, 3, 6, 1, 0, 5, 4],[4, 1, 7, 2, 0, 8, 5, 6, 3],[8, 5, 7, 6, 0, 4, 3, 2, 1],[2, 4, 7, 1, 6, 3, 5, 8, 0],[5, 1, 3, 6, 8, 7, 4, 0, 2],[6, 0, 4, 1, 5, 3, 7, 2, 8],[3, 6, 1, 2, 8, 4, 7, 5, 0],[3, 8, 7, 5, 6, 0, 4, 2, 1],[7, 8, 6, 5, 4, 0, 2, 3, 1]]
fifteentestset =  [[10, 2, 9, 0, 7, 6, 11, 12, 5, 13, 8, 14, 3, 4, 1], [5, 9, 0, 12, 14, 7, 6, 10, 11, 8, 1, 4, 2, 3, 13], [0, 6, 3, 11, 12, 7, 5, 4, 14, 2, 13, 10, 8, 1, 9], [6, 13, 2, 5, 9, 12, 8, 3, 1, 10, 14, 7, 0, 4, 11], [0, 3, 12, 8, 2, 4, 9, 11, 10, 13, 7, 14, 5, 1, 6], [5, 6, 14, 12, 2, 0, 3, 7, 8, 1, 10, 13, 11, 4, 9], [10, 3, 14, 13, 4, 1, 11, 6, 5, 0, 7, 2, 12, 9, 8], [0, 1, 10, 13, 11, 8, 7, 2, 9, 5, 4, 6, 3, 14, 12], [14, 7, 2, 3, 13, 9, 11, 8, 4, 5, 1, 10, 12, 0, 6], [1, 6, 0, 5, 7, 3, 14, 10, 11, 12, 13, 2, 9, 8, 4]]


class Node:
	def __init__(self,stateMat,parent,action,cost,depth):
		self.stateMat = stateMat
		self.parent = parent
		self.action = action
		self.cost = cost
		self.depth = depth

		if self.stateMat:
			self.ID = ''.join(str(locs) for locs in self.stateMat)


goal_node = Node 

def matStacker(mat):
	if len(mat) == 9:
		a = np.array(mat[0:3])
		b = np.array(mat[3:6])
		c = np.array(mat[6:10])
		d = np.stack((a,b,c))
		#print("stacked array is: \n", d)
		return d
	else: 
		a = np.array(mat[0:4])
		b = np.array(mat[4:8])
		c = np.array(mat[8:12])
		d = np.array(mat[12:16])
		e = np.stack((a,b,c,d))
		return e
'''
def findBlank(mat):
	s = matStacker(mat)
	for i in range(0,3):
		for j in range(0,3):
			if(s[i][j]==0):
				return i,j
'''
def getSuccessors(currNode):
    #global num_nodes_expanded
    #num_nodes_expanded += 1
    children = list()
    for i in range(1,5):
        newPosition = currNode.stateMat[:]
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
            children.append(Node(finalPosition,currNode,i,currNode.cost,currNode.depth))
        else:
            children.append(Node(newPosition,currNode,i,currNode.cost+1,currNode.depth+1))
    
    successors = [children for children in children if children.stateMat]
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

def DFID(initialState, goalTest, thisTime, iter):
	
	global goal_node, max_search_depth, num_nodes_expanded
	num_nodes_expanded = 0
	maximum_depth = 100

	for i in range(0, maximum_depth):
		depth_limit = i
		openList = LifoQueue()
		closedList = set()

		currNode = Node(initialState,None,0,0,0)
		openList.put(currNode)

		while not openList.empty():

			currTime = timeit.default_timer()
			if (currTime-thisTime) >= time_constraint:
				#time_acceptable = False
				return 0

			nodeNode = openList.get()
			closedList.add(nodeNode)

			if nodeNode.stateMat == goalTest:
				goal_node.put(nodeNode)
				return openList

			possibleStates = reversed(getSuccessors(nodeNode))

			for state in possibleStates:

				if state.depth > depth_limit:
					max_search_depth == depth_limit
				else:
					if state.ID not in closedList:
						openList.put(state)
						closedList.add(state.ID)
						num_nodes_expanded += 1


def export(initialstate, goalnode, elapsedTime, namefile):

    global tileMoves
    egoalnode = goalnode.get()
    eopenlist = initialstate
    i = namefile
    tileMoves = stepBack(eopenlist,egoalnode)
    #file = open("eightpDFID_{0}.txt".format(i), 'w')
    #file = open("namefile.txt", 'w')
    #file.write("path_to_goal: " + str(tileMoves))
    #file.write("\ncost_of_path: " + str(len(tileMoves)))
    #file.write("\nnum_nodes_expanded: " + str(num_nodes_expanded))
    #file.write("\n" + str(num_nodes_expanded))
    #file.write("\n" + str(egoalnode.depth))
    #file.write("\n" + format(elapsedTime, '.8f'))
    #file.write("\nsearch_depth: " + str(goal_node.depth))
    #file.write("\nrunning_time: " + format(elapsedTime, '.8f'))    
    #file.close()
    x_vals.append(num_nodes_expanded)
    y_vals.append(elapsedTime)

def genPuzzles(goaltemp):
	temp = goaltemp
	puzzleSize = len(goalState)
	randStart = []
	for each in range(0,10):
		randStart.append(random.sample(temp,puzzleSize))
	print("puzzles generated :\n", randStart)
	this_puzzleset = puzzleSet(randStart[0],randStart[1],randStart[2],randStart[3],randStart[4],randStart[5],randStart[6],randStart[7],randStart[8],randStart[9],)
	return randStart



def main():
	global puzzleSize, puzzle_side_len, puzzle_instances
	global startState, goalState, goal_node, num_nodes_expanded
	global start_time
	global time_acceptable 
	global x_vals, y_vals
	start = []
	stop = []
	results = []
	x_vals = []
	y_vals = []
	x_vals_fails = []
	y_vals_fails = []



	parser = argparse.ArgumentParser()
	parser.add_argument('board')
	args = parser.parse_args()
	board = board_map[args.board]

	startState = []
	if len(board) == 9:
		goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
		testset = eighttestset
		temp = goalState
	else:
		goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
		testset = fifteentestset
		temp = goalState
	
	randStart = []
	goal_node = queue.Queue()
	#puzzle_instances = genPuzzles(temp)
	puzzle_instances = testset
	puzzleSize = len(goalState)
	puzzle_side_len = int(puzzleSize ** 0.5)
	for each in range(0,len(puzzle_instances)):
		#randStart.append(random.sample(startState,puzzleSize))
		print("running DFID on puzzle :\n", puzzle_instances[each])
		#print("goal puzzle state is :\n", matStacker(goalState))
		start.append(timeit.default_timer())
		#results = DFID(startState, goalState, start[each], each)
		results = DFID(puzzle_instances[each], goalState, start[each], each)
		stop.append(timeit.default_timer())

		print("********    Result of DFID    ********* ")
		print("num nodes expanded were: \n", num_nodes_expanded)
		#print("time elapsed was: \n", stop-start)
		if results:
			export(puzzle_instances[each], goal_node, stop[each]-start[each], each)
			#export(startState,goal_node,stop[each]-start[each],each)
			print("solution found ! \n")
		else:
			print("no solution found :( ")
			x_vals_fails.append(num_nodes_expanded)
			y_vals_fails.append(stop[each]-start[each])	

	fig, ax = plt.subplots()
	plt.title("Results of DFID on 10 test instances of 8 puzzle")
	plt.ylabel("nodes expanded")
	plt.xlabel("time elapsed")
	ax.plot(y_vals,x_vals,'bo',label='sucessful search')
	ax.plot(y_vals_fails,x_vals_fails,'ro',label='failed search')
	legend = ax.legend(loc='lower right')
	plt.savefig('DFIDplot')

board_map = {
    '8Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8],
    '15Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
}

main()
