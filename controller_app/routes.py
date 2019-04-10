from aiohttp.web import Application
from views import receive_sensor_data, get_manipulator_status


def setup_routes(app):
    """
    Maps urls to the views
    :param app: aiohttp application instance
    :type app: Application
    """
    app.router.add_post('/api/sensor', receive_sensor_data)
    app.router.add_get('/api/manipulator/status', get_manipulator_status)
