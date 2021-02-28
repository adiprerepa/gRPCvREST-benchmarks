import lib
import threading
from bottle import run, put

# grpc -> 8888
# rest -> 8080

@put('/')
def yo():
    return 'yo'

if __name__ == '__main__':
   # lib.FileServer().start(8888)
   rpc_thread = threading.Thread(target=lib.FileServer().start, args=(8888,))
   rest_thread = threading.Thread(target=run, kwargs={'host': '127.0.0.1', 'port': 8080})
   rpc_thread.start()
   rest_thread.start()
