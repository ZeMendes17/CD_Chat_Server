"""CD Chat client program"""
import logging
import sys
import socket

from .protocol import CDProto, CDProtoBadFormat

logging.basicConfig(filename=f"{sys.argv[0]}.log", level=logging.DEBUG)


class Client:
    """Chat Client process."""
    
    # sock.sendall('ola'.encode())

    def __init__(self, name: str = "Foo"):
        """Initializes chat client."""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        """Connect to chat server and setup stdin flags."""
        
        self.sock.connect(('localhost', 2000))

    def loop(self):
        """Loop indefinetely."""
        pass
