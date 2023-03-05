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
        self.name = {} # dicionario que guarda o nome de cada conn
        self.clientChannels = {} # dicionario que guarda os channels de cada user

        print("Server has been initialized")
        logging.debug("Server initialized")
        

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready # servidor espera por clientes, o servidor bloqueia e só desbloqueia quando alguem se ligar
        print("New client has arrived!")
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
                    self.name[conn] = user
                    self.clientChannels[conn] = [None] # indicates that it is in the base channel
                    print('User: ' + user + ' register with success')
                    logging.debug(f"{user} has joined the chat")

            elif command == "join":
                channel = data_info["channel"]
                client_channels = self.clientChannels.get(conn)

                if channel == None:
                    print("User cannot join, invalid channel")
                elif channel in client_channels:
                    print("User already in " + channel)
                else:
                    if client_channels == [None]:
                        self.clientChannels[conn] = [channel]
                    else:
                        self.clientChannels[conn].append(channel)

                    print(f"User joined: {channel}")
                    logging.debug(f"{self.name[conn]} joined: {channel}")

            elif command == "unjoin":
                channel = data_info["channel"]
                client_channels = self.clientChannels.get(conn)

                if channel == None:
                    print("User cannot unjoin, invalid channel")
                elif channel in client_channels:
                    if client_channels == [channel]:
                        self.clientChannels[conn] = [None]
                    else:
                        self.clientChannels[conn].remove(channel)

                    print(f"User unjoined: {channel}")
                    logging.debug(f"{self.name[conn]} unjoined: {channel}")
                else:
                    print("User is not in " + channel)

            elif command == "message": 
                # needs to send the message
                message = data_info["message"]
                if message == None:
                    print("User cannot send message. Invalid format")
                else:
                    # sends message to users in the same channel
                    channel = data_info["channel"] # sends to this channel or all of them?
                    msgToSend = CDProto.message(f'{self.name[conn]}>> {message}')
                    print(f'{self.name[conn]} (channel: {channel}) -> {message}')
                    logging.debug(f'{self.name[conn]} (channel: {channel}) -> {message}')

                    for user in self.clientChannels.keys():
                        if channel == "" and user != conn:
                            CDProto.send_msg(user, msgToSend)

                        elif user != conn and channel in self.clientChannels[user]:
                            CDProto.send_msg(user, msgToSend)

            else:
                print("Invalid command") # nao vem para aqui quase de certeza


        else:
            # print("Something went wrong. Closing...")
            print('Closing', conn)
            try:
                logging.debug(f'{self.name[conn]} left the chat')
                del self.name[conn]
                del self.clientChannels[conn]
            except KeyError as err:
                self.name = {}
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
