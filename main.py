from tempMonitoring import dbLoggingLoop
from tempController import temperatureControlLoop
import time
import json
from multiprocessing import Process
from logger import Logger
from setGpioPermissions import setPermissions

CONFIG_JSON_PATH = './config.json'

mainLog = Logger('main')
mainLog.initLogFile()

def loadConfig(filepath) :
     with open(filepath) as file :
        return json.load(file)

config = loadConfig(CONFIG_JSON_PATH)

def logTemperatureToDb():
    pass

def startTemperatureLogging():
    processes = []

    for recConf in config["record_temps"] :
        mainLog.log.info(f'Starting temperature monitoring loop.\n{recConf}')
        loggingProcess = Process(target=dbLoggingLoop, kwargs=recConf)
        loggingProcess.start()
        processes.append(loggingProcess)
        time.sleep(5)

    return processes

def startTemperatureControllers():
    processes = []

    for controlConfig in config["control_temps"] :
        mainLog.log.info(f'Starting temperature control loop.\n{controlConfig}')
        ctrlProcess = Process(target=temperatureControlLoop, args=[controlConfig])
        ctrlProcess.start()
        processes.append(ctrlProcess)
        time.sleep(5)

    return processes

def main():
    setPermissions()
    allProcesses = startTemperatureLogging()
    allProcesses = startTemperatureControllers()

    try :
        while True :
            time.sleep(60)
    finally :
        for process in allProcesses :
            process.terminate()
            process.join()


if __name__ == "__main__" :
    mainLog.log.info('Program Starting.')
    main()