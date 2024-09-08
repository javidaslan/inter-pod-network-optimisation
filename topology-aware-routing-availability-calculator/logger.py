import logging


def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Define logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    logger_format = logging.Formatter('{"level": "%(levelname)s", "timestamp": "%(asctime)s", '
                                      '"file": "%(filename)s:%(''lineno)s",'
                                      ' "message": "%(message)s"}', "%Y-%m-%d %H:%M:%S")
    stream_handler.setFormatter(logger_format)

    return logger
