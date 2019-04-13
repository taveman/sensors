import logging
from aiohttp import web
from routes import setup_routes
from tools import init_logger, env_variable_to_int

from tasks import start_background_tasks, cleanup_background_tasks


DEBUG_LOG = True if env_variable_to_int('DEBUG') else False


logger = init_logger(
    'controller',
    '/var/log/controller.log',
    '/var/log/controller_debug.log',
    '/var/log/controller_error.log',
    debug=DEBUG_LOG)

logger.info('STARTING CONTROLLER: DEBUG IS {}'.format('ON' if DEBUG_LOG else 'OFF'))

app = web.Application()
setup_routes(app)

#  additional task that communicates with manipulator
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)
web.run_app(app)


