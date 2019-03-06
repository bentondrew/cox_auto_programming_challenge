import mock
import pytest
from cox_auto_app.data_collection import (get_dataset_id,
                                          get_vehicle_ids,
                                          get_vehicle_data,
                                          get_dealer_info)


class TestGetDatasetid(object):
    """
    Tests for get_dataset_id function.
    """
    # get_json_request pass through tests.
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_status(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            get_dataset_id()

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_content(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            get_dataset_id()

    # get_dataset_id generated exceptions
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_not_dict(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        json_data = 1
        expected_error = ('Data returned {} from {} is not of type '
                          'dict.'.format(json_data, url))
        mock_get.return_value = json_data
        with pytest.raises(RuntimeError, match=expected_error):
            get_dataset_id()

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_key_not_in_return(self, mock_get):
        json_data = {'test': True}
        mock_get.return_value = json_data
        with pytest.raises(KeyError):
            get_dataset_id()

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_value_for_key_not_str(self, mock_get):
        url = 'https://vautointerview.azurewebsites.net/api/datasetid'
        json_data = {'datasetId': True}
        expected_error = ('Data returned {} from {} does not have value '
                          'of type str for key datasetId.'
                          .format(json_data, url))
        mock_get.return_value = json_data
        with pytest.raises(RuntimeError, match=expected_error):
            get_dataset_id()

    # good test
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_good_return(self, mock_get):
        json_data = {'datasetId': 'test'}
        mock_get.return_value = json_data
        assert get_dataset_id() == json_data['datasetId']


class TestGetVehicleids(object):
    """
    Tests for get_vehicle_ids function.
    """
    # get_json_request pass through tests.
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_status(self, mock_get):
        data_set_id = '7'
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            get_vehicle_ids(data_set_id=data_set_id)

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_content(self, mock_get):
        data_set_id = '7'
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get.side_effect = RuntimeError(expected_error)
        with pytest.raises(RuntimeError, match=expected_error):
            get_vehicle_ids(data_set_id=data_set_id)

    # get_vehicle_ids generated exceptions
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_not_dict(self, mock_get):
        data_set_id = '7'
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        json_data = 1
        expected_error = ('Data returned {} from {} is not of type '
                          'dict.'.format(json_data, url))
        mock_get.return_value = json_data
        with pytest.raises(RuntimeError, match=expected_error):
            get_vehicle_ids(data_set_id=data_set_id)

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_key_not_in_return(self, mock_get):
        data_set_id = '7'
        json_data = {'test': True}
        mock_get.return_value = json_data
        with pytest.raises(KeyError):
            get_vehicle_ids(data_set_id=data_set_id)

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_value_for_key_not_str(self, mock_get):
        data_set_id = '7'
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles'
               .format(data_set_id))
        json_data = {'vehicleIds': True}
        expected_error = ('Data returned {} from {} does not have value '
                          'of type list for key vehicleIds.'
                          .format(json_data, url))
        mock_get.return_value = json_data
        with pytest.raises(RuntimeError, match=expected_error):
            get_vehicle_ids(data_set_id=data_set_id)

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_value_in_list_not_int(self, mock_get):
        data_set_id = '7'
        json_data = {'vehicleIds': [1, 'hi']}
        # Not testing for error message match due to issue with
        # long string comparisons in pytest.
        mock_get.return_value = json_data
        with pytest.raises(RuntimeError):
            get_vehicle_ids(data_set_id=data_set_id)

    # good test
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_good_return(self, mock_get):
        data_set_id = '7'
        json_data = {'vehicleIds': [1, 2]}
        mock_get.return_value = json_data
        assert get_vehicle_ids(
            data_set_id=data_set_id) == json_data['vehicleIds']


class TestGetVehicleData(object):
    """
    Tests for get_vehicle_data function.
    """
    # get_json_request pass through tests.
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_status(self, mock_get):
        data_set_id = '7'
        vehicle_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get.side_effect = RuntimeError(expected_error)
        data_return = {vehicle_id: {}}
        get_vehicle_data(url=url,
                         data_return=data_return,
                         vehicle_id=vehicle_id)
        assert vehicle_id in data_return
        expected_keys = ['vehicleId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(vehicle_id)
            if key == 'vehicleId':
                assert data_return.get(vehicle_id).get(key) == vehicle_id
            if key == 'error_message':
                assert data_return.get(vehicle_id).get(key) == expected_error

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_content(self, mock_get):
        data_set_id = '7'
        vehicle_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get.side_effect = RuntimeError(expected_error)
        data_return = {vehicle_id: {}}
        get_vehicle_data(url=url,
                         data_return=data_return,
                         vehicle_id=vehicle_id)
        assert vehicle_id in data_return
        expected_keys = ['vehicleId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(vehicle_id)
            if key == 'vehicleId':
                assert data_return.get(vehicle_id).get(key) == vehicle_id
            if key == 'error_message':
                assert data_return.get(vehicle_id).get(key) == expected_error

    # get_vehicle_data generated exceptions
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_not_dict(self, mock_get):
        data_set_id = '7'
        vehicle_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        json_data = 1
        expected_error = ('Data returned {} from {} is not of type '
                          'dict.'.format(json_data, url))
        mock_get.return_value = json_data
        data_return = {vehicle_id: {}}
        get_vehicle_data(url=url,
                         data_return=data_return,
                         vehicle_id=vehicle_id)
        assert vehicle_id in data_return
        expected_keys = ['vehicleId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(vehicle_id)
            if key == 'vehicleId':
                assert data_return.get(vehicle_id).get(key) == vehicle_id
            if key == 'error_message':
                assert data_return.get(vehicle_id).get(key) == expected_error

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_key_not_in_return(self, mock_get):
        data_set_id = '7'
        vehicle_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        json_data = {'vehicleId': 1,
                     'year': 1,
                     'model': 'test',
                     'dealerId': 1}
        expected_error = ('"Key make not found in vehicle '
                          'info dict {} returned from '
                          'url {}"'
                          .format(json_data,
                                  url))
        mock_get.return_value = json_data
        data_return = {vehicle_id: {}}
        get_vehicle_data(url=url,
                         data_return=data_return,
                         vehicle_id=vehicle_id)
        assert vehicle_id in data_return
        expected_keys = ['vehicleId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(vehicle_id)
            if key == 'vehicleId':
                assert data_return.get(vehicle_id).get(key) == vehicle_id
            if key == 'error_message':
                assert data_return.get(vehicle_id).get(key) == expected_error

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_value_for_key_not_correct(self, mock_get):
        data_set_id = '7'
        vehicle_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        json_data = {'vehicleId': 1,
                     'year': 7.5,
                     'make': 'test',
                     'model': 'test',
                     'dealerId': 1}
        expected_error = ('Value 7.5 is not type int '
                          'in vehicle info '
                          'dict {} returned from url {}'
                          .format(json_data,
                                  url))
        mock_get.return_value = json_data
        data_return = {vehicle_id: {}}
        get_vehicle_data(url=url,
                         data_return=data_return,
                         vehicle_id=vehicle_id)
        assert vehicle_id in data_return
        expected_keys = ['vehicleId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(vehicle_id)
            if key == 'vehicleId':
                assert data_return.get(vehicle_id).get(key) == vehicle_id
            if key == 'error_message':
                assert data_return.get(vehicle_id).get(key) == expected_error

    # good test
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_good_return(self, mock_get):
        data_set_id = '7'
        vehicle_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/vehicles/{}'
               .format(data_set_id, vehicle_id))
        json_data = {'vehicleId': 1,
                     'year': 1,
                     'make': 'test',
                     'model': 'test',
                     'dealerId': 1}
        mock_get.return_value = json_data
        data_return = {vehicle_id: {}}
        get_vehicle_data(url=url,
                         data_return=data_return,
                         vehicle_id=vehicle_id)
        assert vehicle_id in data_return
        assert data_return.get(vehicle_id) == json_data


class TestGetDealerInfo(object):
    """
    Tests for get_dealer_info function.
    """
    # get_json_request pass through tests.
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_status(self, mock_get):
        data_set_id = '7'
        dealer_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/dealers/{}'
               .format(data_set_id, dealer_id))
        return_status = 500
        expected_error = ('Got unexpected status code {} from url '
                          '{}'.format(return_status, url))
        mock_get.side_effect = RuntimeError(expected_error)
        data_return = {dealer_id: {}}
        get_dealer_info(url=url,
                        data_return=data_return,
                        dealer_id=dealer_id)
        assert dealer_id in data_return
        expected_keys = ['dealerId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(dealer_id)
            if key == 'dealerId':
                assert data_return.get(dealer_id).get(key) == dealer_id
            if key == 'error_message':
                assert data_return.get(dealer_id).get(key) == expected_error

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_bad_content(self, mock_get):
        data_set_id = '7'
        dealer_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/dealers/{}'
               .format(data_set_id, dealer_id))
        return_content = 'bad'
        expected_error = ('Expected html content type '
                          'from url {} but got {}'
                          .format(url, return_content))
        mock_get.side_effect = RuntimeError(expected_error)
        data_return = {dealer_id: {}}
        get_dealer_info(url=url,
                        data_return=data_return,
                        dealer_id=dealer_id)
        assert dealer_id in data_return
        expected_keys = ['dealerId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(dealer_id)
            if key == 'dealerId':
                assert data_return.get(dealer_id).get(key) == dealer_id
            if key == 'error_message':
                assert data_return.get(dealer_id).get(key) == expected_error

    # get_dealer_info generated exceptions
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_not_dict(self, mock_get):
        data_set_id = '7'
        dealer_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/dealers/{}'
               .format(data_set_id, dealer_id))
        json_data = 1
        expected_error = ('Data returned {} from {} is not of type '
                          'dict.'.format(json_data, url))
        mock_get.return_value = json_data
        data_return = {dealer_id: {}}
        get_dealer_info(url=url,
                        data_return=data_return,
                        dealer_id=dealer_id)
        assert dealer_id in data_return
        expected_keys = ['dealerId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(dealer_id)
            if key == 'dealerId':
                assert data_return.get(dealer_id).get(key) == dealer_id
            if key == 'error_message':
                assert data_return.get(dealer_id).get(key) == expected_error

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_key_not_in_return(self, mock_get):
        data_set_id = '7'
        dealer_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/dealers/{}'
               .format(data_set_id, dealer_id))
        json_data = {'dealerId': 1}
        expected_error = ('"Key name not found in dealer '
                          'info dict {} returned from '
                          'url {}"'
                          .format(json_data,
                                  url))
        mock_get.return_value = json_data
        data_return = {dealer_id: {}}
        get_dealer_info(url=url,
                        data_return=data_return,
                        dealer_id=dealer_id)
        assert dealer_id in data_return
        expected_keys = ['dealerId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(dealer_id)
            if key == 'dealerId':
                assert data_return.get(dealer_id).get(key) == dealer_id
            if key == 'error_message':
                assert data_return.get(dealer_id).get(key) == expected_error

    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_return_value_for_key_not_correct(self, mock_get):
        data_set_id = '7'
        dealer_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/dealers/{}'
               .format(data_set_id, dealer_id))
        json_data = {'name': 7.5,
                     'dealerId': 1}
        expected_error = ('Value 7.5 is not type str '
                          'in dealer info '
                          'dict {} returned from url {}'
                          .format(json_data,
                                  url))
        mock_get.return_value = json_data
        data_return = {dealer_id: {}}
        get_dealer_info(url=url,
                        data_return=data_return,
                        dealer_id=dealer_id)
        assert dealer_id in data_return
        expected_keys = ['dealerId', 'error_message']
        for key in expected_keys:
            assert key in data_return.get(dealer_id)
            if key == 'dealerId':
                assert data_return.get(dealer_id).get(key) == dealer_id
            if key == 'error_message':
                assert data_return.get(dealer_id).get(key) == expected_error

    # good test
    @mock.patch('cox_auto_app.data_collection.get_json_request')
    def test_good_return(self, mock_get):
        data_set_id = '7'
        dealer_id = 8
        url = ('https://vautointerview.azurewebsites.net/api/{}/dealers/{}'
               .format(data_set_id, dealer_id))
        json_data = {'name': 'test',
                     'dealerId': 1}
        mock_get.return_value = json_data
        data_return = {dealer_id: {}}
        get_dealer_info(url=url,
                        data_return=data_return,
                        dealer_id=dealer_id)
        assert dealer_id in data_return
        assert data_return.get(dealer_id) == json_data
