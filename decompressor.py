import pickle
import sys

class Decompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            filename_length = int.from_bytes(compressed_file.read(4), sys.byteorder)
            filename = compressed_file.read(filename_length).decode('utf-8')
            fl = int.from_bytes(compressed_file.read(4), sys.byteorder)
            frequencies = pickle.loads(compressed_file.read(fl))
            print(frequencies)
            dl = int.from_bytes(compressed_file.read(16), sys.byteorder)
            data = int.from_bytes(compressed_file.read(dl), sys.byteorder)

        with open(filename, 'w') as textfile:
            output = ''
            reverse_lookup = {frequencies[key]:key for key in frequencies}
            full_binary = bin(data)[3:].split('1')
            for n in full_binary:
                output += reverse_lookup[n]
            textfile.write(output)
                
