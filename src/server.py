"""CD Chat server program."""
import logging
import socket
import selectors
import json
from .protocol import CDProto

logging.basicConfig(filename="server.log", level=logging.DEBUG)

class Server:
    """Chat Server process."""

    def __init__(self):
        #                           INET                TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criar socket
        self.sock.bind(('localhost', 2000)) # associa endereço
        self.sock.listen(5) # tamanho da fila de espera
        self.sel = selectors.DefaultSelector() # selector
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept) 
        self.activeClients = [] # lista para guardar os clientes atualmente ativos para envio de mensagens
        self.clientChannels = {} # dicionario que guarda os channels de cada user

        print("Server has been initialized")
        logging.debug("Server initialized")
        

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready # servidor espera por clientes, o servidor bloqueia e só desbloqueia quando alguem se ligar
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)
    
    def read(self, conn, mask):
        miniHeader = int.from_bytes(conn.recv(2), 'big') #to seperate messages
        data = conn.recv(miniHeader).decode("utf-8") # Should be ready

        if data:
            print('Received: ' + data)

            try:
                data_info = json.loads(data)
            except json.JSONDecodeError:
                print("Error reading json")
                return
            
            command = data_info["command"]

            if command == "register":
                user = data_info["user"]
                if user == None:
                    print("Cannot register user. Invalid User")

                else:
                    self.clientChannels[conn] = []
                    self.activeClients.append(conn)
                    print('User: ' + user + ' register with success')

            elif command == "join":
                channel = data_info["channel"]
                client_channels = self.clientChannels[conn]

                if channel == None:
                    print("User cannot join, invalid channel")
                elif channel in client_channels:
                    print("User already in " + channel)
                else:
                    print("User joined: " + channel)
                    self.clientChannels[conn].append(channel)

            elif command == "message": 
                # needs to send the message
                message = data_info["message"]
                if message == None:
                    print("User cannot send message. Invalid format")
                else:
                    # sends message to users in the same channel
                    channel = data_info["channel"] # sends to this channel or all of them?
                    for user in self.activeClients:
                        if user != conn and self.clientChannels[user] != None:
                            user_channels = self.clientChannels[user]
                            if channel in user_channels:
                                CDProto.send_msg(user, data)


            else:
                print("Invalid command")


        else:
            print("Something went wrong. C  losing...")
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    
    # print(data.decode())

    def loop(self):
        """Loop indefinetely."""

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
