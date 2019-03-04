import logging
from cox_auto_app.app_test import test


def app():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - '
                               '%(name)s - '
                               '%(levelname)s - '
                               '%(message)s')
    logging.info('Testing.')
    print(test())
