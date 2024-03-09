FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

RUN pip3 install pytest==8.0.0

COPY iss_tracker.py iss_tracker.py

RUN chmod +rx iss_tracker.py

ENV PATH="/code:$PATH"
