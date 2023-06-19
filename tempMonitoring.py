"""This module is for is for retrieving temperature data from 1-wire DS18B20 Sensors
and storing them between update intervals.
"""
from w1thermsensor import W1ThermSensor, Unit, Sensor
import time 
from db.Database import Database


def updateDbForId(db, sensorId :str, processId:int) :
    DESC_INDEX = 2
    ID_INDEX = 0
    curs = db.con.cursor()
    sensorInfo = db.getSensorFromDb(sensorId)

    sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensorId)
    tempC = sensor.get_temperature()

    insertSQL = "INSERT into temp_readings (temperature_c, device_id, process_id) VALUES (%s, %s, %s)"
    value = (tempC, sensorInfo[ID_INDEX], processId)

    curs.execute(insertSQL, value)

    db.con.commit()

    print(f"For {sensorInfo[DESC_INDEX]} at {tempC}c.")
    print(curs.rowcount, "record inserted.")


def dbLoggingLoop(sensorId, processId, updateIntrvlSecs):
    db = Database()
    while True:
        updateDbForId(db,sensorId, processId)
        time.sleep(updateIntrvlSecs)