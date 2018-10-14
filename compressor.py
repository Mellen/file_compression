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

        frequencies = {}
        for c in text:
            if c in frequencies:
                frequencies[c] += 1
            else:
                frequencies[c] = 1

        freq_list = sorted([(k,frequencies[k]) for k in frequencies], key=lambda f: f[1])

        frequencies = {f[0]:'0'*i for i, f in enumerate(freq_list)}

        data = self.text_to_data(text, frequencies)
        data_byte_count = (data.bit_length() // 8) + 1;
        
        with open(self.outputname, 'wb') as compressed_file:
            filename_bytes = os.path.basename(self.filename).encode('utf-8')
            compressed_file.write((len(filename_bytes)).to_bytes(4, sys.byteorder))
            compressed_file.write(filename_bytes)
            freq_pickle = pickle.dumps(frequencies)
            compressed_file.write((len(freq_pickle)).to_bytes(4, sys.byteorder))
            compressed_file.write(freq_pickle)
            compressed_file.write(data_byte_count.to_bytes(16, sys.byteorder))
            compressed_file.write(data.to_bytes(data_byte_count, sys.byteorder))

    def text_to_data(self, text, frequencies):
        value = '1'
        for c in text:
            value += frequencies[c]
            value += '1'
        return int(value, 2)
