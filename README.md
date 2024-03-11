# ISS Tracker

## Project Objective

The goal of the ISS Tracker project is to develop a Flask web application that provides real-time tracking and analysis of the International Space Station (ISS). It achieves this by fetching live data from NASA's public repository, parsing the XML data, and calculating metrics such as the ISS's current speed and geographic position.

## Contents

- **Dockerfile**: Setup for the Docker environment.
- **docker-compose.yml**: Configuration for Docker Compose.
- **iss_tracker.py**: The main script for ISS tracking and analysis.
- **requirements.txt**: Lists the necessary Python packages.
- **test/**: Folder containing unit tests.
  - **test_iss_tracker.py**: Script for unit testing the main application.
- **diagram.png**: Diagram illustrating the project's system architecture.
- **README.md**: Documentation providing details and setup instructions for the project.

## Instructions

### 1. Accessing the Data

ISS data can be accessed through NASA's public data repository. The provided URL directs to an XML file with the ISS's position and velocity information, available in the Mean of J2000 (J2K) frame and updated every four minutes across a span of 15 days.

### 2. Building the Container

To containerize the ISS Tracker, follow these steps:
1. Ensure Docker is installed on your machine.
2. Use a terminal to navigate to the directory with the Dockerfile and Python scripts.
3. Execute `docker-compose up -d` to build the Docker image and start the Flask app in the background.
4. Confirm the container is running on port 5000 using `docker ps -a` and list all Docker images with `docker images`.

### 3. Running Unit Tests

To perform unit tests within the Docker container, use:
```bash
docker exec -it iss_tracker /bin/bash

### 4. Accessing the Routes

The Flask application supports various routes for interacting with the ISS data:

GET /now: Current epoch's speed and position.
GET /epochs: Access to the full dataset.
GET /epochs?limit=int&offset=int: Dataset access with pagination.
GET /epochs/<epoch>: Data for a specific epoch.
GET /epochs/<epoch>/speed: Speed at a given epoch.
GET /epochs/<epoch>/location: Geolocation data for an epoch. May return "Address Not Found" over oceans.

### 5. Free-up space

To remove the Docker container and free up resources, run bash command:
```bash
docker-compose down
Verify removal with docker ps -a.

## Interpretation of outputs
The application's output provides insights into the ISS's location, speed, and trajectory, enabling users to track its movement in real time.

## Acknowledgments
This project uses NASA's public data and some parts of the code, and this README file include contributions from ChatGPT by OpenAI for documentation and code comments. The geodetic calculations have been verified using an online tracker.

