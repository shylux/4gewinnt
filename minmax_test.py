from minmax import *


class FourInARowMinMax(MinMax):

    def heuristic(self, node):
        print("Heuristic:", node)
        return node.state[-1]

    def expand_node(self, node):
        states = self.expand_state(node.state)
        node.children = [Node(state, node) for state in states]

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
print(minimax.minmax(5))