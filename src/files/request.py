import sys
import base64
from jsonrpc.proxy import ServiceProxy

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print('Usage {} <user_pk> <filename>'.format( sys.argv[0] ))
        sys.exit(1)

    user_pk = sys.argv[1]
    filename = sys.argv[2]
    rpc_server = ServiceProxy('http://127.0.0.1:8080/api/')
    with open( filename, 'rb') as input_content:
        content = base64.b64encode( input_content.read() )
        rpc_server.api.upload_photo( user_pk, content.decode('utf-8'))
