import mock
import pytest
from cox_auto_app.request_tools import (get_json_request,
                                        post_json_request,
                                        check_response)


class TestGetJson(object):
    """
    Tests for get_json_request function. These tests demonstrate
    expected failure modes for get_json_request function in
    addition to testing the calling of this function by the
    merge function.
    """
    @mock.patch('cox_auto_app.request_tools.check_response')
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

    @mock.patch('cox_auto_app.request_tools.check_response')
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

    @mock.patch('cox_auto_app.request_tools.check_response')
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


class TestPostJson(object):
    """
    Tests for post_json_request function. These tests demonstrate
    expected failure modes for post_json_request function in
    addition to testing the calling of this function by the
    merge function.
    """
    @mock.patch('cox_auto_app.request_tools.check_response')
    @mock.patch('requests.post')
    def test_bad_status(self, mock_post, mock_check):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        mock_post.return_value.status_code = return_status
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_check.side_effect = RuntimeError(expected_error)
        post_data = {'test': True}
        with pytest.raises(RuntimeError, match=expected_error):
            post_json_request(url=url, post_data=post_data)

    @mock.patch('cox_auto_app.request_tools.check_response')
    @mock.patch('requests.post')
    def test_bad_content(self, mock_post, mock_check):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        mock_post.return_value.status_code = 200
        mock_post.return_value.headers = {'content-type': return_content}
        expected_error = ('Expected json content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_check.side_effect = RuntimeError(expected_error)
        post_data = {'test': True}
        with pytest.raises(RuntimeError, match=expected_error):
            post_json_request(url=url, post_data=post_data)

    @mock.patch('cox_auto_app.request_tools.check_response')
    @mock.patch('requests.post')
    def test_good_return(self, mock_post, mock_check):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'application/json'
        json_data = {'test': True}
        mock_post.return_value.status_code = 200
        mock_post.return_value.headers = {'content-type': return_content}
        mock_post.return_value.json.return_value = json_data
        mock_check.return_value = json_data
        assert post_json_request(url=url, post_data=json_data) == json_data


class TestCheckResponse(object):
    """
    Tests for check_response function.
    """
    def test_bad_status(self):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        mock_response = mock.MagicMock()
        mock_response.return_value.status_code = return_status
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        with pytest.raises(RuntimeError, match=expected_error):
            check_response(url=url, response=mock_response)

    def test_bad_content(self):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        mock_response = mock.MagicMock()
        mock_response.return_value.status_code = 200
        mock_response.return_value.headers = {'content-type': return_content}
        expected_error = ('Expected json content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        with pytest.raises(RuntimeError, match=expected_error):
            check_response(url=url, response=mock_response)

    def test_good_return(self):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'application/json'
        json_data = {'test': True}
        mock_response = mock.MagicMock()
        mock_response.return_value.status_code = 200
        mock_response.return_value.headers = {'content-type': return_content}
        mock_response.return_value.json.return_value = json_data
        assert check_response(url=url, response=mock_response) == json_data

    #    @mock.patch('requests.get')
    #    def test_good_return(self, mock_get):
    #        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
    #        return_content = 'application/json'
    #        json_data = {'test': True}
    #        mock_get.return_value.status_code = 200
    #        mock_get.return_value.headers = {'content-type': return_content}
    #        mock_get.return_value.json.return_value = json_data
    #        assert get_json_request(url=url) == json_data
