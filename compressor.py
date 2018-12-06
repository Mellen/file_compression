import sys
import os
from binarytree import Leaf, Node, printTree, LEFT, RIGHT

class TextCompressor():
    def __init__(self, filename):
        self.filename = filename
        self.outputname = filename+'.tc'

    def compress(self):
        with open(self.filename, 'r') as textfile:
            text = textfile.read()

        chars = ''.join(set(text))

        data = self.text_to_data(text, chars)
        
        with open(self.outputname, 'wb') as compressed_file:
            filename_bytes = os.path.basename(self.filename).encode('utf-8')
            compressed_file.write((len(filename_bytes)).to_bytes(4, sys.byteorder))
            compressed_file.write(filename_bytes)
            char_bytes = chars.encode('utf-8')
            compressed_file.write((len(char_bytes)).to_bytes(4, sys.byteorder))
            compressed_file.write(char_bytes)
            bit_length = len(chars).bit_length()
            compressed_file.write(bit_length.to_bytes(4, sys.byteorder))
            compressed_file.write((len(data)).to_bytes(4, sys.byteorder))
            for datum in data:
                compressed_file.write(datum.to_bytes(8, sys.byteorder))

    def text_to_data(self, text, chars):
        bl = len(chars).bit_length()
        max_inserts = 64//bl;
        current_insert = 0
        value = ''
        values = []
        for c in text:
            n = chars.index(c) + 1
            b = (bin(n)[2:]).zfill(bl)
            value += b
            current_insert += 1
            if current_insert == max_inserts:
                values.append(int(value, 2))
                current_insert = 0
                value = ''

        if current_insert < max_inserts and current_insert > 0:
            values.append(int(value, 2))

        return values


class BinaryCompressor():

    def __init__(self, filename):
        self.filename = filename
        self.outputname = filename + '.bc'

    def compress(self):
        all_bytes = []
        with open(self.filename, 'rb') as binaryfile:
            all_bytes = binaryfile.read()

        print('start length', len(all_bytes))

        bytes_frequency = self.getFrequencies(all_bytes)
        
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
            
        symbol_map = {leaf.data[0]:leaf.code for leaf in leaves}

        output_bits = '1'
        for b in all_bytes:
            output_bits = output_bits + symbol_map[b]

        byte_count = (len(output_bits)+7) // 8

        output_int = int(output_bits, 2)

        output_bytes = output_int.to_bytes(byte_count, sys.byteorder)

        print(symbol_map)
        print('end length', len(output_bytes))        

    def getFrequencies(self, all_bytes):
        byte_set = set(all_bytes)

        bytes_frequency_dict = {b:0 for b in byte_set}

        for b in all_bytes:
            bytes_frequency_dict[b] = bytes_frequency_dict[b] + 1
        
        return sorted([item for item in bytes_frequency_dict.items()], key=lambda item:item[1])

        
