import logging
from .data_collection import (get_dataset_id,
                              get_vehicle_ids,
                              get_data_for_vehicles,
                              get_dealer_names)
from .request_tools import (post_json_request)


def merge():
    logging.info('Getting data set id.')
    data_set_id = get_dataset_id()
    logging.info('Getting vehicle ids for data set id {}.'
                 .format(data_set_id))
    vehicle_ids = get_vehicle_ids(data_set_id=data_set_id)
    logging.info('Getting vehicle info.')
    dealer_list, error_list = get_data_for_vehicles(data_set_id=data_set_id,
                                                    vehicle_ids=vehicle_ids)
    if error_list:
        for item in error_list:
            logging.info('Error {} in getting info for vehicle id {}'
                         .format(item['error_message'], item['vehicleId']))
    logging.info('Getting dealer info.')
    dealer_list, error_list = get_dealer_names(data_set_id=data_set_id,
                                               dealer_list=dealer_list)
    if error_list:
        for item in error_list:
            logging.info('Error {} in getting info for dealer id {}'
                         .format(item['error_message'], item['dealerId']))
    dealer_dict = {'dealers': dealer_list}
    post_url = ('https://vautointerview.azurewebsites.net/api/{}/answer'
                .format(data_set_id))
    return post_json_request(url=post_url, post_data=dealer_dict)
