import os
import logging
from controller_app.structures import ControllerStatus
from controller_app.tools import env_variable_to_int


logger = logging.getLogger('controller')

SENSOR_STATUS_KEEPER = {}
controller_state = ControllerStatus()

MANIPULATOR_HOST = os.environ.get('MANIPULATOR_HOST')
MANIPULATOR_PORT = os.environ.get('MANIPULATOR_PORT')

THRESHOLD_VALUE = env_variable_to_int('THRESHOLD_VALUE')
THRESHOLD_SENSORS = env_variable_to_int('THRESHOLD_SENSORS')
