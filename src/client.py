"""CD Chat client program"""
import logging
import sys
import socket
import selectors
import os
import fcntl

from .protocol import CDProto, CDProtoBadFormat

logging.basicConfig(filename=f"{sys.argv[0]}.log", level=logging.DEBUG)


class Client:
    """Chat Client process."""
    
    # sock.sendall('ola'.encode())

    def __init__(self, name: str = "Foo"):
        """Initializes chat client."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.selector = selectors.DefaultSelector()
        self.name = name
        self.channel = ""
        self.host = 'localhost' # host and port used to connect to server
        self.port = 2000
        self.clientChannels = [] # lista que guarda os channels do client

        # set sys.stdin non_blocking
        orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
        fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)
        self.selector.register(sys.stdin, selectors.EVENT_READ, self.send)

        print(f"Client {self.name} as been initialized")

    def connect(self):
        """Connect to chat server and setup stdin flags."""
        self.sock.connect((self.host, self.port))
        self.selector.register(self.sock, selectors.EVENT_READ, self.receive)
        serverMessage = CDProto.register(self.name)
        CDProto.send_msg(self.sock, serverMessage)

        print(f"You have established a connection with the server {self.host} in the port {self.port}")
        logging.debug(f"{self.name} has established a connection with {self.host}:{self.port}")

    def receive(self, sock, mask):
        messageInfo = CDProto.recv_msg(self.sock)
        logging.debug(f'Received {messageInfo.__str__}')
        print(f'{messageInfo.message}')
        
    def send(self, stdin, mask):
        message = stdin.read()

        if message == "exit\n" and len(message.split(" ")) == 1:
            print(f'Unregistering {self.name}')
            self.selector.unregister(self.sock)
            self.sock.close()
            print('Closing chat...')
            sys.exit()
        # fazer para join e message
        elif message.split(" ")[0] == "/join" and len(message.split(" ")) == 2:
            self.channel = message.split(" ")[1]

            if self.channel in self.clientChannels:
                print(f'{self.name} is already in this channel "{self.channel}". Impossible to join')
            else:
                self.clientChannels.append(self.channel) # adiciona o channel a lista dos clientes
                print(f"{self.name} has joined {self.channel}")
                joinMessage = CDProto.join(self.channel)
                CDProto.send_msg(self.sock, joinMessage)
        else:
            normalMessage = CDProto.message(message, self.channel)
            CDProto.send_msg(self.sock, normalMessage)


    def loop(self):
        """Loop indefinetely."""
        
        while True:
            sys.stdout.write(self.name + ">")
            sys.stdout.flush()

            for key, mask in self.selector.select():
                callback = key.data
                callback(key.fileobj, mask)
