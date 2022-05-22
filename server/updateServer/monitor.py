
import os
from socket import socket
from time import sleep
from traceback import print_list
from config import Config


class Monitor():
    
    def __init__(self, sync, socket, logger):
        """
        :param sync: client syncing class for receiving data
        :param socket: client socket 
        """
        
        self.logger = logger
        self.socket = socket
        self.sync = sync



    def run(self):
        sync = self.sync
        while True:
            client_file = self.socket.makefile('rb')
            command = client_file.readline()
            command = str(command.decode("utf-8", errors='replace'))
            
            self.logger.debug("[+]command received: " + command)
            command = command.split(' ')
            # print("list command: ", command)
            
            config = Config()
            config.setClientWatch(self.socket.getpeername(), True)
            self.logger.debug("[+]paused observer for downloading")
            
            if (command[0] == 'putData'):
                sync.receiveDir(client_file)

            elif (command[0] == 'makeData'):
                if (os.path.exists(command[1])):
                    self.logger.debug("[-]file already exits")
                
                else:
                    sync.receiveDir(client_file)

            elif (command[0] == 'rmData'):
                sync.rmFile(command[1])
            
            elif (command[0] == 'moveData'):
                sync.moveFile(command[1],command[2])

            # sleep(1)
            config.setClientWatch(self.socket.getpeername(), False)
            self.logger.debug("[+]released observer ")

