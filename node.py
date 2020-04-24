class Node:
    def __init__(self, node, parent, action, movingPiece, cost, key):
        self.node = node
        self.parent = parent
        self.action = action
        self.movingPiece = movingPiece
        self.cost = cost
        self.key = key

        # create a unique Identifier for each node created
        if self.node:
            self.ID = ''.join(str(s) for s in self.node)

    # overloaded the equal and less than operator to work with nodes 
    # taken from https://www.geeksforgeeks.org/operator-overloading-in-python/
    def __eq__(self, other):
        return self.ID == other.ID

    def __lt__(self, other):
        return self.ID < other.ID