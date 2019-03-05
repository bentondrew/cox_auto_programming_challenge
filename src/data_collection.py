from .request_tools import (get_json_request)


def get_dataset_id():
    """
    Makes a request to the
    https://vautointerview.azurewebsites.net/api/datasetid
    url to get a datasetid.

    Does not catch exceptions.

    Raises RunimeError if data back from url is not a dict
    with a string value. Explicitly attempts to access
    'datasetid' key to raise KeyError if key doesn't exist.

    Returns the sting value for the 'datasetId' key in the
    received dict.
    """
    url = 'https://vautointerview.azurewebsites.net/api/datasetid'
    data_set_id = get_json_request(url=url)
    if type(data_set_id) is not dict:
        raise RuntimeError('Data returned {} from {} is not of type '
                           'dict.'.format(data_set_id, url))
    # Check if key in dict; expected to raise KeyError if key
    # not in dict.
    value = data_set_id['datasetid']
    if type(value) is not str:
        raise RuntimeError('Data returned {} from {} does not have value '
                           'of type str for key datasetid.'
                           .format(data_set_id, url))
    return value
