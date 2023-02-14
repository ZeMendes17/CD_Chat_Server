"""CD Chat server program."""
import logging
import socket

logging.basicConfig(filename="server.log", level=logging.DEBUG)

class Server:
    """Chat Server process."""
    #                           INET                TCP
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criar socket
    serversock.bind(('localhost', 2000)) # associa endereço
    serversock.listen(5) # tamanho da fila de espera
    conn, addr = serversock.accept() # servidor espera por clientes, o servidor bloqueia e só desbloqueia quando alguem se ligar
    data = conn.recv(1000)
    print(data.decode())

    def loop(self):
        """Loop indefinetely."""

