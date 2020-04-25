from collections import deque
from node import Node, reshapePuzzle
import argparse
import timeit
import random
import matplotlib.pyplot as plt 

num_nodes_expanded = 0
puzzleSize = 0
puzzle_side_len = 0
time_constraint = 60 # seconds
eighttestset = [[5, 1, 7, 0, 8, 3, 6, 4, 2],[8, 7, 2, 3, 6, 1, 0, 5, 4],[4, 1, 7, 2, 0, 8, 5, 6, 3],[8, 5, 7, 6, 0, 4, 3, 2, 1],[2, 4, 7, 1, 6, 3, 5, 8, 0],[5, 1, 3, 6, 8, 7, 4, 0, 2],[6, 0, 4, 1, 5, 3, 7, 2, 8],[3, 6, 1, 2, 8, 4, 7, 5, 0],[3, 8, 7, 5, 6, 0, 4, 2, 1],[7, 8, 6, 5, 4, 0, 2, 3, 1]]
fifteentestset =  [[10, 2, 9, 0, 7, 6, 11, 12, 5, 13, 8, 14, 3, 4, 1], [5, 9, 0, 12, 14, 7, 6, 10, 11, 8, 1, 4, 2, 3, 13], [0, 6, 3, 11, 12, 7, 5, 4, 14, 2, 13, 10, 8, 1, 9], [6, 13, 2, 5, 9, 12, 8, 3, 1, 10, 14, 7, 0, 4, 11], [0, 3, 12, 8, 2, 4, 9, 11, 10, 13, 7, 14, 5, 1, 6], [5, 6, 14, 12, 2, 0, 3, 7, 8, 1, 10, 13, 11, 4, 9], [10, 3, 14, 13, 4, 1, 11, 6, 5, 0, 7, 2, 12, 9, 8], [0, 1, 10, 13, 11, 8, 7, 2, 9, 5, 4, 6, 3, 14, 12], [14, 7, 2, 3, 13, 9, 11, 8, 4, 5, 1, 10, 12, 0, 6], [1, 6, 0, 5, 7, 3, 14, 10, 11, 12, 13, 2, 9, 8, 4]]

def BFS(startState, goalState):
    global directions
    unvisitedNodes = deque([Node(startState, None, None, 0,0,0)])
    exploredNodes = set()

    while unvisitedNodes:
        currNode = unvisitedNodes.popleft()
        exploredNodes.add(currNode.ID)
        
        if timeit.default_timer() >= time_constraint:
            return 0

        if currNode.node == goalState:
            directions = stepBack(startState,currNode)
            return unvisitedNodes
        
        successors = getSuccessors(currNode)

        for nextNode in successors:
            if nextNode.ID not in exploredNodes:
                unvisitedNodes.append(nextNode)
                exploredNodes.add(nextNode.ID)
        
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
            children.append(Node(finalPosition,currNode,i,0,0,0))
        else:
            children.append(Node(newPosition,currNode,i,0,0,0))
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

def outputUtil(initialstate, goalnode, elapsedTime, namefile):

    global tileMoves
    egoalnode = goalnode.get()
    eopenlist = initialstate
    i = namefile
    tileMoves = stepBack(eopenlist,egoalnode)
  # optional utils to write output to files numbered by each instance where successful
    #file = open("eightpdfs_{0}.txt".format(i), 'w')
    #file.write("Tile moves (path to goal): " + str(tileMoves))
    #file.write("\npast cost: " + str(len(tileMoves)))
    #file.write("\nnumber of nodes expanded: " + str(num_nodes_expanded))
    #file.write("\ndepth of search: " + str(egoalnode.depth))
    #file.write("\nrun time of search: " + format(elapsedTime, '.8f'))    
    #file.close()
    x_vals.append(num_nodes_expanded)
    y_vals.append(elapsedTime)

def main():
	global puzzleSize, puzzle_side_len, time_constraint, x_vals, y_vals
	x_vals = []
	y_vals = []
	x_vals_fails = []
	y_vals_fails = []

	parser = argparse.ArgumentParser()
	parser.add_argument('board')
	args = parser.parse_args()
	board = board_map[args.board]

	startState = board
	if len(board) == 9:
		goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
		testset = eighttestset
	else:
		goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
		testset = fifteentestset

	puzzleSize = len(startState)
	puzzle_side_len = int(puzzleSize ** 0.5)
	puzzle_instances = testset
	#random.shuffle(startState)
	#print("A randomized Starting state: ")
	for each in range(0,len(puzzle_instances)):
		startState = testset[each]
		reshapePuzzle(startState)
		print("running bfs on puzzle: \n", startState)
		startTime = timeit.default_timer()
		results = BFS(startState, goalState)
		stopTime = timeit.default_timer()

		print("********    Result of BFS    ********* ")
		if results:
			print("solution found! \n")
			print("path_to_goal: " + str(directions))
			print("\ncost_of_path: " + str(len(directions)))
			outputUtil(puzzle_instances[each], results.pop(), stopTime-startTime, each)
		else:
			print("no solution found, time limit exceeded")
			x_vals_fails.append(num_nodes_expanded)
			y_vals_fails.append(stopTime-startTime)		
	#print("\ntime taken: ", stopTime - startTime, " seconds")
	fig, ax = plt.subplots()
	plt.title("Results of BFS on 10 test instances of 8 puzzle")
	plt.ylabel("nodes expanded")
	plt.xlabel("time elapsed")
	ax.plot(y_vals,x_vals,'bo',label='sucessful search')
	ax.plot(y_vals_fails,x_vals_fails,'ro',label='failed search')
	legend = ax.legend(loc='lower right')
	plt.savefig('bfsplot')

board_map = {
    '8Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8],
    '15Puzzle' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
}


main()
