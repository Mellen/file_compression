import sys
import os
from math import ceil
from binarytree import buildTree

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

        leaves, _ = buildTree(bytes_frequency)

        symbol_map = {leaf.data[0]:leaf.code for leaf in leaves}

        output_bits = '1'
        for b in all_bytes:
            output_bits = output_bits + symbol_map[b]

        byte_count = (len(output_bits)+7) // 8

        output_int = int(output_bits, 2)

        output_bytes = output_int.to_bytes(byte_count, sys.byteorder)

        max_count_bytes = ceil(leaves[-1].data[1].bit_length()/8)

        header_bytes = len(leaves).to_bytes(2, sys.byteorder)
        header_bytes += max_count_bytes.to_bytes(8, sys.byteorder)

        for leaf in leaves:
            header_bytes += (leaf.data[0].to_bytes(1, sys.byteorder))
            header_bytes += leaf.data[1].to_bytes(max_count_bytes, sys.byteorder)

        with open(self.outputname, 'wb') as out_file:
            out_file.write(header_bytes)
            out_file.write(output_bytes)

        print('end length', len(output_bytes) + len(header_bytes))

    def getFrequencies(self, all_bytes):
        byte_set = set(all_bytes)

        bytes_frequency_dict = {b:0 for b in byte_set}

        for b in all_bytes:
            bytes_frequency_dict[b] = bytes_frequency_dict[b] + 1

        return sorted([item for item in bytes_frequency_dict.items()], key=lambda item:item[1])

        
