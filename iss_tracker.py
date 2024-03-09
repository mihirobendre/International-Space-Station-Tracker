
import requests
import xmltodict
import pprint
import logging
from datetime import datetime
import math
from flask import Flask, request

app = Flask(__name__)

def speed_calculator(x_vel, y_vel, z_vel):

    '''
    Calculate the magnitude of velocity (speed) given its components in three dimensions.

    Parameters:
    x_vel (float): The velocity component along the x-axis.
    y_vel (float): The velocity component along the y-axis.
    z_vel (float): The velocity component along the z-axis.

    Returns:
    float: The magnitude of velocity (speed) calculated using the Euclidean distance formula.
    '''

    speed = math.sqrt(x_vel**2 + y_vel**2 + z_vel**2)
    return speed

def get_data():
    #fetching and parsing the data

    """
    Fetches and parses International Space Station (ISS) coordinates data from NASA's public API.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the state vectors of the ISS at different epochs.
                               Each dictionary represents the state vector data for a specific epoch.
    """

    response = requests.get(url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    status_code = response.status_code

    if status_code == 200:
        logger.info("Successfully fetched data")
    else:
        logger.error("Failed to fetch data")

    full_data_xml = response.content

    full_data_dicts = xmltodict.parse(full_data_xml)

    # now, printing statement about the range of data from 1st and last epochs
    stateVector = full_data_dicts['ndm']['oem']['body']['segment']['data']['stateVector']

    return stateVector

@app.route('/epochs', methods = ['GET'])
def epochs_general():
    """
    Retrieves ISS coordinates data for a specified range of epochs.

    Args:
        offset (int): The starting index of the data to be returned (default is 0).
        limit (int): The maximum number of data points to be returned (default is the length of the data).

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the ISS coordinates data for the specified range of epochs.
    """

    data = get_data()
    
    offset = request.args.get('offset', 0)
    try:
        offset = int(offset)
    except ValueError:
        return "Invalid start parameter; start must be an integer.\n"

    limit = request.args.get('limit', len(data))

    try:
        limit = int(limit)
    except ValueError:
        return "Invalid limit parameter; limit must be an integer.\n"

    return_data = []
    counter = 0
    
    result = []
    for item in data:
        if data.index(item) >= offset:
            result.append(item)
            counter += 1
            if counter >= limit:
                return(result)
    
    return data

@app.route('/comment', methods = ['GET'])
def print_comment():
    response = requests.get(url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    status_code = response.status_code

    if status_code == 200:
        logger.info("Successfully fetched data")
    else:
        logger.error("Failed to fetch data")

    full_data_xml = response.content

    full_data_dicts = xmltodict.parse(full_data_xml)

    # now, printing statement about the range of data from 1st and last epochs
    comment = full_data_dicts['ndm']['oem']['body']['segment']['data']['COMMENT']

    return comment

@app.route('/header', methods = ['GET'])
def print_header():
    response = requests.get(url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    status_code = response.status_code

    if status_code == 200:
        logger.info("Successfully fetched data")
    else:
        logger.error("Failed to fetch data")

    full_data_xml = response.content

    full_data_dicts = xmltodict.parse(full_data_xml)

    # now, printing statement about the range of data from 1st and last epochs
    header = full_data_dicts['ndm']['oem']['header']
    return header

@app.route('/metadata', methods = ['GET'])
def print_metadata():
    response = requests.get(url = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    status_code = response.status_code

    if status_code == 200:
        logger.info("Successfully fetched data")
    else:
        logger.error("Failed to fetch data")

    full_data_xml = response.content

    full_data_dicts = xmltodict.parse(full_data_xml)

    # now, printing statement about the range of data from 1st and last epochs
    metadata = full_data_dicts['ndm']['oem']['body']['segment']['metadata']

    return metadata

@app.route('/epochs/<epoch>',methods = ['GET'])
def specific_epoch(epoch):
    
    """
    Retrieves ISS coordinates data for a specific epoch.

    Args:
        epoch (str): The epoch for which the ISS coordinates data is requested.

    Returns:
        Union[Dict[str, Any], str]: A dictionary containing the ISS coordinates data for the specified epoch,
                                    or a string indicating that the epoch was not found.
    """

    data = get_data()
    for item in data:
        if item["EPOCH"] == epoch:
            return item

    return "Epoch not found"

@app.route('/epochs/<epoch>/speed',methods = ['GET'])
def specific_epoch_speed(epoch):
    """
    Retrieves the speed of the ISS for a specific epoch.

    Args:
        epoch (str): The epoch for which the ISS speed is requested.

    Returns:
        Union[str, Response]: A string representation of the speed of the ISS for the specified epoch,
                              or a string indicating that the epoch was not found.
    """

    data = get_data()
    for item in data:
        if item["EPOCH"] == epoch:
            x_vel = float(item['X_DOT']['#text'])
            y_vel = float(item['Y_DOT']['#text'])
            z_vel = float(item['Z_DOT']['#text'])
            speed = speed_calculator(x_vel, y_vel, z_vel)
            return str(speed) + '\n'

    return "Epoch not found"


@app.route('/now',methods = ['GET'])
def epoch_and_speed_now():
    """
    Calculates the closest epoch to the current time and the instantaneous speed at that epoch.

    Args:
        stateVector (List[Dict[str, Any]]): A list of dictionaries containing state vector data.

    Returns:
        str: A string representing the closest epoch to the current time and the instantaneous speed at that epoch.
    """

    stateVector = get_data()

    # then, print full epoch closest to now
    current_date = datetime.now().date()
    print("Current date: ", current_date)

    # Specific date
    year_first_day = datetime(datetime.now().year, 1, 1)

    # Current date
    current_date_and_time = datetime.now()
    print("Current date and time: ", current_date_and_time)
    current_hour = int(str(current_date_and_time)[11:13])
    current_min = int(str(current_date_and_time)[14:16])

    print("Current hour: ", current_hour)
    print("Current minute: ", current_min)

    # printing statement about range of data, using timestamps from first and last epochs
    # Calculate the difference in days
    days_since_start_of_year = int((current_date_and_time - year_first_day).days)

    print("Number of days since start of year:", days_since_start_of_year)
    current_day = days_since_start_of_year + 1

    list_of_minutes = []
    
    for instance in stateVector:
        epoch_string = instance['EPOCH']
        day_number = int(epoch_string[5:8])
        hour = int(epoch_string[9:11])
        minute = int(epoch_string[12:14])

        if day_number == current_day:
            if hour == current_hour:
                list_of_minutes.append({'minute_val':minute, 'index':stateVector.index(instance)})

    closest_value = None
    closest_value_index = None
    min_difference = float('inf')
    
    print("List of minutes: ")
    pprint.pprint(list_of_minutes)

    for value in list_of_minutes:
        min_in_list = value['minute_val']
        index_of_min_in_list = value['index']
        difference = abs(min_in_list - current_min)
        if difference < min_difference:
            min_difference = difference
            closest_value = min_in_list
            closest_value_index = index_of_min_in_list


    print("Closest value: ", closest_value)

    print("Closest value's index: ", closest_value_index)

    #instantaneous speed:

    x_dot_inst = float(stateVector[closest_value_index]['X_DOT']['#text'])
    y_dot_inst = float(stateVector[closest_value_index]['Y_DOT']['#text'])
    z_dot_inst = float(stateVector[closest_value_index]['Z_DOT']['#text'])

    speed_inst = speed_calculator(x_dot_inst, y_dot_inst, z_dot_inst)
    ret_speed_string = "Instantaneous speed at closest epoch: " + str(speed_inst)
    ret_epoch = "Closest epoch to now: " + str(stateVector[closest_value_index])

    return ret_epoch + '\n' + ret_speed_string + '\n'

#configure logging
logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
