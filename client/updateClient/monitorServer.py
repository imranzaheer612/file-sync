

import os
from updateClient.syncClient import SyncClient


class MonitorServer():
    
    def __init__(self, socket, syncing_dir, client, logger):
        self.socket = socket
        self.syncing_dir = syncing_dir
        self.client = client
        self.logger = logger



    def run(self):
        global PAUSED

        sync = SyncClient(self.client, self.logger)

        while True:
            try: 
                client_file = self.socket.makefile('rb')
                command = client_file.readline()

                command = str(command.decode("utf-8", errors='replace'))
                # print(command)
                command = command.split(' ')
                # print("path: ", str(command[2]))

                # print("command recieing data ")
                PAUSED = True
                self.logger.debug("[+]paused observer while downloading")

                if (command[0] == 'putData'):
                    # print("gonna make file", command)
                    sync.receiveDir()

                elif (command[0] == 'makeData'):
                    if (os.path.exists(command[1])):
                        self.logger.warn("[-]file already exits")
                    
                    else:
                        sync.receiveDir()

                elif (command[0] == 'rmData'):
                    sync.rmFile(command[1])
                
                elif (command[0] == 'moveData'):
                    sync.moveFile(command[1],command[2])

                PAUSED = False
                self.logger.debug("[+]released pause after downloading ")
            except Exception as e:
                self.logger.error("error: ", e)