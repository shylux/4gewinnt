class Node(object):

    state = None
    children = []

    def __init__(self, state):
        self.state = state

    def __repr__(self):
        if len(self.children) == 0:
            return str(self.state)
        else:
            return "(" + ", ".join([str(child) for child in self.children]) + ")"


def minmax(root_state, max_depth, expand_state, rate_state):
    max_depth -= 1



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
