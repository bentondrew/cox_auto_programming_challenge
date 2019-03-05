import logging
from .app_test import test


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - '
                               '%(name)s - '
                               '%(levelname)s - '
                               '%(message)s')
    try:
        logging.info('Testing.')
        print(test())
    except Exception:
        logging.error('Exception', exc_info=True)
