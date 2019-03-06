import mock
import pytest
from cox_auto_app.request_tools import (get_json_request)


class TestGetJson(object):
    """
    Tests for get_json_request function. These tests demonstrate
    expected failure modes for get_json_request function in
    addition to testing the calling of this function by the
    merge function.
    """
    @mock.patch('check_response')
    @mock.patch('requests.get')
    def test_bad_status(self, mock_get, mock_check):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        mock_get.return_value.status_code = return_status
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_check.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            get_json_request(url=url)

    @mock.patch('check_response')
    @mock.patch('requests.get')
    def test_bad_content(self, mock_get, mock_check):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'content-type': return_content}
        expected_error = ('Expected json content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_check.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            get_json_request(url=url)

    @mock.patch('check_response')
    @mock.patch('requests.get')
    def test_good_return(self, mock_get, mock_check):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'application/json'
        json_data = {'test': True}
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'content-type': return_content}
        mock_get.return_value.json.return_value = json_data
        mock_check.return_value = json_data
        assert get_json_request(url=url) == json_data

    #    @mock.patch('requests.get')
    #    def test_good_return(self, mock_get):
    #        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
    #        return_content = 'application/json'
    #        json_data = {'test': True}
    #        mock_get.return_value.status_code = 200
    #        mock_get.return_value.headers = {'content-type': return_content}
    #        mock_get.return_value.json.return_value = json_data
    #        assert get_json_request(url=url) == json_data
