from .data_collection import (get_dataset_id,
                              get_vehicle_ids)


def merge():
    data_set_id = get_dataset_id()
    vehicle_ids = get_vehicle_ids(data_set_id=data_set_id)
    return data_set_id, vehicle_ids
