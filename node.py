class Node:
    def __init__(self, node, parent, move, depth, cost, key):

        self.state = node

        self.parent = parent

        self.move = move

        self.depth = depth

        self.cost = cost

        self.key = key

        if self.state:
            self.map = ''.join(str(s) for s in self.node)