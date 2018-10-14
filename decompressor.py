import pickle
import sys

class Decompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            filename_length = int.from_bytes(compressed_file.read(4), sys.byteorder)
            filename = compressed_file.read(filename_length).decode('utf-8')
            sbl = int.from_bytes(compressed_file.read(4), sys.byteorder)
            print(sbl)
            sorted_chars = compressed_file.read(sbl).decode('utf-8')
            frequencies = {'0'*i:c for i, c in enumerate(sorted_chars)}
            print(frequencies)
            dl = int.from_bytes(compressed_file.read(16), sys.byteorder)
            data = int.from_bytes(compressed_file.read(dl), sys.byteorder)

        with open(filename, 'w') as textfile:
            output = ''
            full_binary = bin(data)[3:].split('1')
            for n in full_binary:
                output += frequencies[n]
            textfile.write(output)
                
