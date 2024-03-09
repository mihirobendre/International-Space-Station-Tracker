
from iss_tracker import speed_calculator

import pytest

def test_speed_calculator():
    assert speed_calculator(1,2,3) == 3.7416573867739413
