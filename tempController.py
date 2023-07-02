from w1thermsensor import W1ThermSensor, Sensor
from db.Database import Database
import time
import gpio as GPIO
from datetime import datetime, timedelta

def setPins(cntrlCnfg, triggerOn):
    for pinCnfg in cntrlCnfg["coolingPins"] :
        _setPin(pinCnfg, triggerOn)

def _setPin(pinCnfg: object, triggerOn: bool):
    """Sets pin to high or low based on pin config and passed boolean

    Args:
        pinCnfg (object): Pin configuration
        triggerOn (bool): Set to on state if true
    """
    if triggerOn :
        GPIO.output(pinCnfg["pin"], pinCnfg["onState"])
        return
    
    GPIO.output(pinCnfg["pin"], pinCnfg["offState"])    

def initPins(cntrlCnfg): 
    for pinCnfg in cntrlCnfg["coolingPins"] :
        GPIO.setup(pinCnfg["pin"], GPIO.OUT)
        print(pinCnfg["triggerLow"] )
        pinCnfg["onState"] = GPIO.LOW if pinCnfg["triggerLow"] else GPIO.HIGH
        pinCnfg["offState"] = GPIO.HIGH if pinCnfg["triggerLow"] else GPIO.LOW
        _setPin(pinCnfg, pinCnfg["defaultState"])
    
def _delayStartHasPassed(delayStartUntil):
    return datetime.now() > delayStartUntil

def temperatureControlLoop(cntrlCnfg):
    db = Database()
    checkIntervalSecs = cntrlCnfg["checkIntervalSecs"]
    sensorId= cntrlCnfg["sensorId"]
    cool = ("cool" in cntrlCnfg and cntrlCnfg["cool"])
    heat = ("heat" in cntrlCnfg and cntrlCnfg["heat"])
    sensor = W1ThermSensor(sensor_type=Sensor.DS18B20, sensor_id=sensorId)
    controlEventId = None
    delayStartUntil = datetime.now() + timedelta(minutes=cntrlCnfg["delayStartMins"])

    if heat :
        raise Exception("Theres currently no heating logic.")

    initPins(cntrlCnfg)

    while True :
        tempC = sensor.get_temperature()
        
        # delay start has 
        if(cool and (datetime.now() > delayStartUntil)
             and tempC > cntrlCnfg["targetTemp"] + cntrlCnfg["tempDifference"]):            
            checkIntervalSecs = 1
            if not controlEventId :
                controlEventId = createNewControlEventInDb(db, tempC, **cntrlCnfg)
                setPins(cntrlCnfg, triggerOn=True)                
            
        # Clear control event and turn off cooler, update original event in db
        if controlEventId and tempC < cntrlCnfg["targetTemp"] :
            updateExistingEvent(db, controlEventId, tempC)
            controlEventId = None
            setPins(cntrlCnfg, triggerOn=False)                
            delayStartUntil = datetime.now() + timedelta(minutes=cntrlCnfg["delayStartMins"])
            checkIntervalSecs = cntrlCnfg["checkIntervalSecs"]

        print(tempC)
        time.sleep(checkIntervalSecs)

def createNewControlEventInDb(db, currentTemp, targetTemp, processId, heat, cool, sensorId, **kwargs):    
    dbSensorId = db.getSensorFromDb(sensorId)[0]

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

def updateExistingEvent(db, controlEventId, currentTemp, **kwargs):
    curs = db.con.cursor()
    updateSQL = f"""
    UPDATE temp_controller_events tce
        SET event_stop=CURRENT_TIMESTAMP, temp_finish={currentTemp}
        WHERE id={controlEventId}
    """

    curs.execute(updateSQL)
    db.con.commit()

    print(curs.rowcount, " updated record for finished control event.")