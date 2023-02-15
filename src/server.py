"""CD Chat server program."""
import logging
import socket
import selectors

logging.basicConfig(filename="server.log", level=logging.DEBUG)

class Server:
    """Chat Server process."""

    def __init__(self):
        #                           INET                TCP
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criar socket
        self.serversock.bind(('localhost', 2000)) # associa endereço
        self.serversock.listen(5) # tamanho da fila de espera
        self.sel = selectors.DefaultSelector() # selector
        self.sel.register(self.serversock, selectors.EVENT_READ, self.accept) 
        self.activeClients = [] # lista para guardar os clientes atualmente ativos para envio de mensagens
        

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready # servidor espera por clientes, o servidor bloqueia e só desbloqueia quando alguem se ligar
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)
    
    def read(self, conn, mask):
        data = conn.recv(1000)

        if data:
            print('echoing', repr(data), 'to', conn) # nao e para dar echo, e para enviar para os outros clients
            conn.send(data)

        else:
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
