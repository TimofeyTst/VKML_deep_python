import logging


class OnlyUpperFilter(logging.Filter):
    def filter(self, record):
        method = record.msg.split(":")[0]
        return method.isupper()


def get_lru_cache_logger(log_file_name="cache.log", is_debug=False, logger_filter=None):
    logger = logging.getLogger("LoggerLRUCache")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s")

    file_handler = logging.FileHandler(log_file_name, mode="w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    if logger_filter is not None:
        file_handler.addFilter(logger_filter)
    logger.addHandler(file_handler)

    # Stream logging
    if is_debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_formatter = logging.Formatter("%(levelname)s\t%(message)s")
        stream_handler.setFormatter(stream_formatter)
        if logger_filter is not None:
            stream_handler.addFilter(logger_filter)
        logger.addHandler(stream_handler)

    return logger
