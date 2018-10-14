import pickle

class Decompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            compressed = pickle.load(compressed_file)

        with open(compressed.filename, 'w') as textfile:
            output = []
            reverse_lookup = {compressed.uniques[key]:key for key in compressed.uniques}
            for c in compressed.data:
                output.append(reverse_lookup[c])

            text = ' '.join(output)

            textfile.write(text)
                
