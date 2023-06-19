from tempMonitoring import dbLoggingLoop
from tempController import temperatureControlLoop
import time
import json
from multiprocessing import Process, Manager, Value

CONFIG_JSON_PATH = './config.json'


def loadConfig(filepath) :
     with open(filepath) as file :
        return json.load(file)

config = loadConfig(CONFIG_JSON_PATH)

def logTemperatureToDb():
    pass

def startTemperatureLogging():
    processes = []

    for recConf in config["record_temps"] :
        loggingProcess = Process(target=dbLoggingLoop, kwargs=recConf)
        loggingProcess.start()
        processes.append(loggingProcess)
        time.sleep(5)

    return processes

def startTemperatureControllers():
    processes = []

    for controlConfig in config["control_temps"] :
        ctrlProcess = Process(target=temperatureControlLoop, args=[controlConfig])
        ctrlProcess.start()
        processes.append(ctrlProcess)
        time.sleep(5)

    return processes

def main():
    # allProcesses = startTemperatureLogging()
    allProcesses = startTemperatureControllers()

    try :
        while True :
            time.sleep(60)
    finally :
        for process in allProcesses :
            process.terminate()
            process.join()


if __name__ == "__main__" :
    main()