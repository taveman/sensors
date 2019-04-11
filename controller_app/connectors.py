# class ManipulatorInterface:
#     """
#     Manipulator interface needs to be used by all possible realisations of the manipulator connectors
#     """
#
#     def send_data(self, data):
#         """
#         Sends data to the manipulator
#         :param data:
#         :return:
#         """
#         raise NotImplementedError('send_data method needs to be implemented')


class ManipulatorConnector:
    """
    Manipulator connector that can communicate with manipulator service
    """
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def send_data(self, data):
        """
        Sends data to a manipulator
        :param data: data to be sent
        :type data: dict
        :return:
        """
        pass
