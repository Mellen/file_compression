LEFT = '1'
RIGHT = '0'

class Leaf():
    def __init__(self, data, value):
        self.data = data
        self.value = value
        self.parent = None
        self.code = ''

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def update_code(self, update):
        self.code = update + self.code

class Node():
    def __init__(self, left, right, value):
        self.value = value
        self.left = left
        self.right = right
        self.code = ''

        self.left.update_code(LEFT)
        self.right.update_code(RIGHT)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def update_code(self, update):
        self.code = update + self.code
        self.left.update_code(update)
        self.right.update_code(update)


def buildTree(byte_frequencies):
    tree = [Leaf(bf, bf[1]) for bf in byte_frequencies]

    leaves = []

    while len(tree) > 1:
        left, right = tree[:2]
        if type(left) is Leaf:
            leaves.append(left)
        if type(right) is Leaf:
            leaves.append(right)
        tree = tree[2:]
        node = Node(left, right, left.value + right.value)
        tree.append(node)
        tree = sorted(tree, key=lambda node: node.value)

    return leaves, tree[0]

