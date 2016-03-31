from sys import maxsize


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

    def minimax(self, max_depth, node=None, alpha=0, beta=0):
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

        values = []
        for child in node.children:
            values.append(self.minimax(max_depth, child))

        value = max(values) if node.max_node else min(values)
        return value


class FourInARowMinMax(MinMax):

    def heuristic(self, node):
        print("Heuristic:", node)
        return node.state[-1]

    def expand_state(self, state):
        print("Expand:", state)
        if len(state) > 1:
            s1 = state[:int(len(state)/2)]
            s2 = state[int(len(state)/2):]
            return [s1, s2]
        return []


testdata = [10, 11, 9, 12, 14, 15, 13, 14, 5, 2, 4, 1, 3, 22, 20, 21]

root = Node(testdata)
root.max_node = True

print(root)
minimax = FourInARowMinMax()
minimax.root = root
print(minimax.minimax(5))
