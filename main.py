import requests
from datetime import datetime
import redis
import json
import logging

r = redis.Redis()
r.ping()


# Listens to Pushes made to Redis
def listen():
    print("Listening for messages on Releases Queue...")
    while True:
        data = r.brpop("releases")
        try:
            json_data = parse_json(data[1].decode("UTF-8"))
            if json_data is not None:
                send_to_timeline(json_data.get("service_name"), json_data.get("version"), json_data.get("environment"))
        except Exception as e:
            r.rpush("releases", data)
            logging.exception("Exception in listen(): ", e)


# Parses Json and catches failures
def parse_json(data):
    try:
        json_data = json.loads(data)
        json_dict = {
            "service_name": json_data["microservice"],
            "version": json_data["microservice_version"],
            "environment": json_data["environment"]
        }
        return json_dict

    except json.JSONDecodeError:
        logging.exception("Failed to parse JSON")
        return None


# Sends to Catalogue-Timeline API
def send_to_timeline(service_name, version, environment):
    api_url = "http://localhost:2000/catalogue-timeline/insert"
    requests.post(url=api_url, json=payload(service_name, version, environment))


# Builds PayLoad for Catalogue-Timeline-API
def payload(service_name, version, environment):
    now = datetime.now()

    api_data = {
        "service": service_name,
        "date": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "environment": environment,
        "eventType": "deployment",
        "message": "Deployed Version: " + version
    }
    return api_data


if __name__ == '__main__':
    listen()

