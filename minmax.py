import sys


class Node(object):

    state = None
    children = []
    max_node = False
    parent = None

    def __init__(self, state, parent=None):
        self.parent = parent
        if parent:
            self.max_node = not parent.max_node
        self.state = state

    def __repr__(self):
        if len(self.children) == 0:
            return str(self.state)
        else:
            return "(" + ", ".join([str(child) for child in self.children]) + ")"


class MinMax(object):

    root = None

    def heuristic(self, node):
        raise NotImplementedError()

    def expand_state(self, state):
        raise NotImplementedError()

    def minmax(self, max_depth, node=None, alpha=-sys.maxsize, beta=sys.maxsize):
        max_depth -= 1

        if not node:
            node = self.root

        if max_depth == 0:  # leaf node
            return self.heuristic(node)

        if len(node.children) == 0:
            states = self.expand_state(node.state)
            node.children = [Node(state, node) for state in states]

        if len(node.children) == 0:
            return self.heuristic(node)

        value = -sys.maxsize if node.max_node else sys.maxsize  # initialize with worst value
        for child in node.children:
            child_value = self.minmax(max_depth, child, alpha, beta)
            if node.max_node:
                value = max(value, child_value)
                alpha = value
                if value > beta:  # check for pruning
                    return value
            else:
                value = min(value, child_value)
                beta = value
                if value < alpha:
                    return value

        return value
