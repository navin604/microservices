import mysql.connector

db_conn = mysql.connector.connect(host="kafkalab6.eastus2.cloudapp.azure.com", user="root", password = "Passwordf8785", database = "events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          CREATE TABLE auto_pilot
          (id INT NOT NULL AUTO_INCREMENT, 
           vehicle_id VARCHAR(250) NOT NULL,
           time VARCHAR(250) NOT NULL,
           location VARCHAR(250) NOT NULL,
           speed_at_enable INT NOT NULL,
           weather_data VARCHAR(100) NOT NULL,
           follow_distance VARCHAR(100) NOT NULL,
           highway VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT auto_pilot_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE auto_brake
          (id INT NOT NULL AUTO_INCREMENT, 
           vehicle_id VARCHAR(250) NOT NULL,
           time VARCHAR(250) NOT NULL,
           location VARCHAR(250) NOT NULL,
           speed_at_enable INTEGER NOT NULL,
           weather_data VARCHAR(100) NOT NULL,
           follow_distance VARCHAR(100) NOT NULL,
           highway VARCHAR(100) NOT NULL,
           engaged VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT auto_brake_pk PRIMARY KEY(id))
          ''')

db_conn.commit()
db_conn.close()
