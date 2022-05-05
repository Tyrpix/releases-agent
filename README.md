# Releases Agent

## Description
- Simulates AWS deployer releases that send POST requests.
- Requests are sent to the Redis Queue.
- This agent pops the data from the queue and creates a PayLoad.
- Payload is formatted according to the Catalogue-Timeline API Documentation.
- Using a simple queue allows for data to not be lost if the API is down.

## Getting Started


### Dependencies
- Python 3
- [catalogue-timeline](https://github.com/hmrc/catalogue-timeline)
- [Redis](https://pypi.org/project/redis/)
- [Requests](https://docs.python-requests.org/en/latest/)


### Installation
- pip install redis
- pip install requests


### Usage
Run the application, and it will listen for messages sent to the
"releases" Redis queue. A Payload will be created from the message
and sent to the catalogue-timeline API.