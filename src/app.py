import logging
from .app_test import test


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - '
                               '%(name)s - '
                               '%(levelname)s - '
                               '%(message)s')
    logging.info('Testing.')
    print(test())
