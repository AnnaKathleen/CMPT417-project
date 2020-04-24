class Node:
    def __init__(self, node, parent, action, movingPiece, cost, key):
        self.node = node
        self.parent = parent
        self.action = action
        self.movingPiece = movingPiece
        self.cost = cost
        self.key = key

        if self.node:
            self.map = ''.join(str(s) for s in self.node)