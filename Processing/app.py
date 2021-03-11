import connexion
from connexion import NoContent
from mysql import connector
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import datetime
import yaml
import os
import datetime
import json
import logging
import requests
import logging.config
logger = logging.getLogger('basicLogger')
from apscheduler.schedulers.background import BackgroundScheduler




with open('app_conf.yml', 'r') as f:
 app_config = yaml.safe_load(f.read())


with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


def get_stats():
    logger.info("Stats Request Has Started")
    if not os.path.isfile(app_config['datastore']['filename']):
        logger.error("Statistics do not exist")
        return "Statistics do not exist", 404
    else:
            with open ('data.json') as json_file:
                data = json.load(json_file)
            logger.debug(data)
            logger.info("Stats Request Has Finised")
            return data, 200



def populate_stats():
    """ Periodically update stats """
    logger.info("Starting Periodic Processing")
    if not os.path.isfile(app_config['datastore']['filename']):
        num_ap_readings = 0
        speed_ap_readings = 0
        num_ab_readings = 0
        speed_ab_readings = 0
        last_updated = '2016-08-29T09:12:33Z'
    else:
        with open(app_config['datastore']['filename']) as f:
            data = json.load(f)
            last_updated = data['last_updated']


    date = datetime.datetime.now()
    autopilot = requests.get('http://localhost:8090/auto-pilot?timestamp=' + last_updated)
    if autopilot.status_code != 200:
        logger.error('Status Code not 200')
    autobrake = requests.get('http://localhost:8090/auto-pilot?timestamp=' + last_updated)
    if autobrake.status_code != 200:
        logger.error('Status Code not 200')
    dic = {}
    ap_data = autopilot.json()
    print(ap_data)
    ab_data = autobrake.json()
    print(ab_data)
    logger.info(len(ap_data) + len(ab_data))
    if not os.path.isfile(app_config['datastore']['filename']):
        if len(ap_data) == 0:
            dic['num_ap_readings'] = 0
            dic['speed_ap_readings'] = 0
        else:
            dic['num_ap_readings'] = len(ap_data)
            dic['speed_ap_readings'] = max(item['speed_at_enable'] for item in ap_data)

        if len(ab_data) == 0:
            dic['num_ab_readings'] = 0
            dic['speed_ab_readings'] = 0
        else:
            dic['num_ab_readings'] = len(ab_data)
            dic['speed_ab_readings'] = max(item['speed_at_enable'] for item in ab_data)

        dic['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(app_config['datastore']['filename'], 'w') as outfile:
            json.dump(dic, outfile)
        logger.debug(dic)
        logger.info("Ending Periodic Processing")
    else:
        with open('data.json') as json_file:
            data = json.load(json_file)
            if len(ap_data) == 0:
                data['num_ap_readings'] = 0
                data['speed_ap_readings'] = 0

            else:
                data['num_ap_readings'] = len(ap_data)
                data['speed_ap_readings'] = max(item['speed_at_enable'] for item in ap_data)

            if len(ab_data) == 0:
                data['num_ab_readings'] = 0
                data['speed_ab_readings'] = 0
            else:
                data['num_ab_readings'] = len(ab_data)
                data['speed_ab_readings'] = max(item['speed_at_enable'] for item in ab_data)

            data['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            with open(app_config['datastore']['filename'], 'w') as outfile:
                json.dump(data, outfile)
            logger.debug(data)
            logger.info("Ending Periodic Processing")









def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sched.start()



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100, use_reloader=False)