import SocketServer, threading
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import peerhandler

class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer): 
    allow_reuse_address = True

online = True
def kill():
    global online
    online = False
    return True


port = peerhandler.gaParams.getVar('port')

class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        global online
        online = True

    def run(self):
        server = AsyncXMLRPCServer(('', port))
        server.register_function(kill, '__kill__')
        server.register_instance(peerhandler.PeerHandler())
        global online
        try:
            while online:
                server.handle_request()
        finally:
            server.server_close()

        server.server_close()
