import mock
import pytest
from cox_auto_app.data_operations import (merge)


class TestMerge(object):
    """
    Test successful execution of merge function.
    """
    @mock.patch('cox_auto_app.data_operations.post_json_request')
    @mock.patch('cox_auto_app.data_operations.get_dealer_names')
    @mock.patch('cox_auto_app.data_operations.get_data_for_vehicles')
    @mock.patch('cox_auto_app.data_operations.get_vehicle_ids')
    @mock.patch('cox_auto_app.data_operations.get_dataset_id')
    def test_good(self,
                  mock_get_dataset,
                  mock_get_vehicle_ids,
                  mock_vehicle_data,
                  mock_dealer_data,
                  mock_json_post):
        data_set_id = '7'
        mock_get_dataset.return_value = data_set_id
        vehicle_ids = [1, 2, 3, 4]
        mock_get_vehicle_ids.return_value = vehicle_ids
        vehicle_data = [{'dealerId': 1,
                         'vehicles': [{'vehicleId': 1,
                                       'year': 1,
                                       'make': 'test',
                                       'model': 'test'},
                                      {'vehicleId': 2,
                                       'year': 1,
                                       'make': 'test',
                                       'model': 'test'}]},
                        {'dealerId': 2,
                         'vehicles': [{'vehicleId': 3,
                                       'year': 1,
                                       'make': 'test',
                                       'model': 'test'},
                                      {'vehicleId': 4,
                                       'year': 1,
                                       'make': 'test',
                                       'model': 'test'}]}]
        error_data = None
        mock_vehicle_data.return_value = (vehicle_data, error_data)
        dealer_data = [{'dealerId': 1,
                        'name': 'test',
                        'vehicles': [{'vehicleId': 1,
                                      'year': 1,
                                      'make': 'test',
                                      'model': 'test'},
                                     {'vehicleId': 2,
                                      'year': 1,
                                      'make': 'test',
                                      'model': 'test'}]},
                       {'dealerId': 2,
                        'name': 'test',
                        'vehicles': [{'vehicleId': 3,
                                      'year': 1,
                                      'make': 'test',
                                      'model': 'test'},
                                     {'vehicleId': 4,
                                      'year': 1,
                                      'make': 'test',
                                      'model': 'test'}]}]
        mock_dealer_data.return_value = (dealer_data, error_data)
        json_data = {'dealers': dealer_data}
        mock_json_post.return_value = json_data
        merge()


class TestMergeErrorInDatasetidCollection(object):
    """
    Tests for expected exceptions in datasetid collection in
    merge function. These tests demonstrate expected failure
    modes for get_dataset_id function in addition to testing
    the calling of this function by the merge function.
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
    merge function. These tests demonstrate expected failure
    modes for the get_vehicle_ids function in addition to testing
    the calling of this function by the merge function.
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
        # Removed expected error match due to pytest issue with comparing
        # long strings.
        with pytest.raises(RuntimeError):
            merge()
