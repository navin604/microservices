import mysql.connector
db_conn = mysql.connector.connect(host="kafkalab6.eastus2.cloudapp.azure.com", user="root", password = "Passwordf8785", database = "events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE auto_pilot, auto_brake
''')
db_conn.commit()
db_conn.close()