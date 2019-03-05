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
