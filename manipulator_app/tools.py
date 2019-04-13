import os
import logging
from logging.handlers import TimedRotatingFileHandler


def init_logger(logger_name, info_logger_path, debug_logger_path='/var/log/manipulator_debug.log',
                error_logger_path='/var/log/manipulator_error.log', debug=False):
    """
    Logger initializer
    :param logger_name: logger name to be used
    :type logger_name: str
    :param info_logger_path: path to the logger with logging level INFO
    :type info_logger_path: str
    :param debug_logger_path: path to the logger with logging level DEBUG
    :type debug_logger_path: str
    :param error_logger_path: path to the logger with logging level ERROR
    :type error_logger_path: str
    :param debug: does logger need to record debug information or doesn't
    :type debug: bool
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.ERROR)

    logger = logging.getLogger(logger_name)

    formatter = logging.Formatter('%(levelname)s [%(funcName)s]: %(asctime)s: %(name)s: %(message)s')
    file_h_info = TimedRotatingFileHandler(info_logger_path, when='D', interval=1, backupCount=50)
    file_h_error = TimedRotatingFileHandler(error_logger_path, when='D', interval=1, backupCount=50)

    file_h_info.setLevel(logging.INFO)
    file_h_info.setFormatter(formatter)

    file_h_error.setLevel(logging.ERROR)
    file_h_error.setFormatter(formatter)

    stream_h = logging.StreamHandler()
    stream_h.setFormatter(formatter)
    stream_h.setLevel(logging.INFO)

    root_logger.addHandler(file_h_error)

    if debug:
        file_h_debug = TimedRotatingFileHandler(debug_logger_path, when='D', interval=1, backupCount=50)
        file_h_debug.setLevel(logging.DEBUG)
        file_h_debug.setFormatter(formatter)

        logger.addHandler(file_h_debug)
        stream_h.setLevel(logging.DEBUG)

    logger.addHandler(stream_h)
    logger.addHandler(file_h_info)

    logger.setLevel(logging.DEBUG) if debug else logger.setLevel(logging.INFO)

    return logger


def env_variable_to_int(name):
    """
    Environment variable conversion to an integer
    :param name: environment variable
    :return: converted env variable to an integer or 0
    :rtype: int
    """
    env_var = os.environ.get(name)
    if not env_var:
        return 0

    try:
        return int(env_var)
    except ValueError:
        return 0
