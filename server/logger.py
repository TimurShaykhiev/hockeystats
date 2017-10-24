import logging
from logging.handlers import RotatingFileHandler

from config import LOADER_LOG_FILE


LOG_SIZE_LIMIT = 50*1024*1024
BACKUP_COUNT = 5

LOADER_LOGGER_NAME = 'loader'


def create_loader_logger():
    logger = logging.getLogger(LOADER_LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(filename)s] [%(levelname)s] %(message)s')

    rfh = RotatingFileHandler(LOADER_LOG_FILE, maxBytes=LOG_SIZE_LIMIT, backupCount=BACKUP_COUNT)
    rfh.setLevel(logging.DEBUG)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)
    return logger


def get_loader_logger():
    return logging.getLogger(LOADER_LOGGER_NAME)


def create_app_log_handler(log_file):
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s [%(module)s:%(lineno)d]')
    rfh = RotatingFileHandler(log_file, maxBytes=LOG_SIZE_LIMIT, backupCount=BACKUP_COUNT)
    rfh.setLevel(logging.DEBUG)
    rfh.setFormatter(formatter)
    return rfh
