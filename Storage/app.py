import connexion
from connexion import NoContent
from mysql import connector
import pymysql
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
from base import Base
from auto_pilot import AutoPilot
from auto_brake import AutoBrake
import datetime
import yaml
import logging
import logging.config
logger = logging.getLogger('basicLogger')

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

logger.info(f"Connecting to DB. Hostname:{app_config['datastore']['hostname']}, Port: {app_config['datastore']['port']}")

DB_ENGINE = create_engine(f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)


def get_auto_pilot(timestamp):
    """ Gets new auto pilot reading after the timestamp """
    print(timestamp)
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(AutoPilot).filter(AutoPilot.date_created >=
    timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Auto Pilot readings after %s returns %d results" %
    (timestamp, len(results_list)))

    return results_list, 200


def get_auto_brake(timestamp):
    """ Gets new auto brake reading after the timestamp """
    print(timestamp)
    session = DB_SESSION()
    print(timestamp)
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    print(timestamp_datetime)
    readings = session.query(AutoBrake).filter(AutoBrake.date_created >=
                                               timestamp_datetime)
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for Auto Brake readings after %s returns %d results" %
                (timestamp, len(results_list)))

    return results_list, 200


def process_messages():
    """ Process event messages """

    hostname = "%s:%d" % (app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).

    consumer = topic.get_simple_consumer(consumer_group=b'event_group', reset_offset_on_start=False, auto_offset_reset=OffsetType.LATEST)

    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        
        payload = msg["payload"]
        

        if msg["type"] == "AutoPilot":
            id = payload['vehicle_id']
            session = DB_SESSION()
            ap = AutoPilot(payload['vehicle_id'],
                           payload['time'],
                           payload['location'],
                           payload['speed_at_enable'],
                           payload['highway'],
                           payload['weather_data'],
                           payload['follow_distance'])


            session.add(ap)

            session.commit()
            session.close()

            logger.info(f'Stored event {logger.name} request with a unique id of {id}')

            return NoContent, 201
        elif msg["type"] == "AutoBrake":
            """ Receives an autobrake reading """
            
            session = DB_SESSION()
            id = payload['vehicle_id']

            ab = AutoBrake(payload['time'],
                           payload['location'],
                           payload['speed_at_enable'],
                           payload['highway'],
                           payload['weather_data'],
                           payload['follow_distance'],
                           payload['vehicle_id'],
                           payload['engaged'])

            session.add(ab)

            session.commit()
            session.close()
            logger.debug(f'Stored event {logger.name} request with a unique id of {id}')
            return NoContent, 201

        # Commit the new message as being read
        consumer.commit_offsets()



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)





if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
