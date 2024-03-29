
from iss_tracker import speed_calculator, download_iss_data, xml_data_parser, get_stateVector, location_info, specific_epoch_speed, calculate_closest_datapoint_to_now
import requests
import pytest
from datetime import datetime


'''
General functions:
'''

# Testing function for speed calc
def test_speed_calculator():
    assert speed_calculator(1,2,3) == 3.7416573867739413

# Fixture for sample data
@pytest.fixture
def sample_xml_data(): 
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<ndm>
    <oem id="CCSDS_OEM_VERS" version="2.0">
        <header>
            <CREATION_DATE>2024-068T18:36:27.254Z</CREATION_DATE>
            <ORIGINATOR>JSC</ORIGINATOR>
        </header>
        <body>
            <segment>
                <metadata>
                    <OBJECT_NAME>ISS</OBJECT_NAME>
                    <OBJECT_ID>1998-067-A</OBJECT_ID>
                    <CENTER_NAME>EARTH</CENTER_NAME>
                    <REF_FRAME>EME2000</REF_FRAME>
                    <TIME_SYSTEM>UTC</TIME_SYSTEM>
                    <START_TIME>2024-068T12:00:00.000Z</START_TIME>
                    <STOP_TIME>2024-083T12:00:00.000Z</STOP_TIME>
                </metadata>
                <data>
                    <COMMENT>Units are in kg and m^2</COMMENT>
                    <stateVector>
                        <EPOCH>2024-068T12:00:00.000Z</EPOCH>
                        <X units="km">4</X>
                        <Y units="km">5</Y>
                        <Z units="km">6</Z>
                        <X_DOT units="km/s">7</X_DOT>
                        <Y_DOT units="km/s">8</Y_DOT>
                        <Z_DOT units="km/s">9</Z_DOT>
                    </stateVector>
                    <stateVector>
                        <EPOCH>2024-068T12:04:00.000Z</EPOCH>
                        <X units="km">1</X>
                        <Y units="km">2</Y>
                        <Z units="km">-3</Z>
                        <X_DOT units="km/s">4</X_DOT>
                        <Y_DOT units="km/s">5</Y_DOT>
                        <Z_DOT units="km/s">6</Z_DOT>
                    </stateVector>
                </data>
            </segment>
        </body>
    </oem>
</ndm>'''

BASE_URL = 'http://localhost:5000'


# Testing function for downloading ISS data successfully
def test_download_iss_data():
    assert download_iss_data() is not None

# Testing function for xml data parsing
def test_xml_data_parser(sample_xml_data):
    parsed_data = xml_data_parser(sample_xml_data)
    assert parsed_data['ndm']['oem']['body']['segment']['data']['stateVector'][0]['EPOCH'] == '2024-068T12:00:00.000Z'
    assert parsed_data['ndm']['oem']['body']['segment']['metadata']['OBJECT_NAME'] == 'ISS'
    assert parsed_data['ndm']['oem']['header']['CREATION_DATE'] == '2024-068T18:36:27.254Z'
    assert parsed_data['ndm']['oem']['body']['segment']['data']['COMMENT'] == 'Units are in kg and m^2'
    
# Testing function for getting state vector
def test_get_stateVector(sample_xml_data):
    parsed_sv = get_stateVector(sample_xml_data)
    assert parsed_sv[0]['EPOCH'] == '2024-068T12:00:00.000Z'
    assert parsed_sv[0]["X"]['#text'] == '4'
    assert parsed_sv[0]["Y"]['#text'] == '5'
    assert parsed_sv[0]["Z"]['#text'] == '6'
    assert parsed_sv[0]["X_DOT"]['#text'] == '7'
    assert parsed_sv[0]["Y_DOT"]['#text'] == '8'
    assert parsed_sv[0]["Z_DOT"]['#text'] == '9'

# Fixture returning sample epoch from sample data
@pytest.fixture
def epoch():
    return '2024-068T12:00:00.000Z'

# Testing function for location info
def test_location_info(epoch):
    assert location_info(epoch)['altitude'] == 434.1838505706133
    assert location_info(epoch)['latitude'] == -51.72659878401766
    assert location_info(epoch)['longitude'] == 12.962791887166693
    assert location_info(epoch)['geolocation'] == 'None'

# Testing function for specific epoch speed
def test_specific_epoch_speed(epoch):
    assert specific_epoch_speed(epoch) == '7.6516394881106065'

# Fixture for test datetime value
@pytest.fixture
def test_datetime():
    return datetime(2024, 3, 8, 12, 0, 0)

# Testing function for finding closest datapoint to test datetime value
def test_closest_datapoint_to_now(sample_xml_data, test_datetime):
    closest_index = calculate_closest_datapoint_to_now(sample_xml_data, test_datetime)
    assert closest_index == 0


'''
Routes:
'''
    
# Testing function for printing all epochs
def test_print_epochs():
    response = requests.get('http://localhost:5000/epochs')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Testing function for printing comment
def test_print_comment():
    response = requests.get('http://localhost:5000/comment')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Testing function for printing header
def test_print_header():
    response = requests.get('http://localhost:5000/header')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Testing function for printing metadata
def test_print_metadata():
    response = requests.get('http://localhost:5000/metadata')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Testing function for the /epochs?limit=int&offset=int route
def test_epochs_limit_offset_route():
    response = requests.get('http://localhost:5000/epochs?limit=5&offset=0')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 5

# Testing function for the /epochs/<epoch> route
def test_epochs_epoch_route():
    response1 = requests.get('http://localhost:5000/epochs')
    if response1.status_code == 200:
        epoch = response1.json()[0]['EPOCH']
        response2 = requests.get('http://localhost:5000/epochs/' + epoch)
        assert response2.status_code == 200
        assert isinstance(response2.json(), dict)

# Testing function for the /epochs/<epoch>/speed route
def test_epochs_epoch_speed_route():
    response1 = requests.get('http://localhost:5000/epochs')
    if response1.status_code == 200:
        epoch = response1.json()[0]['EPOCH']
        response2 = requests.get('http://localhost:5000/epochs/' + epoch + '/speed')
        assert response2.status_code == 200
        assert 'speed' in response2.json()

# Testing function for the /epochs/<epoch>/location route
def test_epochs_epoch_location_route():
    response1 = requests.get('http://localhost:5000/epochs')
    if response1.status_code == 200:
        epoch = response1.json()[0]['EPOCH']
        response2 = requests.get('http://localhost:5000/epochs/' + epoch + '/location')
        assert response2.status_code == 200
        assert 'latitude' in response2.json()
        assert 'longitude' in response2.json()
        assert 'altitude' in response2.json()
        assert 'geolocation' in response2.json()

# Testing function for the /now route
def test_now_route():
    response = requests.get('http://localhost:5000/now')
    assert response.status_code == 200
    assert 'latitude' in response.json()
    assert 'longitude' in response.json()
    assert 'altitude' in response.json()
    assert 'geolocation' in response.json()



    

