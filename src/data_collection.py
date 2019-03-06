import logging
from threading import (Thread)
from .request_tools import (get_json_request)


def get_dataset_id():
    """
    Makes a request to the
    https://vautointerview.azurewebsites.net/api/datasetid
    url to get a datasetId.

    Does not catch exceptions.

    Raises RunimeError if data back from url is not a dict
    with a string value for the 'datasetId' key. Explicitly
    attempts to access 'datasetId' key to raise KeyError if
    key doesn't exist.

    Returns the sting value for the 'datasetId' key in the
    received dict.
    """
    url = 'https://vautointerview.azurewebsites.net/api/datasetid'
    data_set_dict = get_json_request(url=url)
    if type(data_set_dict) is not dict:
        raise RuntimeError('Data returned {} from {} is not of type '
                           'dict.'.format(data_set_dict, url))
    # Check if key in dict; expected to raise KeyError if key
    # not in dict.
    value = data_set_dict['datasetId']
    if type(value) is not str:
        raise RuntimeError('Data returned {} from {} does not have value '
                           'of type str for key datasetId.'
                           .format(data_set_dict, url))
    return value


def get_vehicle_ids(data_set_id):
    """
    Makes a request to the
    https://vautointerview.azurewebsites.net/api/{datasetId}/vehicles
    url to get a list of vehicle ids.

    Does not catch exceptions.

    Raises RunimeError if data back from url is not a dict
    with a list value for the 'vehicleIds' key. The list
    is expected to be a list of integers. Explicitly
    attempts to access 'vehicleIds' key to raise KeyError if
    key doesn't exist.

    Returns a list of the vehicle ids.
    """
    url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
           .format(data_set_id))
    vehicle_id_dict = get_json_request(url=url)
    if type(vehicle_id_dict) is not dict:
        raise RuntimeError('Data returned {} from {} is not of type '
                           'dict.'.format(vehicle_id_dict, url))
    # Check if key in dict; expected to raise KeyError if key
    # not in dict.
    value = vehicle_id_dict['vehicleIds']
    if type(value) is not list:
        raise RuntimeError('Data returned {} from {} does not have value '
                           'of type list for key vehicleIds.'
                           .format(vehicle_id_dict, url))
    for i, v_id in enumerate(value):
        if type(v_id) is not int:
            raise RuntimeError('Data {} at index {} in list of vehicle ids {} '
                               'returned from {} does not have value '
                               'of type int.'
                               .format(v_id, i, value, url))
    return value


def get_data_for_vehicles(data_set_id, vehicle_ids):
    """
    Calls get_vehicle_data to get details for a specific
    vehicle id at the url
    https://vautointerview.azurewebsites.net/api/{datasetId}/vehicles/{vehicleId}.

    Does not catch exceptions.

    Returns a list of of dealers and an error list.

    The dealer list contains a list of dicts which contain
    the dealerId and the list of vehicles for each dealer.
    Each vehicle in the list of vehicles is a dict containing
    the vehicleId, year, make, and model keys.

    If an error occurs when downloading vehicle info, will
    save the error for that vehicle id in the dict under the
    key error_message. These errors are not raised as it is
    anticipated that an error for one may not mean all will
    error. Any vehicle with an error will be saved in an
    error list which is returned separately.
    """
    error_list = None
    dealer_list = None
    download_return = {}
    thread_list = []
    for vehicle_id in vehicle_ids:
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        download_return[vehicle_id] = {}
        kwargs = {'url': url,
                  'data_return': download_return[vehicle_id]}
        v_thread = Thread(target=get_vehicle_data, kwargs=kwargs)
        v_thread.start()
        thread_list.append(v_thread)
    for v_thread in thread_list:
        v_thread.join()
    for vehicle_id in download_return:
        vehicle_info = download_return[vehicle_id]
        logging.info('Data for vehicle id {}: {}'
                     .format(vehicle_id, vehicle_info))
        if 'error_message' in vehicle_info:
            if error_list:
                error_list.append(vehicle_info)
            else:
                error_list = [vehicle_info]
        else:
            dealer_id = vehicle_info['dealerId']
            d_v_info = {k: v
                        for k, v in vehicle_info.items()
                        if k != 'dealerId'}
            if dealer_list:
                dealer = next((dealer_info
                               for dealer_info in dealer_list
                               if dealer_info['dealerId'] ==
                               dealer_id),
                              None)
                if dealer:
                    dealer['vehicles'].append(d_v_info)
                else:
                    dealer_list.append({'dealerId': dealer_id,
                                        'vehicles': [d_v_info]})
            else:
                dealer_list = [{'dealerId': dealer_id,
                                'vehicles': [d_v_info]}]
    return dealer_list, error_list


def get_vehicle_data(url, data_return):
    """
    Makes requests to the
    https://vautointerview.azurewebsites.net/api/{datasetId}/vehicles/{vehicleId}
    url to get details for a specific vehicle id.

    Catches exceptions and adds them to error_message field.

    Fills in the provided data_return variable with the
    vehicle info. The vehicle info is a dict containing
    the dealerId, vehicleId, year, make, and model keys.

    If an error occurs when downloading vehicle info, will
    save the error for that vehicle id in the dict under the
    key error_message. These errors are not raised as it is
    anticipated that an error for one may not mean all will
    error. Any vehicle with an error will be saved in an
    error list which is returned separately.

    Adds error_message for  if data back from url is not a dict
    with the keys of vehicleId, year, make, model, dealerId.
    The vehicleId is expected to be an integer. The year
    is expected to be an integer. The make is expected to
    be a string. The model is expected to be a string. The
    dealerId is expected to be an integer. Explicitly
    attempts to access the expected keys to raise KeyError if
    the key doesn't exist.
    """
    try:
        vehicle_info_dict = get_json_request(url=url)
        if type(vehicle_info_dict) is not dict:
            raise RuntimeError('Data returned {} from {} is not '
                               'of type dict.'
                               .format(vehicle_info_dict, url))
        expected_keys_and_types = {'vehicleId': int,
                                   'year': int,
                                   'make': str,
                                   'model': str,
                                   'dealerId': int}
        for key in expected_keys_and_types:
            if key not in vehicle_info_dict:
                raise RuntimeError('Key {} not found in vehicle '
                                   'info dict {} returned from '
                                   'url {}'
                                   .format(key,
                                           vehicle_info_dict,
                                           url))
            if type(vehicle_info_dict
                    [key]) is not expected_keys_and_types[key]:
                raise RuntimeError('Value {} is not type {} '
                                   'in vehicle info '
                                   'dict {} returned from url {}'
                                   .format(vehicle_info_dict[key],
                                           expected_keys_and_types
                                           [key],
                                           vehicle_info_dict,
                                           url))
        data_return = vehicle_info_dict
        logging.info('data_return for url {}: {}'
                     .format(url, data_return))
    except Exception as e:
        data_return['error_message'] = e
        logging.info('data_return for url {}: {}'
                     .format(url, data_return))
