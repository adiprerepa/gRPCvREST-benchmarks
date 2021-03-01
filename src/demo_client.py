import os
import sys
import lib


client = lib.FileClient('192.168.88.143:8888')
in_file_name = '/home/aditya/Downloads/5GiB.bin'


def bench_gRPC_upload(benchmark):
    benchmark(client.upload, in_file_name)
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        chunk_size = 1024**2 * sys.argv[0]
        client.chunk_size = chunk_size
    # demo for file uploading
    client.upload(in_file_name)

