import mock
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
