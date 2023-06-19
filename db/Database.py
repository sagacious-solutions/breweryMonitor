import mysql.connector
import json

CREDS_JSON_PATH = './creds/dbConfig.json'

class Database :
    def __init__ (self):
        with open(CREDS_JSON_PATH) as file :
            dbConfig = json.load(file)
            self.con = mysql.connector.connect(**dbConfig)

    def getSensorFromDb(self, sensorId: str) :
        getDeviceDbId = f"""
        SELECT * FROM temp_sensors
            WHERE sensor_id='{sensorId}'
        """

        curs = self.con.cursor()
        curs.execute(getDeviceDbId)
        result = curs.fetchall()

        if not len(result) :
            raise Exception(f'No record found for sensor {sensorId} in database.')
        
        return result[0]