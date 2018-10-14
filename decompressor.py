import pickle

class Decompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            compressed = pickle.load(compressed_file)

        with open(compressed.filename, 'w') as textfile:
            output = ''
            reverse_lookup = {compressed.uniques[key]:key for key in compressed.uniques}
            expected_length = (64 // compressed.bit_length)*compressed.bit_length
            for value in compressed.data:
                b = bin(value)[2:]
                b = b.zfill(expected_length)
                while len(b) >= compressed.bit_length:
                    chunk = b[:compressed.bit_length]
                    print(chunk, int(chunk,2))
                    b = b[compressed.bit_length:]
                    key = int(chunk, 2)
                    output += reverse_lookup[key]

            textfile.write(output)
                
