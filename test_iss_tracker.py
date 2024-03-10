
from iss_tracker import speed_calculator, fetch_all_data, get_stateVector, location_info, specific_epoch_speed, calculate_closest_datapoint_to_now

import pytest

def test_speed_calculator():
    assert speed_calculator(1,2,3) == 3.7416573867739413

def test_fetch_all_data():
    fetched_data = fetch_all_data()
    assert len(fetched_data) == 1
    assert isinstance(fetched_data[0], dict)





