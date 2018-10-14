import pickle
import sys
import os

class Compressor():
    def __init__(self, filename):
        self.filename = filename
        self.outputname = filename+'.tc'

    def compress(self):
        with open(self.filename, 'r') as textfile:
            text = textfile.read()
        
        uniques = {t:i for (i, t) in enumerate(set(text))}
        data = self.text_to_data(text, uniques)
        
        with open(self.outputname, 'wb') as compressed_file:
            filename_bytes = os.path.basename(self.filename).encode('utf-8')
            compressed_file.write((len(filename_bytes)).to_bytes(4, sys.byteorder))
            compressed_file.write(filename_bytes)
            unique_pickle = pickle.dumps(uniques)
            compressed_file.write((len(unique_pickle)).to_bytes(4, sys.byteorder))
            compressed_file.write(unique_pickle)
            bit_length = len(uniques).bit_length()
            compressed_file.write(bit_length.to_bytes(4, sys.byteorder))
            compressed_file.write((len(data)).to_bytes(4, sys.byteorder))
            for datum in data:
                compressed_file.write(datum.to_bytes(8, sys.byteorder))

    def text_to_data(self, text, uniques):
        bl = len(uniques).bit_length()
        max_inserts = 64//bl;
        current_insert = 0
        value = ''
        values = []
        for c in text:
            n = uniques[c]
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
