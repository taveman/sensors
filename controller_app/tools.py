import logging
from logging.handlers import TimedRotatingFileHandler


def init_logger(logger_name, info_logger_path, debug_logger_path='/var/log/controller_debug.log', debug=False):
    """
    Logger initializer
    :param logger_name: logger name to be used
    :type logger_name: str
    :param info_logger_path: path to the logger with logging level INFO
    :type info_logger_path: str
    :param debug_logger_path: path to the logger with logging level DEBUG
    :type debug_logger_path: str
    :param debug: does logger need to record debug information or doesn't
    :type debug: bool
    """
    logger = logging.getLogger(logger_name)

    formatter = logging.Formatter('%(levelname)s [%(funcName)s]: %(asctime)s: %(name)s: %(message)s')
    file_h_info = TimedRotatingFileHandler(info_logger_path, when='D', interval=1, backupCount=50)
    file_h_info.setLevel(logging.INFO)
    file_h_info.setFormatter(formatter)

    stream_h = logging.StreamHandler()
    stream_h.setFormatter(formatter)
    stream_h.setLevel(logging.INFO)

    if debug:
        file_h_debug = TimedRotatingFileHandler(debug_logger_path, when='D', interval=1, backupCount=50)
        file_h_debug.setLevel(logging.DEBUG)
        file_h_debug.setFormatter(formatter)

        logger.addHandler(file_h_debug)
        stream_h.setLevel(logging.DEBUG)

    logger.addHandler(stream_h)
    logger.addHandler(file_h_info)

    logger.setLevel(logging.DEBUG) if debug else logger.setLevel(logging.INFO)
