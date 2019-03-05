import requests


def get_json_request(url):
    """
    Makes a get request to the provided url.

    Raises Runtime errors if the HTTP status code is
    not 200 or the content-type is not application/json.

    Returns the json data in the body encoded in python
    data objects.
    """
    resp = requests.get(url)
    if resp.status_code == 200:
        if 'application/json' in resp.headers['content-type']:
            return resp.json()
        else:
            raise RuntimeError('Expected html content type '
                               'from url {} but got {}'
                               .format(url, resp.headers['content-type']))
    else:
        raise RuntimeError('Got unexpected status code {} from url {}'
                           .format(resp.status_code, url))
