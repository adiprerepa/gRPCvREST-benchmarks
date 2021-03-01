import os
from concurrent import futures
import grpc
import time
import timeit
import chunk_pb2, chunk_pb2_grpc



def get_file_chunks(filename, chunk_size):
    with open(filename, 'rb') as f:
        while True:
            print(chunk_size)
            piece = f.read(chunk_size);
            if len(piece) == 0:
                return
            yield chunk_pb2.Chunk(buffer=piece)


def save_chunks_to_file(chunks, filename):
    with open(filename, 'wb') as f:
        for chunk in chunks:
            f.write(chunk.buffer)

def cleanup(filename):
    if os.path.exists(filename):
        os.remove(filename)

class FileClient:
    def __init__(self, address):
        channel = grpc.insecure_channel(address, options=[
            ('grpc.max_send_message_length', 1024**3),
        ])
        self.stub = chunk_pb2_grpc.FileServerStub(channel)
        # default chunk size of 1 MB
        self.chunk_size = 1024**2

    def upload(self, in_file_name):
        t1 = timeit.default_timer()
        chunks_generator = get_file_chunks(in_file_name, self.chunk_size)
        response = self.stub.upload(chunks_generator)
        print('upload of file took %.15f' % (timeit.default_timer() - t1))
        assert response.length == os.path.getsize(in_file_name)

    def download(self, target_name, out_file_name):
        response = self.stub.download(chunk_pb2.Request(name=target_name))
        save_chunks_to_file(response, out_file_name)


class FileServer(chunk_pb2_grpc.FileServerServicer):
    def __init__(self):

        class Servicer(chunk_pb2_grpc.FileServerServicer):
            def __init__(self):
                self.tmp_file_name = '/tmp/server_tmp'
                self.chunk_size = 1024**2

            def upload(self, request_iterator, context):
                save_chunks_to_file(request_iterator, self.tmp_file_name)
                size = os.path.getsize(self.tmp_file_name)
                # deletion takes time - need to delete for next iteration
                cleanup(self.tmp_file_name)
                return chunk_pb2.Reply(length=size)

            def download(self, request, context):
                if request.name:
                    return get_file_chunks(self.tmp_file_name, self.chunk_size)

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        chunk_pb2_grpc.add_FileServerServicer_to_server(Servicer(), self.server)

    def start(self, port):
        address = '[::]:%d' % (port)
        self.server.add_insecure_port(address)
        print('starting on %s' % address)
        self.server.start()
        self.server.wait_for_termination()

