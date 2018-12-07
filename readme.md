# File Compression

A exploratory look at how to compress files.

tc.py uses my basic understanding of how losses compression should work (see https://dev.to/mellen/the-basic-basics-of-compression-lap to see how I came up with it.)

bc.py is an implementation of Huffman coding, that works for any type of file. It is a lot better at compression compared to my basic implementation.

(**Requires python 3**)

tc.py is a text file compression programme

     usage: tc.py [-h] [-d] file name

     positional arguments:  
        file name   The name of the file to be processed.

     optional arguments:  
        -h, --help  show this help message and exit  
        -d          Decompress the file (defaults to compressing).

bc.py is a compression programme for any type of file

     usage: bc.py [-h] [-d] file name

     positional arguments:  
        file name   The name of the file to be processed.

     optional arguments:  
        -h, --help  show this help message and exit  
        -d          Decompress the file (defaults to compressing).
