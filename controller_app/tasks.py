"""
Tasks that needs to be run on the main loop along with aiohttp web server
"""
import logging
from datetime import datetime
import asyncio

from controller_app.connectors import ManipulatorConnector
from controller_app.config import controller_state
from controller_app.structures import ControllerStatus
from controller_app.config import SENSOR_STATUS_KEEPER, MANIPULATOR_PORT, MANIPULATOR_HOST,\
    THRESHOLD_VALUE, THRESHOLD_SENSORS


async def run_manipulator(status_keeper, threshold_value, threshold_sensors, contr_state, manipulator):
    """
    Task that needs to wake up every 5 seconds, make decision on what
    to send to the manipulator based on what is in the special dict that
    keeps the latest sent data from sensors
    :param status_keeper: status keeper that keeps sensors states
    :type status_keeper: dict
    :param threshold_value: value that serves as a threshold point for sensors
    :type threshold_value: int
    :param threshold_sensors: number of sensors with state value above threshold_value which makes
            controller_state to change the state
    :type threshold_sensors: int
    :param contr_state: structure, that keeps the controller state
    :type contr_state: ControllerStatus
    :param manipulator: ManipulatorConnector object that can communicate with manipulator service
    :type manipulator: ManipulatorConnector
    """
    logger = logging.getLogger('controller')
    logger.debug('Starting manipulator task')

    while True:
        await asyncio.sleep(5)
        outlined_sensors = 0
        logger.info(status_keeper.items())
        for _, value in status_keeper.items():
            if value >= threshold_value:
                outlined_sensors += 1

        if outlined_sensors >= threshold_sensors:
            contr_state.change_status()
            logger.info(
                'Number of sensors above threshold: {} Controller status changed to {}'.format(
                    outlined_sensors, contr_state.status
                )
            )

        manipulator.send_data({'status': contr_state.status, 'datetime': datetime.now().strftime('%Y%m%dT%H%M')})


async def start_background_tasks(app):
    manipulator = ManipulatorConnector(host=MANIPULATOR_HOST, port=MANIPULATOR_PORT)
    app['manipulator_send_status'] = app.loop.create_task(
        run_manipulator(SENSOR_STATUS_KEEPER, THRESHOLD_VALUE, THRESHOLD_SENSORS, controller_state, manipulator)
    )


async def cleanup_background_tasks(app):
    app['manipulator_send_status'].cancel()
    await app['manipulator_send_status']
