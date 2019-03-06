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
        merge_results = merge()
        logging.info('Merge completed with status of {} in {} '
                     'milliseconds.'
                     .format(merge_results['success'],
                             merge_results['totalMilliseconds']))
        logging.info('Merge status message: {}'.merge_results['message'])
    except Exception:
        logging.error('Exception', exc_info=True)
