
import logging


class LogClient():

    def __init__(self) -> None:
        pass


    def getLogger(self):

        logger_name = 'logger'
        logger = logging.getLogger(logger_name)
        formatter = logging.Formatter('[%(asctime)s] : %(message)s')

        # output log file per thread
        outputFile = "data\log\log.txt"
        fileHandler = logging.FileHandler(outputFile, mode='w')
        fileHandler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)

        return logger