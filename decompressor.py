import pickle
import sys

class Decompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            filename_length = int.from_bytes(compressed_file.read(4), sys.byteorder)
            filename = compressed_file.read(filename_length).decode('utf-8')
            ul = int.from_bytes(compressed_file.read(4), sys.byteorder)
            print('ul', ul)
            uniques = pickle.loads(compressed_file.read(ul))
            bit_length = int.from_bytes(compressed_file.read(4), sys.byteorder)
            dl = int.from_bytes(compressed_file.read(4), sys.byteorder)
            data = []
            current_bytes = compressed_file.read(8)
            while current_bytes:
                datum = int.from_bytes(current_bytes, sys.byteorder)
                data.append(datum)
                current_bytes = compressed_file.read(8)

        with open(filename, 'w') as textfile:
            output = ''
            reverse_lookup = {uniques[key]:key for key in uniques}
            expected_length = (64 // bit_length)*bit_length
            for value in data:
                b = bin(value)[2:]
                b = b.zfill(expected_length)
                while len(b) >= bit_length:
                    chunk = b[:bit_length]
                    b = b[bit_length:]
                    key = int(chunk, 2)
                    output += reverse_lookup[key]

            textfile.write(output)
                
