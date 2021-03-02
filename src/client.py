import os
import sys
import grpclib
import http.client
import time
import timeit
from contextlib import closing
# CHANGE THIS IF YOU AREN'T ADITYA
# dont use localhost - not accurate
url = '192.168.88.143'
grpc_port = 8888
rest_port = 8080
client = grpclib.FileClient(url + ':' + str(grpc_port))
# todo make this configurable
in_file_name = '/home/aditya/Downloads/5GiB.bin'

#mimics codalab as close as possible
def upload_rest_chunked(file_name, chunk_size):
    conn = http.client.HTTPConnection(url + ':' + str(rest_port))
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
            conn.send(b'0\r\n\r\n')
            response = conn.getresponse()
            print(response)
            
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: python3 client.py <protocol> <chunk size in mb> where protocols are 'grpc' or 'rest'")
        sys.exit()
    chunk_size = 1024**2 * int(sys.argv[2])
    if sys.argv[1] == "rest":
        t1 = timeit.default_timer()
        upload_rest_chunked(in_file_name, chunk_size)
        print('upload of file took %.15f' % (timeit.default_timer() - t1))
    else:
        client.chunk_size = chunk_size
        client.upload(in_file_name)
