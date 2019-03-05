import logging
from .data_operations import merge


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - '
                               '%(name)s - '
                               '%(levelname)s - '
                               '%(message)s')
    try:
        logging.info('Merging vehicle and dealer information for '
                     'datasets.')
        print(merge())
    except Exception:
        logging.error('Exception', exc_info=True)
