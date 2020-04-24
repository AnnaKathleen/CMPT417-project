class Node:
    def __init__(self, node, parent, action, movingPiece):
        self.node = node
        self.parent = parent
        self.action = action
        self.movingPiece = movingPiece

        if self.node:
            self.map = ''.join(str(s) for s in self.node)