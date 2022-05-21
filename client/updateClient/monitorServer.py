##
# wait wor changes from the client on the socket
# 
# client disconnected --- connected again --> registered ->>> monitor changes
# 
# 
# received command --> {mkdir "path"} --> mkdir at path 
# received command --> {rmdir "path"} --> remove dir at path
#  
# received command --> {mkFile "path"} --> make file at path 
# received command --> {rmFile "path"} --> remove file at path 
# #

# from traceback import print_list
# from syncServer import Sync


import os
from updateClient.syncClient import SyncClient
from updateServer.monitorClient import PAUSED


class MonitorServer():
    
    def __init__(self, socket, syncing_dir, client):
        self.socket = socket
        self.syncing_dir = syncing_dir
        self.client = client

        



    def run(self):
        global PAUSED

        sync = SyncClient(self.client)

        # get the commands first
        while True:
            client_file = self.socket.makefile('rb')
            # command = self.socket.recv(1024)
            command = client_file.readline()
            # command = self.socket.recv(1024)

            command = str(command.decode("utf-8", errors='replace'))
            # print(command)
            command = command.split(' ')
            # print("path: ", str(command[2]))

            # print("command recieing data ")
            PAUSED = True
            print("paused observer change downloading")

            if (command[0] == 'putData'):
                print("gonna make file", command)
                sync.receiveDir()

            elif (command[0] == 'makeData'):
                if (os.path.exists(command[1])):
                    print("file already exits")
                
                else:
                    sync.receiveDir()

            elif (command[0] == 'rmData'):
                sync.rmFile(command[1])
            
            elif (command[0] == 'moveData'):
                sync.moveFile(command[1],command[2])

            PAUSED = False
            print("release pause after downloading ")
