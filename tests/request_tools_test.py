import mock
import pytest
from cox_auto_app.request_tools import (get_json_request)


class TestGetJson(object):
    """
    Tests for get_json_request function.
    """
    @mock.patch('requests.get')
    def test_bad_status(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        mock_get.return_value.status_code = return_status
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        with pytest.raises(RuntimeError, match=expected_error):
            get_json_request(url=url)

    @mock.patch('requests.get')
    def test_bad_content(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'content-type': return_content}
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        with pytest.raises(RuntimeError, match=expected_error):
            get_json_request(url=url)

    @mock.patch('requests.get')
    def test_good_return(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'text/html'
        json_data = {'test': True}
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'content-type': return_content}
        mock_get.return_value.json.return_value = json_data
        assert get_json_request(url=url) == json_data
