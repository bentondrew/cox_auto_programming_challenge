from .data_collection import (get_dataset_id,
                              get_vehicle_ids,
                              get_data_for_vehicles)


def merge():
    data_set_id = get_dataset_id()
    vehicle_ids = get_vehicle_ids(data_set_id=data_set_id)
    dealer_list, error_list = get_data_for_vehicles(data_set_id=data_set_id,
                                                    vehicle_ids=vehicle_ids)
    return data_set_id, vehicle_ids, dealer_list, error_list
