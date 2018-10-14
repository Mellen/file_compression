import pickle

class Compressor():
    def __init__(self, filename):
        self.filename = filename
        self.outputname = filename+'.tc'

    def compress(self):
        with open(self.filename, 'r') as textfile:
            text = textfile.read()
        
        uniques = {t:i for (i, t) in enumerate(set(text))}
        data = self.text_to_data(text, uniques)
        compressed = CompressedStructure(self.filename, uniques, len(uniques).bit_length(), data)
        
        with open(self.outputname, 'wb') as compressed_file:
            pickle.dump(compressed, compressed_file)

    def text_to_data(self, text, uniques):
        bl = len(uniques).bit_length()
        max_inserts = 64//bl;
        current_insert = 0
        value = ''
        values = []
        for c in text:
            n = uniques[c]
            b = (bin(n)[2:]).zfill(bl)
            print(n, b)
            value += b
            current_insert += 1
            if current_insert == max_inserts:
                values.append(int(value, 2))
                current_insert = 0
                value = ''

        if current_insert < max_inserts:
            values.append(int(value, 2))

        return values

class CompressedStructure():
    def __init__(self, filename, uniques, bit_length, data):
        self.filename = filename
        self.uniques = uniques
        self.bit_length = bit_length
        self.data = data
