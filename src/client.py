import os
import sys
import lib
import http.client
import time
from contextlib import closing
url = '192.168.88.143:8888'
rest_url = '127.0.0.1:8080'
client = lib.FileClient(url)
in_file_name = '/home/aditya/Downloads/5GiB.bin'

def upload_rest_chunked(file_name, chunk_size):
    conn = http.client.HTTPConnection(rest_url)
    with closing(conn):
        conn.putrequest('PUT', '/upload-file')
        headers = {
                'Transfer-Encoding': 'chunked',
                'X-Requested-With': 'XMLHttpRequest',

        }
        for n, v in headers.items():
            conn.putheader(n, v)
        conn.endheaders()
        with open(file_name, 'rb') as f:
            bytes_uploaded = 0
            while True:
                to_send = f.read(chunk_size)
                if not to_send:
                    break
                conn.send(b'%X\r\n%s\r\n' % (len(to_send), to_send))
                bytes_uploaded += len(to_send)
                print(bytes_uploaded)
            conn.send(b'0\r\n\r\n')
            response = conn.getresponse()
            print(response)
            
def bench_gRPC_upload(benchmark):
    benchmark(client.upload, in_file_name)
    
if __name__ == '__main__':
    if len(sys.argv) == 2:
        chunk_size = 1024**2 * int(sys.argv[1])
        client.chunk_size = chunk_size
    # demo for file uploading
    #client.upload(in_file_name)
    upload_rest_chunked(in_file_name, 1024*16)
