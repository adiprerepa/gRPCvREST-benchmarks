import os

import lib


client = lib.FileClient('192.168.88.143:8888')
in_file_name = '/home/aditya/Downloads/5GiB.bin'


def bench_gRPC_upload(benchmark):
    benchmark(client.upload, in_file_name)
    
if __name__ == '__main__':

    # demo for file uploading
    client.upload(in_file_name)

