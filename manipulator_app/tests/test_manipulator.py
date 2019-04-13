from unittest import TestCase
import json
import struct
import socket
import logging
import threading

from manipulator_app.manipulator import Manipulator

FAKE_PORT = 10001
HOST = '127.0.0.1'
logger = logging.getLogger('test')


def client_send_testing_data(data, port):
    """
    Socket client that sends data to the server
    :param data: data to be sent
    :type data: dict
    :param port: port to be listened to
    :type port: int
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        json_a = json.dumps(data)
        body_length = len(json_a)
        data_to_send = struct.pack('b{}s'.format(body_length), body_length, json_a.encode())
        s.sendall(data_to_send)


def client_send_testing_data_improper_json(data, port):
    """
    Socket client that sends data to the server
    :param data: data to be sent
    :type data: dict
    :param port: port to be listened to
    :type port: int
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        json_a = json.dumps(data)[:-1]
        print(json_a)
        body_length = len(json_a)
        data_to_send = struct.pack('b{}s'.format(body_length), body_length, json_a.encode())
        s.sendall(data_to_send)


def listening_server(manipulator, data_to_be_placed, port):
    """
    Starts listening and returns socket with data
    :param manipulator: Manipulator instance
    :type manipulator: Manipulator
    :param data_to_be_placed: object to be used to keep the result data
    :type data_to_be_placed: list
    :param port: port to be listened to
    :type port: int
    :return: socket
    :rtype socket.socket
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as m_socket:
        m_socket.bind((HOST, port))
        m_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket.setdefaulttimeout(3)
        m_socket.listen()
        remote_socket, addr = m_socket.accept()  # blocks here until data appears
        result = manipulator.read_from_socket(remote_socket)
        data_to_be_placed.append(result)


class TestManipulator(TestCase):

    def setUp(self):
        self.manipulator = Manipulator(host=HOST, port=FAKE_PORT, logger=logger)

    def test_data_parsed_correctly(self):
        """
        Tests if the data sent from client is received correctly by Manipulator
        """
        port = 10002
        result_data = []
        sending_data = {'datetime': '20190101T0230', 'status': 'down'}
        server_thread = threading.Thread(target=listening_server, args=(self.manipulator, result_data, port))
        client_thread = threading.Thread(target=client_send_testing_data, args=(sending_data, port))

        server_thread.start()
        client_thread.start()

        server_thread.join()
        client_thread.join()

        self.assertDictEqual(sending_data, result_data[0])

    def test_data_parsed_with_invalid_json(self):
        """
        Tests if the data sent from client is received correctly by Manipulator
        """
        port = 10003
        result_data = []
        sending_data = {'datetime': '20190101T0230', 'status': 'down'}
        server_thread = threading.Thread(target=listening_server, args=(self.manipulator, result_data, port))
        client_thread = threading.Thread(target=client_send_testing_data_improper_json, args=(sending_data, port))

        server_thread.start()
        client_thread.start()

        server_thread.join()
        client_thread.join()

        self.assertIsNone(result_data[0])
