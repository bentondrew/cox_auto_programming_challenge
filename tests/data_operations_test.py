import mock
import pytest
from cox_auto_app.data_operations import (merge)


class TestMergeErrorInDatasetidCollection(object):
    """
    Tests for expected exceptions in datasetid collection in
    merge function.
    """
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_bad_status(self, mock_get_dataset):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get_dataset.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_bad_content(self, mock_get_dataset):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get_dataset.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_return_not_dict(self, mock_get_dataset):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        expected_error = ('Data returned from {} is not of type '
                          'dict.'.format(url))
        mock_get_dataset.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_not_right_key_in_dict_return(self, mock_get_dataset):
        mock_get_dataset.side_effect = KeyError('Test error')
        with pytest.raises(KeyError):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_return_dict_key_value_not_str(self, mock_get_dataset):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        expected_error = ('Data returned from {} does not have value '
                          'of type str for key datasetid.'.format(url))
        mock_get_dataset.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()


class TestMergeErrorInVehicleidsCollection(object):
    """
    Tests for expected exceptions in vehicleIds collection in
    merge function.
    """
    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_bad_status(self, mock_get_dataset, mock_get_vehicle_ids):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get_vehicle_ids.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_bad_content(self, mock_get_dataset, mock_get_vehicle_ids):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get_vehicle_ids.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_return_not_dict(self, mock_get_dataset, mock_get_vehicle_ids):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        expected_error = ('Data returned from {} is not of type '
                          'dict.'.format(url))
        mock_get_vehicle_ids.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_not_right_key_in_dict_return(self,
                                          mock_get_dataset,
                                          mock_get_vehicle_ids):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        mock_get_vehicle_ids.side_effect = KeyError('Test error')
        with pytest.raises(KeyError):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_return_dict_key_value_not_list(self,
                                            mock_get_dataset,
                                            mock_get_vehicle_ids):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        expected_error = ('Data returned from {} does not have value '
                          'of type list for key vehicleIds.'
                          .format(url))
        mock_get_vehicle_ids.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()

    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_item_not_int_in_list(self,
                                  mock_get_dataset,
                                  mock_get_vehicle_ids):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        expected_error = ('Data hi at index 2 in list of vehicle ids '
                          '[5, 9, "hi"] returned from {} does not have value '
                          'of type int.'
                          .format(url))
        mock_get_vehicle_ids.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            merge()
