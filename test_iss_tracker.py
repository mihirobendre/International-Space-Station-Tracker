
from iss_tracker import speed_calculator, download_iss_data, xml_data_parser, get_stateVector, location_info, specific_epoch_speed, calculate_closest_datapoint_to_now
#from flask import jsonify
import pytest

def test_speed_calculator():
    assert speed_calculator(1,2,3) == 3.7416573867739413

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


def test_download_iss_data():
    assert download_iss_data() is not None

def test_xml_data_parser():
    parsed_data = xml_data_parser(sample_xml_data)
    assert parsed_data['ndm']['oem']['body']['segment']['data']['stateVector'][0]['EPOCH'] == '2024-068T12:00:00.000Z'
    assert parsed_data['ndm']['oem']['body']['segment']['metadata']['OBJECT_NAME'] == 'ISS'
    assert parsed_data['ndm']['oem']['header']['CREATION_DATE'] == '2024-068T18:36:27.254Z'
    assert parsed_data['ndm']['oem']['body']['segment']['data']['COMMENT'] == 'Units are in kg and m^2'
    
def test_get_stateVector():
    parsed_sv = get_stateVector(sample_xml_data)
    assert parsed_sv[0]['EPOCH'] == '2024-068T12:00:00.000Z'
    assert parsed_sv[0]["X"]['#text'] == '4'
    assert parsed_sv[0]["Y"]['#text'] == '5'
    assert parsed_sv[0]["Z"]['#text'] == '6'
    assert parsed_sv[0]["X_DOT"]['#text'] == '7'
    assert parsed_sv[0]["Y_DOT"]['#text'] == '8'
    assert parsed_sv[0]["Z_DOT"]['#text'] == '9'

@pytest.fixture
def epoch():
    return '2024-068T12:00:00.000Z'

def test_location_info(epoch):
    assert location_info(epoch) == 'Hello World'
