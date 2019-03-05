import mock
import pytest
from cox_auto_app.data_operations import (merge)


class TestMerge(object):
    """
    Tests for merge function.
    """
    @mock.patch('cox_auto_app.data_operations.get_json_request')
    def test_bad_status(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_json_request')
    def test_bad_content(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_json_request')
    def test_good_return(self, mock_get):
        json_data = {'test': True}
        mock_get.return_value = json_data
        assert merge() == json_data
