import gpio as GPIO
import json

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
        pinCnfg["onState"] = GPIO.LOW if pinCnfg["triggerLow"] else GPIO.HIGH
        pinCnfg["offState"] = GPIO.HIGH if pinCnfg["triggerLow"] else GPIO.LOW
        _setPin(pinCnfg, pinCnfg["defaultState"])
    

def testTempController(cntrlCnfg, triggerOn):
    initPins(cntrlCnfg)

    setPins(cntrlCnfg, triggerOn)                

def loadConfig(filepath) :
     with open(filepath) as file :
        return json.load(file)

CONFIG_JSON_PATH = './config.json'

cntrlCnfgs = loadConfig(CONFIG_JSON_PATH)

# print(cntrlCnfgs["control_temps"])

testTempController(cntrlCnfgs["control_temps"][0], triggerOn=False)
testTempController(cntrlCnfgs["control_temps"][1], triggerOn=False)