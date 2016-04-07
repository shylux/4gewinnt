import sys


class Node(object):

    state = None
    children = []
    max_node = False
    parent = None

    def __init__(self, state, parent=None):
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

    def expand_node(self, state):
        raise NotImplementedError()

    def minmax(self, max_depth, node=None, alpha=-sys.maxsize, beta=sys.maxsize):
        if not node:
            node = self.root

        if max_depth == 0:  # leaf node
            return self.heuristic(node)
        max_depth -= 1

        if len(node.children) == 0:
            self.expand_node(node)

        if len(node.children) == 0:
            node.value = self.heuristic(node)
            return node.value

        node.value = -sys.maxsize if node.max_node else sys.maxsize  # initialize with worst value
        for child in node.children:
            child_value = self.minmax(max_depth, child, alpha, beta)
            if node.max_node:
                node.value = max(node.value, child_value)
                alpha = node.value
                if alpha > beta:  # check for pruning
                    break
            else:
                node.value = min(node.value, child_value)
                beta = node.value
                if beta < alpha:
                    break

        # sort for optimization
        node.children.sort(key=lambda n: -getattr(n, "value", sys.maxsize))
        if not node.max_node:
            node.children = list(reversed(node.children))

        return node.value
