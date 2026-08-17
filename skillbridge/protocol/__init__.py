"""Protocols defined for communications between layers:
- response module defines the protocol between Cadence and Python daemon thread.
    The SKILL side does not know the length of the payload beforehand (the execution result),
    which is why we use framing bytes (STX/NAK ... RS).
- socket module defines the protocol between Python daemon thread (server) and client socket.
    Since we know the payload length in advance, we prepend a 10-byte length header.
"""

__all__ = ()
