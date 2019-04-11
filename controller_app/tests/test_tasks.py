import os
import logging
import asyncio
from unittest import TestCase, mock
from controller_app.tasks import run_manipulator
from controller_app.structures import ControllerStatus
from controller_app.connectors import ManipulatorConnector
from controller_app.config import THRESHOLD_SENSORS, THRESHOLD_VALUE
from aiohttp.web import Application
from controller_app.tools import init_logger


def init_local_loger():
    """
    Mocking logger so it logs to /dev/null during testing
    """
    devnull = open(os.devnull, 'w')
    logger = logging.getLogger('controller')
    logger_handler = logging.StreamHandler(stream=devnull)
    logger.addHandler(logger_handler)


async def do_nothing(value):
    return None

init_local_loger()


class TasksTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Here side_effect=InterruptedError allows us to break of the while loop
        """
        cls.mock_get_manipulator_patcher = mock.patch('controller_app.connectors.ManipulatorConnector.send_data')
        cls.mock_get_manipulator_patcher_start = cls.mock_get_manipulator_patcher.start()
        cls.mock_get_manipulator_patcher_start.side_effect = InterruptedError

        cls.mock_get_sleep_patcher = mock.patch('asyncio.sleep')
        cls.mock_get_sleep_patcher_start = cls.mock_get_sleep_patcher.start()
        cls.mock_get_sleep_patcher_start.side_effect = do_nothing

    def setUp(self):
        self.controller_status = ControllerStatus()
        self.manipulator = ManipulatorConnector(host='localhost', port='8080')

    def test_run_manipulator_1(self):
        """
        Tests that the decision is made by the task is correct. Expecting status property to change the status
        """
        self.controller_status.status = ControllerStatus.status_down
        loop = asyncio.get_event_loop()
        test_status_keeper = {
            1: 4,
            2: 5,
            3: 5,
            4: 6,
            5: 6,
            6: 5,
            7: 8,
            8: 1
        }
        with self.assertRaises(InterruptedError):
            task = loop.create_task(run_manipulator(test_status_keeper, 5, 4, self.controller_status, self.manipulator))
            loop.run_until_complete(task)
            loop.close()
        self.assertEqual(self.controller_status.status, ControllerStatus.status_up)

    def test_run_manipulator_2(self):
        """
        Tests that the decision is made by the task is correct. Expecting status property staying the same
        """
        self.controller_status.status = ControllerStatus.status_down
        loop = asyncio.get_event_loop()
        test_status_keeper = {
            1: 2,
            2: 2,
            3: 2,
            4: 2,
            5: 2,
            6: 2,
            7: 2,
            8: 2
        }
        with self.assertRaises(InterruptedError):
            task = loop.create_task(run_manipulator(test_status_keeper, 5, 4, self.controller_status, self.manipulator))
            loop.run_until_complete(task)
            loop.close()
        self.assertEqual(self.controller_status.status, ControllerStatus.status_down)

    def test_run_manipulator_3(self):
        """
        Tests that the decision is made by the task is correct. Expecting status property to change the status
        """
        self.controller_status.status = ControllerStatus.status_down
        loop = asyncio.get_event_loop()
        test_status_keeper = {
            1: 6,
            2: 6,
            3: 6,
            4: 6,
            5: 2,
            6: 2,
            7: 2,
            8: 2
        }
        with self.assertRaises(InterruptedError):
            task = loop.create_task(run_manipulator(test_status_keeper, 5, 4, self.controller_status, self.manipulator))
            loop.run_until_complete(task)
            loop.close()
        self.assertEqual(self.controller_status.status, ControllerStatus.status_up)
