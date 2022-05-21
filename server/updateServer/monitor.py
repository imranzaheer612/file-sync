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

import os
from socket import socket
from time import sleep
from traceback import print_list
from config import Config
# from updateClient.monitorServer import PAUSED
# from updateServer.sync import Sync


class Monitor():
    
    def __init__(self, sync, socket):
        self.socket = socket
        # self.syncing_dir = syncing_dir
        self.sync = sync
        # self.observer = watcher.observer



    def run(self):
        # global PAUSED

        sync = self.sync
        # socket.makefile('rb').
        # get the commands first
        while True:
            client_file = self.socket.makefile('rb')
            # client_file.flush()
            # command = self.socket.recv(1024)
            command = client_file.readline()
            
            command = str(command.decode("utf-8", errors='replace'))
            print("init command received: ", command)
            command = command.split(' ')
            # print("path: ", str(command[2]))

            print("list command: ", command)
            
            config = Config()
            config.setClientWatch(self.socket.getpeername(), True)
            print("paused observer change downloading")
            
            if (command[0] == 'putData'):
                sync.receiveDir(client_file)

            elif (command[0] == 'makeData'):
                if (os.path.exists(command[1])):
                    print("file already exits")
                
                else:
                    sync.receiveDir(client_file)

            elif (command[0] == 'rmData'):
                sync.rmFile(command[1])
            
            elif (command[0] == 'moveData'):
                sync.moveFile(command[1],command[2])

            # sleep(1)
            config.setClientWatch(self.socket.getpeername(), False)
            print("release pause after downloading ")

