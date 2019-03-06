import requests


def get_json_request(url):
    """
    Makes a get request to the provided url.

    Raises Runtime errors if the response HTTP status code is
    not 200 or the content-type is not application/json.

    Returns the json data in the body encoded in python
    data objects.
    """
    resp = requests.get(url)
    return check_response(url=url, response=resp)


def post_json_request(url, post_data):
    """
    Makes a post request to the provided url with the provided data
    as json in the post request.

    Raises Runtime errors if the response HTTP status code is
    not 200 or the content-type is not application/json.

    Returns the json data in the body encoded in python
    data objects.
    """
    resp = requests.post(url, json=post_data)
    return check_response(url=url, response=resp)


def check_response(url, response):
    if response.status_code == 200:
        if 'application/json' in response.headers['content-type']:
            return response.json()
        else:
            raise RuntimeError('Expected json content type '
                               'from url {} but got {}'
                               .format(url, response.headers['content-type']))
    else:
        raise RuntimeError('Got unexpected status code {} from url {}'
                           .format(response.status_code, url))
