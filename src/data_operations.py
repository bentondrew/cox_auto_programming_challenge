from .request_tools import (get_json_request)


def merge():
    url = 'https://vautointerview.azurewebsites.net/api/datasetid'
    return get_json_request(url=url)
