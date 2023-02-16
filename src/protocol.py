"""Protocol for chat server - Computação Distribuida Assignment 1."""
import json
from datetime import datetime
from socket import socket


class Message:
    """Message Type."""
    def __init__(self, command):
        self.command = command

    def __str__(self):
        return '{"command": '
    
class JoinMessage(Message):
    """Message to join a chat channel."""
    def __init__(self, command, channel):
        super().__init__(command)
        self.channel = channel

    def __str__(self):
        return super().__str__() + f'"join", "channel": "{self.channel}"' + '}'

class RegisterMessage(Message):
    """Message to register username in the server."""
    def __init__(self, command, username):
        super().__init__(command)
        self.username = username
    
    def __str__(self):
        return super().__str__() + f'"register", "user": "{self.username}"' + '}'
    
class TextMessage(Message):
    """Message to chat with other clients."""
    def __init__(self, command, message, channel, timestamp):
        super().__init__(command)
        self.message = message
        self.channel = channel
        self.timestamp = timestamp

    def __str__(self):
        return super().__str__() + f'"message", "message": "{self.message}", "channel": "{self.channel}", "ts": "{self.timestamp}"' + '}'


class CDProto:
    """Computação Distribuida Protocol."""

    @classmethod
    def register(cls, username: str) -> RegisterMessage:
        """Creates a RegisterMessage object."""

        return RegisterMessage('register', username)

    @classmethod
    def join(cls, channel: str) -> JoinMessage:
        """Creates a JoinMessage object."""

        return JoinMessage('join', channel)

    @classmethod
    def message(cls, message: str, channel: str = None) -> TextMessage:
        """Creates a TextMessage object."""

        timestamp = int(datetime.now().timestamp()) # used to get the time stamp
        return TextMessage('message', message, channel, timestamp)

    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        """Sends through a connection a Message object."""
        # has to see what time of message it is and use the classes above to send the messages
        # using if probably

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        """Receives through a connection a Message object."""
        # has to do the opposite of the function above, transforms message received to
        # be sent to other clients on the same channel


class CDProtoBadFormat(Exception):
    """Exception when source message is not CDProto."""

    def __init__(self, original_msg: bytes=None) :
        """Store original message that triggered exception."""
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        """Retrieve original message as a string."""
        return self._original.decode("utf-8")
