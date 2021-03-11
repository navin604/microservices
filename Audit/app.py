import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())



def get_auto_pilot_reading(index):
    """ Get AP Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                            app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving AutoPilot at index %d" % index)
    arr1 = []
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'AutoPilot':
                arr1.append(msg)
        event = arr1[index]
        return event, 200
    except:
        logger.error("No more messages found")

    logger.error("Could not find AP at index %d" % index)
    return { "message": "Not Found"}, 404




def get_auto_brake_reading(index):
    """ Get AB Reading in History """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                            app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True,
    consumer_timeout_ms=1000)
    logger.info("Retrieving Autobrake at index %d" % index)
    arr2 = []
    print('prior to for loop')
    try:
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'AutoBrake':
                arr2.append(msg)
        event = arr2[index]
        return event, 200

    except:
        logger.error("No more messages found")

    logger.error("Could not find BP at index %d" % index)
    return { "message": "Not Found"}, 404










app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8110)