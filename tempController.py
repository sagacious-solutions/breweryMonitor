from w1thermsensor import W1ThermSensor, Sensor
from db.Database import Database
import time

def temperatureControlLoop(ctrlCnfg):
    db = Database()
    checkIntervalSecs = ctrlCnfg["checkIntervalSecs"]
    sensorId= ctrlCnfg["sensorId"]
    cool = ("cool" in ctrlCnfg and ctrlCnfg["cool"])
    heat = ("heat" in ctrlCnfg and ctrlCnfg["heat"])
    sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensorId)
    control_event = None

    if heat :
        raise Exception("Theres currently no heating logic.")

    while True :
        tempC = sensor.get_temperature()
        
        if(cool and tempC > ctrlCnfg["targetTemp"] + ctrlCnfg["tempDifference"]):
            checkIntervalSecs = 1
            if not control_event :
                control_event = createNewControlEventInDb(db, tempC, **ctrlCnfg)

        print(tempC)
        time.sleep(checkIntervalSecs)

def createNewControlEventInDb(db, currentTemp, targetTemp, processId, heat, cool, sensorId, **kwargs):    
    dbSensorId = db.getSensorFromDb(sensorId)[0]

    print(dbSensorId)

    curs = db.con.cursor()
    insertSQL = """
    INSERT INTO temp_controller_events (process_id, temp_start, target_temp, heat, cool, sensor_id) 
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    values = (processId, currentTemp, targetTemp, heat, cool, dbSensorId)

    curs.execute(insertSQL, values)
    db.con.commit()

    print(curs.rowcount, "record inserted for new control event.")
    return curs.lastrowid