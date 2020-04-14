class Node:

    def __init__(self, node, parent, move, depth, cost, key):
        self.node = node
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.key = key

        if self.node:
            self.map = ''.join(str(s) for s in self.node)

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
