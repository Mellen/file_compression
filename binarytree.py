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


def buildTree(bytes_frequency):
    tree = [Leaf(bf, bf[1]) for bf in bytes_frequency]

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


def printTree(root):
    layers = [[root]]
    done = False
    
    while not done:
        last_layer = layers[-1]
        layer = []
        for node in last_layer:
            if type(node) is Node:
                layer.append(node.left)
                layer.append(node.right)
        done = len(layer) == 0
        if not done:
            layers.append(layer)

    for i, layer in enumerate(layers):
        layers[i] = list(map(lambda node: ' '*len(str(node)) + str(node), layer))
    space_count = sum(map(lambda s: len(s), layers[-1]))//2

    string = ''
    
    for layer in layers:
        spaces = ' '*space_count
        space_count = space_count//2
        string = string + spaces + spaces.join(layer)
        string = string + '\n'

    print(string)
