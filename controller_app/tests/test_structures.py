from datetime import datetime
from unittest import TestCase, mock
from controller_app.structures import ControllerStatus


class ControllerStatusTest(TestCase):

    def setUp(self):
        self.controller_status = ControllerStatus()

    def test_controller_status_changed_from_up_to_down(self):
        """
        Tests if status of controller is changed after calling ControllerStatus.change_status from up to down
        """
        self.controller_status.status = ControllerStatus.status_up
        self.controller_status.change_status()
        self.assertEqual(self.controller_status.status, ControllerStatus.status_down)

    def test_controller_status_changed_from_down_to_up(self):
        """
        Tests if status of controller is changed after calling ControllerStatus.change_status from down to up
        """
        self.controller_status.status = ControllerStatus.status_down
        self.controller_status.change_status()
        self.assertEqual(self.controller_status.status, ControllerStatus.status_up)

    def test_changed_time_is_accurate(self):
        """
        Tests if the time changed is almost the same as the time recorded before status change
        """
        curr_time = datetime.now().replace(second=0, microsecond=0).timestamp()
        self.controller_status.change_status()
        res = self.controller_status.to_dict()
        time_change_happened = datetime.strptime(res['time_of_decision'], '%Y%m%dT%H%M').timestamp()
        self.assertEqual(curr_time, time_change_happened)
