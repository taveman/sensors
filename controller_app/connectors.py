import json
import socket
import struct
from logging import Logger


class ManipulatorConnector:
    """
    Manipulator connector that can communicate with manipulator service
    """
    def __init__(self, host, port, logger):
        """
        Initialisation
        :param host: host to be connected to
        :type host: str
        :param port: port to be connected to
        :type port: int
        :param logger: logger
        :type logger: Logger
        """
        self.host = host
        self.port = port
        self.logger = logger

    def send_data(self, data):
        """
        Sends data to a manipulator
        Working with the following format: the first byte
        (let's call it header) tells us the length of the remaining data (let's call it a body). Body is expected
        to be a JSON string that needs to be decoded accordingly
        :param data: data to be sent
        :type data: dict
        """
        self.logger.debug('{}: going to send {}'.format(self.__class__.__name__, data))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.host, self.port))
            except socket.error as e:
                self.logger.error(
                    '{}: couldn\'t connect to the {}:{}\n{}'.format(
                        self.__class__.__name__, self.host, self.port, e
                    )
                )
                return
            except Exception as e:
                self.logger.error(
                    '{}: general error while connecting to the {}:{}\n{}'.format(
                        self.__class__.__name__, self.host, self.port, e
                    )
                )
                return

            try:
                json_a = json.dumps(data)
            except TypeError as e:
                self.logger.error(
                    '{}: couldn\'t serialize {}\n{}'.format(
                        self.__class__.__name__, data, e
                    )
                )
                return

            body_length = len(json_a)
            data_to_send = struct.pack('b{}s'.format(body_length), body_length, json_a.encode())
            try:
                s.sendall(data_to_send)
            except socket.error as e:
                self.logger.error(
                    '{}: couldn\'t send the following data {}\n{}'.format(
                        self.__class__.__name__, data_to_send, e
                    )
                )
            self.logger.debug('{}: ALL OK'.format(self.__class__.__name__))

