class Leaf():
    def __init__(self, data, value):
        self.data = data
        self.value = value

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

class Node():
    def __init__(self, left, right, value):
        self.value = value
        self.left = left
        self.right = right
        
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()

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
