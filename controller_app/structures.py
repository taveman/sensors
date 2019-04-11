from datetime import datetime


class ControllerStatus:
    """
    Controller status structure
    """
    status_up = 'up'
    status_down = 'down'

    def __init__(self):
        self.__status = ControllerStatus.status_up
        self.__time_changed = datetime.now()

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__time_changed = datetime.now()
        self.__status = value

    def change_status(self):
        if self.status == ControllerStatus.status_down:
            self.status = ControllerStatus.status_up
        else:
            self.status = ControllerStatus.status_down

    def to_dict(self):
        """
        Structure ready to be sent
        :rtype: dict
        """
        return {
            'status': self.__status,
            'datetime': datetime.now().strftime('%Y%m%dT%H%M'),
            'time_of_decision': self.__time_changed.strftime('%Y%m%dT%H%M')
        }

