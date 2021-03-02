# gRPCvsREST-benchmarks

Benchmarks for gRPC vs REST for file transfer.

## Running

To run the the server (ideally over a network to mimic real conditions):

```
python3 src/server.py
```

This will spin up a gRPC and REST server on two separate threads. The gRPC service will be 
bound to port `8888`, while the REST service to `8080`.


Once you have the server running, you will need to run the client.


```
python3 src/client.py <protocol> <chunk size>
```

Here, you need to include the protocol you want to benchmark. The options are `grpc` or `rest`. 

As for chunk size, this is expressed in megabytes.

You will also need to change the server ip on the client, you can find this on line `10`. You also
need to change the location of the test file. It is defaulted to a location of a 5 gb file on my compter,
so it will not work for you. You should change this on line `15`.

## Under the hood

When you select the `grpc` option, the client will open a unidirectional stream to the server, read a chunk
from the file, put it in a protobuf message `bytes` field, and send it. 

As for the `rest` option, it uses chunked transfer encoding, following roughly the same protocol.


## Results

More official benchmarks to come, and you can run it on your system, but it looks like these seem to perform the same.

For a 5 GB file on a ~400 MBPS network, it took:
- grpc protocol an average of `46.3` seconds
- rest protocol an average of `46.7` seconds


We can conclude that for streaming large files, there really isn't much of a difference for gRPC vs REST.
