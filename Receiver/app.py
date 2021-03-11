import os
import json
import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
import datetime
import json
from pykafka import KafkaClient
headerInfo = {'content-type': 'application/json'}
logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

def auto_pilot(body):
    id = body['vehicle_id']
    logger.info(f'Received event {logger.name} request with a unique id of {id}')

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "AutoPilot",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    print('PRIOT')
    producer.produce(msg_str.encode('utf-8'))
    print('AFTER')

    logger.info(f'Received event {logger.name} response (Id:{id}) with status 201')
    return NoContent, 201

def auto_brake(body):
    id = body['vehicle_id']
    logger.info(f'Received event {logger.name} request with a unique id of {id}')

    client = KafkaClient(hosts=f"{app_config['events']['hostname']}:{app_config['events']['port']}")
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()
    msg = {"type": "AutoBrake",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f'Received event {logger.name} response (Id:{id}) with status 201')
    return NoContent, 201



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)



if __name__ == "__main__":
    app.run(port=8080)