
# ISS Velocity Analysis

## Description

This project analyzes the velocity data of the International Space Station (ISS). The code fetches velocity data from a NASA API, calculates various metrics, and provides insights into the velocity patterns of the ISS.

## Data Source Description

The velocity data of the ISS is obtained from the NASA public data repository. The data is provided in XML format and contains velocity components in three dimensions (x, y, z) at various epochs.

To access the original data set, you can visit the following link:
[ISS Velocity Data](https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml)

## Building and Running the Container

To build and run the container for this code, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Navigate to the Directory**: Open a terminal or command prompt and navigate to the directory containing the project files.

3. **Build the Container**: Run the following command to build the Docker container:
   ```bash
   docker build -t iss-velocity-analysis .

4. **Run the Container**: Once the container is built, you can run it using the following command:
   ```bash
   docker run -it iss-velocity-analysis
5. Run the flask app, using python3 iss_tracker.py
6. Copy the link and curl it from another terminal, testing various commands. 

After running the container, the Python3 script will be executed, and various metrics related to the velocity of the ISS will be displayed in the console. Refer to the "Output and Interpretation" section for details on what to expect from the output.


## Output and Interpretation

Running the containerized Python3 script will output various metrics related to the velocity of the ISS. Here's what to expect:

Length of stateVector: Total number of velocity data points.
First and Last Epoch: Timestamps of the first and last data points.
Range of stateVector (days): Duration covered by the velocity data.
Current date and time: Current system date and time.
List of minute values within the current hour: Velocity data points within the current hour.
Closest value: Closest velocity data point to the current minute.
Closest value's index: Index of the closest velocity data point.
Instantaneous speed: Speed calculated from the closest velocity data point.
Average speed of ISS: Average speed calculated from all velocity data points.
The output provides insights into the velocity patterns of the ISS, helping to understand its movement in space.

Created using the help of ChatGPT
