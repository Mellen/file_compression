import sys

class Decompressor():
    def __init__(self, filename):
        self.filename = filename

    def decompress(self):
        with open(self.filename, 'rb') as compressed_file:
            filename, data, chars, bit_length = self.readfile(compressed_file)

        with open(filename, 'w') as textfile:
            output = ''
            expected_length = (64 // bit_length)*bit_length
            for value in data:
                b = bin(value)[2:]
                b = b.zfill(expected_length)
                while len(b) >= bit_length:
                    chunk = b[:bit_length]
                    b = b[bit_length:]
                    key = int(chunk, 2)
                    if key > 0:
                        output += chars[key-1]

            textfile.write(output)

    def readfile(self, file_obj):
        filename_length = int.from_bytes(file_obj.read(4), sys.byteorder)
        filename = file_obj.read(filename_length).decode('utf-8')
        cbl = int.from_bytes(file_obj.read(4), sys.byteorder)
        chars = file_obj.read(cbl).decode('utf-8')
        bit_length = int.from_bytes(file_obj.read(4), sys.byteorder)
        dl = int.from_bytes(file_obj.read(4), sys.byteorder)
        data = []
        current_bytes = file_obj.read(8)
        while current_bytes:
            datum = int.from_bytes(current_bytes, sys.byteorder)
            data.append(datum)
            current_bytes = file_obj.read(8)

        return (filename, data, chars, bit_length)
