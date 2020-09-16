import grpc
import LNBitsLightningServicer as lnbits
from concurrent import futures
import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import os



os.environ["GRPC_SSL_CIPHER_SUITES"] = 'HIGH+ECDSA'

# read in key and certificate
with open('tls.key', 'rb') as f:
    private_key = f.read()
with open('tls.cert', 'rb') as f:
    certificate_chain = f.read()

# create server credentials
server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
lnrpc.add_LightningServicer_to_server(lnbits.LNBitsLightningServicer(), server)

# add secure port using crendentials
server.add_secure_port('[::]:10009', server_credentials)
server.start()
server.wait_for_termination()
