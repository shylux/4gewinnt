from sys import maxsize


class Node(object):

    state = None
    children = []
    max_node = False
    parent = None

    def __init__(self, parent, state):
        self.parent = parent
        self.max_node = not parent.max_node
        self.state = state

    def __repr__(self):
        if len(self.children) == 0:
            return str(self.state)
        else:
            return "(" + ", ".join([str(child) for child in self.children]) + ")"


class MinMax(object):

    root = None

    def heuristic(self, state):
        raise NotImplementedError()

    def expand_state(self, state):
        raise NotImplementedError()

    def minimax(self, max_depth, node, alpha=0, beta=0):
        max_depth -= 1

        if not node:
            node = self.root

        if max_depth == 0:  # leaf node
            return self.heuristic(node.state)

        if len(node.children) == 0:
            states = self.expand_state(node.state)
            node.children = [Node(node, state) for state in states]

        values = dict()
        for child in node.children:
            values[child] = self.minimax(child)

        value = max(values) if node.max_node else min(values)



testdata = [10, 11, 9, 12, 14, 15, 13, 14, 5, 2, 4, 1, 3, 22, 20, 21]


def expand_tree(node):
    if len(node.state) > 1:
        n1 = Node(node.state[:len(node.state)/2])
        expand_tree(n1)
        n2 = Node(node.state[len(node.state)/2:])
        expand_tree(n2)
        node.children = [n1, n2]
        node.state = None
    else:
        node.state = node.state[0]

root = Node(testdata)
expand_tree(root)
# import pdb;pdb.set_trace()
print root
