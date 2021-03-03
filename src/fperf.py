import timeit
import os
import sys


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("include file name")
        sys.exit()
    chunk_size = 1024
    t1 = timeit.default_timer()
    with open(sys.argv[1], 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if not c:
                break
    print('took %.15f seconds' % (timeit.default_timer() - t1))
