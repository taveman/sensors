import os
from datetime import datetime
from time import time
from uuid import uuid4
from random import randint
import asyncio

from tools import init_logger, env_variable_to_int, craft_json_http


TIMES_IN_SECONDS = 100
TIME_TO_SLEEP = 1 / TIMES_IN_SECONDS
CONTROLLER_HOST = os.environ.get('CONTROLLER_HOST', 'localhost')
CONTROLLER_PORT = env_variable_to_int('CONTROLLER_PORT')
API_URL = '/api/sensor'
DEBUG_LOG = True if env_variable_to_int('DEBUG') else False


async def send_data(loop):
    """
    Sending data function
    """
    time_now = time()
    # controller_url = 'http://{host}:{port}/api/sensor'.format(
    #     host=CONTROLLER_HOST,
    #     port=CONTROLLER_PORT
    # )
    controller_id = str(uuid4())
    logger = init_logger(
        'sensor',
        '/var/log/sensor/sensor_{}.log'.format(controller_id),
        '/var/log/sensor/sensor_debug_{}.log'.format(controller_id),
        '/var/log/sensor/sensor_error_{}.log'.format(controller_id),
        debug=DEBUG_LOG
    )
    # connector = aiohttp.TCPConnector(limit=100)
    # async with aiohttp.ClientSession(connector=connector) as session:
    #     while True:
    #         data_to_send = {
    #             'id': controller_id,
    #             'payload': randint(0, 9),
    #             'datetime': datetime.now().strftime('%Y%m%dT%H%M')
    #         }
    #         async with session.post(controller_url, json=data_to_send) as resp:
    #             logger.debug('Data sent: {}'.format(data_to_send))

    count = 0
    reader, writer = await asyncio.open_connection(CONTROLLER_HOST, CONTROLLER_PORT, loop=loop)
    while True:
        data_to_send = {
            'id': controller_id,
            'payload': randint(0, 9),
            'datetime': datetime.now().strftime('%Y%m%dT%H%M')
        }
        message = craft_json_http(data_to_send, CONTROLLER_HOST, API_URL)
        writer.write(message)
        # res = await reader.read(1024)
        count += 1
        await asyncio.sleep(TIME_TO_SLEEP)
        if count > 100:
            logger.info('Time passed: {} Count: {}'.format(time() - time_now, count))
            time_now = time()
            count = 0


if __name__ == '__main__':

    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(send_data(main_loop))
