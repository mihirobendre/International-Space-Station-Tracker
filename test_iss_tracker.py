
from iss_tracker import speed_calculator, download_iss_data, xml_data_parser, get_stateVector, location_info, specific_epoch_speed, calculate_closest_datapoint_to_now
#from flask import jsonify
import pytest

def test_speed_calculator():
    assert speed_calculator(1,2,3) == 3.7416573867739413

var_a = 1

sample_xml_data =  '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
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
                        <EPOCH>2024-068T12:04:00.000Z</EPOCH>
                        <X units="km">3981.1591172114599</X>
                        <Y units="km">1817.4273840374899</Y>
                        <Z units="km">-5202.0706291529305</Z>
                        <X_DOT units="km/s">-1.5956939400996299</X_DOT>
                        <Y_DOT units="km/s">7.3610565465317999</Y_DOT>
                        <Z_DOT units="km/s">12</Z_DOT>
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
    assert parsed_data['ndm']['oem']['body']['segment']['data']['stateVector'] == '2024-068T12:04:00.000Z'
    #['oem']['body']['segment']['data']['stateVector'][0]['EPOCH']

'''
    assert len(parsed_data) == 2
    assert isinstance(parsed_data[0], dict)
    assert parsed_data[0]["EPOCH"] == '2024-045T12:04:00.000Z'
    assert parsed_data[0]["X"] == 100.0
    assert parsed_data[0]["Y"] == 200.0
    assert parsed_data[0]["Z"] == 300.0
    assert parsed_data[0]["X_DOT"] == 1.0
    assert parsed_data[0]["Y_DOT"] == 2.0
    assert parsed_data[0]["Z_DOT"] == 3.0
'''