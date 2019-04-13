import sys
import json
import socket
import struct
from logging import Logger


class Manipulator:
    """
    Simple manipulator class
    Expecting the following simple protocol: first 2 bytes tells us about the body size,
    so we know how many bytes to read from socket
    """
    def __init__(self, host, port, logger):
        """
        Instance initialisation
        :param host: host to be bind to
        :type host: str
        :param port: port to be listened to
        :type port: int
        :param logger: logger to be used
        :type logger: Logger
        """
        self.host = host
        self.port = port
        self.logger = logger

    def run_server(self):
        """
        Runs the server
        """
        m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        try:
            m_socket.bind((self.host, self.port))
        except socket.error as e:
            self.logger.error('{}: Error appeared while binding to the {}:{}\n{}'.format(
                self.__class__.__name__, self.host, self.port, e)
            )
            sys.exit(1)

        m_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        m_socket.listen()
        self.logger.debug('{}: listening...'.format(self.__class__.__name__))
        while m_socket:
            remote_socket, addr = m_socket.accept()
            self.logger.debug('{}: got connection from {}'.format(self.__class__.__name__, addr))

            data_from_socket = self.read_from_socket(remote_socket)
            self.logger.info(
                '{}: controller status: {}'.format(
                    self.__class__.__name__, data_from_socket.get('status')
                )
            )

    def read_from_socket(self, sock):
        """
        Reads data from a socket. Expecting the following format: the first byte
        (let's call it header) tells us the length of the remaining data (let's call it a body). Body is expected
        to be a JSON string that needs to be decoded accordingly
        :param sock: socket to be read from
        :type sock: socket.socket
        """
        header = sock.recv(1)
        number_of_bytes_expecting = struct.unpack('b', header)[0]  # in this case we could either use ord(header)
        body = sock.recv(number_of_bytes_expecting)
        self.logger.debug('{}: got the following data: {}'.format(self.__class__.__name__, body))
        try:
            res = json.loads(body)
        except json.decoder.JSONDecodeError as e:
            self.logger.error('{}: json decoding error:\n{}'.format(self.__class__.__name__, e))
            return
        finally:
            sock.close()
        return res
