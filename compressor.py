import pickle

class Compressor():
    def __init__(self, filename):
        self.filename = filename
        self.outputname = filename+'.tc'

    def compress(self):
        with open(self.filename, 'r') as textfile:
            text = textfile.read()
        split_text = text.split(' ')
        uniques = {t:chr(i) for (i, t) in enumerate(set(split_text))}
        data = ''.join([uniques[t] for t in split_text])
        compressed = CompressedStructure(self.filename, uniques, data)
        with open(self.outputname, 'wb') as compressed_file:
            pickle.dump(compressed, compressed_file)


class CompressedStructure():
    def __init__(self, filename, uniques, data):
        self.filename = filename
        self.uniques = uniques
        self.data = data
