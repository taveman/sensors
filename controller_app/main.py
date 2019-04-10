import logging
from aiohttp import web
from routes import setup_routes
from tools import init_logger


init_logger('controller', '/var/log/controller.log', debug=True)

logger = logging.getLogger('controller')
logger.debug('STARTING')

app = web.Application()
setup_routes(app)
web.run_app(app)


