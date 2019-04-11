import logging
from aiohttp import web

from validators import RequestValidator, schema_names
from config import controller_state, SENSOR_STATUS_KEEPER


async def receive_sensor_data(request):
    """
    Accepts data from the sensors
    :param request: aiohttp web request
    :type request: web.Request
    :return: aiohttp response object
    :rtype web.Response
    """
    global SENSOR_STATUS_KEEPER
    logger = logging.getLogger('controller')

    try:
        data = await request.json()

    except web.RequestPayloadError as e:
        logger.error('Request has invalid or no json data:\n{}'.format(e))
        return web.json_response({'status': 'error'}, status=400)

    validation_result = RequestValidator.data_validator(data, validation_schema=schema_names.sensor_data)

    if not validation_result.get('status'):
        logger.error('Received data from sensors validation error: {}\nDATA: {}'.format(
            validation_result.get('errors'), data)
        )
        return web.json_response({'status': 'error', 'details': validation_result.get('errors')}, status=400)

    data = validation_result.get('document')

    SENSOR_STATUS_KEEPER[data['id']] = data['payload']

    logger.info('receive_sensor_data received data: {}'.format(data))
    return web.json_response({'status': 'success'}, status=200)


async def get_manipulator_status(request):
    """
    Returns manipulator status
    :param request: aiohttp web request
    :type request: web.Request
    :return: aiohttp response object
    :rtype web.Response
    """
    logger = logging.getLogger('controller')
    logger.debug('Sending current state to the web server:\n{}'.format(controller_state.to_dict()))
    return web.json_response(controller_state.to_dict(), status=200)
