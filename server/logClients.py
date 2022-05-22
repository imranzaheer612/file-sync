
import logging


class LogClients():

    def __init__(self) -> None:
        pass


    def getLogger(self, name):

        logger_name = 'logger_' + str(name)
        logger = logging.getLogger(logger_name)
        formatter = logging.Formatter('[%(asctime)s] : %(message)s')

        # output log file per thread
        outputFile = "log/client_" + str(name) + ".txt"
        fileHandler = logging.FileHandler(outputFile, mode='w')
        fileHandler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)

        return logger