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
    def __init__(self, command, message, channel, ts):
        super().__init__(command)
        self.message = message
        self.channel = channel
        self.ts = ts

    def __str__(self):
        return super().__str__() + f'"message", "message": "{self.message}", "channel": "{self.channel}", "ts": "{self.ts}"' + '}'


class CDProto:
    """Computação Distribuida Protocol."""

    @classmethod
    def register(cls, username: str) -> RegisterMessage:
        """Creates a RegisterMessage object."""

    @classmethod
    def join(cls, channel: str) -> JoinMessage:
        """Creates a JoinMessage object."""

    @classmethod
    def message(cls, message: str, channel: str = None) -> TextMessage:
        """Creates a TextMessage object."""

    @classmethod
    def send_msg(cls, connection: socket, msg: Message):
        """Sends through a connection a Message object."""

    @classmethod
    def recv_msg(cls, connection: socket) -> Message:
        """Receives through a connection a Message object."""


class CDProtoBadFormat(Exception):
    """Exception when source message is not CDProto."""

    def __init__(self, original_msg: bytes=None) :
        """Store original message that triggered exception."""
        self._original = original_msg

    @property
    def original_msg(self) -> str:
        """Retrieve original message as a string."""
        return self._original.decode("utf-8")
