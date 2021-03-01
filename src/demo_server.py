import lib
import threading
from bottle import run, put
import sys
# grpc -> 8888
# rest -> 8080

@put('/')
def yo():
    return 'yo'

if __name__ == '__main__':
   # lib.FileServer().start(8888)
   server = lib.FileServer()
   if len(sys.argv) == 1:
       chunk_size = 1024**2 * sys.argv[0]
       server.chunk_size = chunk_size
   rpc_thread = threading.Thread(target=server.start, args=(8888,))
   rest_thread = threading.Thread(target=run, kwargs={'host': '127.0.0.1', 'port': 8080})
   rpc_thread.start()
   rest_thread.start()
