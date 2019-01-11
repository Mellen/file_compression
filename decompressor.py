import sys
from binarytree import buildTree, LEFT, Leaf

class TextDecompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            filename, data, chars, bit_length = self.readfile(compressed_file)

        with open(filename, 'w') as textfile:
            output = ''
            expected_length = (64 // bit_length)*bit_length
            for value in data:
                b = bin(value)[2:]
                b = b.zfill(expected_length)
                while len(b) >= bit_length:
                    chunk = b[:bit_length]
                    b = b[bit_length:]
                    key = int(chunk, 2)
                    if key > 0:
                        output += chars[key-1]

            textfile.write(output)

    def readfile(self, file_obj):
        filename_length = int.from_bytes(file_obj.read(4), sys.byteorder)
        filename = file_obj.read(filename_length).decode('utf-8')
        cbl = int.from_bytes(file_obj.read(4), sys.byteorder)
        chars = file_obj.read(cbl).decode('utf-8')
        bit_length = int.from_bytes(file_obj.read(4), sys.byteorder)
        dl = int.from_bytes(file_obj.read(4), sys.byteorder)
        data = []
        current_bytes = file_obj.read(8)
        while current_bytes:
            datum = int.from_bytes(current_bytes, sys.byteorder)
            data.append(datum)
            current_bytes = file_obj.read(8)

        return (filename, data, chars, bit_length)


class BinaryDecompressor():
    def __init__(self, filename):
        self.filename = filename
        self.outputname = '.'.join(filename.split('.')[:-1])

    def decompress(self):
        input_bytes, byte_frequencies = self.readFile()
        _, tree = buildTree(byte_frequencies)
        input_bits = bin(int.from_bytes(input_bytes, sys.byteorder))[3:]
        output_bytes = b''
        current_node = tree
        for bit in input_bits:
            if bit == LEFT:
                current_node = current_node.left
            else:
                current_node = current_node.right

            if type(current_node) is Leaf:
                output_bytes += current_node.data[0]
                current_node = tree

        with open(self.outputname, 'wb') as output_file:
            output_file.write(output_bytes)

    def readFile(self):
        byte_frequencies = []
        input_bytes = None
        with open(self.filename, 'rb') as input_file:
            leaves_count = int.from_bytes(input_file.read(2), sys.byteorder)
            max_count_bytes = int.from_bytes(input_file.read(8), sys.byteorder)
            while leaves_count > 0:
                b = input_file.read(1)
                c = int.from_bytes(input_file.read(max_count_bytes), sys.byteorder)
                byte_frequencies.append((b,c))
                leaves_count -= 1
            input_bytes = input_file.read()
        return input_bytes, byte_frequencies
