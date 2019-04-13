import os
from tools import init_logger, env_variable_to_int
from manipulator import Manipulator

MANIPULATOR_HOST = os.getenv('MANIPULATOR_HOST')
MANIPULATOR_PORT = env_variable_to_int('MANIPULATOR_PORT')
DEBUG_LOG = True if env_variable_to_int('DEBUG') else False

if __name__ == '__main__':

    logger = init_logger(
        'manipulator',
        '/var/log/manipulator/info.log',
        '/var/log/manipulator/debug.log',
        DEBUG_LOG
    )

    logger.info('Manipulator app starting with the following params:'
                '\nMANIPULATOR_HOST: {}'
                '\nMANIPULATOR_PORT: {}'
                '\nDEBUG: {}'.format(MANIPULATOR_HOST, MANIPULATOR_PORT, DEBUG_LOG)
                )
    a = Manipulator(MANIPULATOR_HOST, MANIPULATOR_PORT, logger=logger)
    a.run_server()
