import logging
from datetime import datetime
from pathlib import Path

class Logger :
    def __init__(self, name):
        self.name = name

        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.initStream()

    def initStream(self):
        # Create a stream handler and set the log level
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        self.log.addHandler(stream_handler)
        stream_handler.setFormatter(self.formatter)

    def initLogFile(self):
        current_date = datetime.now().date()
        logPathDir = Path.cwd() / 'logs' 

        logPathDir.mkdir(exist_ok=True, parents=True)
        logPath = logPathDir / f'{self.name}-{current_date}.log'

        # Create a file handler and set the log level
        file_handler = logging.FileHandler(logPath)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter
        file_handler.setFormatter(self.formatter)

        # Add the handlers to the logger
        self.log.addHandler(file_handler)
