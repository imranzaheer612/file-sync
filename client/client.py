import os
import socket
import threading
import sys
from updateClient.syncClient import SyncClient
from updateServer.monitorClient import Watcher
from updateClient.monitorServer import MonitorServer
from updateServer.syncServer import Sync



class Client(): 

    ##
    # REGISTERED --> can be in a json file
    # 
    # --> every time client reopen check if it is a registered client
    # --> if registered then skip the upload dir step and start monitoring
    # host and port can also be
    # #

    def __init__(self, host="10.7.41.237", port=int("55000")):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.recv(32).dec
        self.host = host
        self.port = port
        self.REGISTERED = False
        self.syncing_dir = os.path.join("data", "myData")
        self.signal = True

    #
    # Parallely receiving server commands
    # #
    def receive(self):
        # while self.signal:
            # try:
                data = self.socket.recv(32)
                # client_file = self.socket.makefile('rb')
                data_str = str(data.decode("utf-8"))
                # data_str = client_file.readline()
                # print(data_str)

                if (data_str == 'true'):
                    # upload dir for the first time
                    sync = Sync(self.socket)
                    sync.sendDir(self.syncing_dir);
                    print("sync done")

                else:
                    sync = SyncClient(self)
                    sync.receiveDir()
                # then sync changes
                self.REGISTERED = True

                sync  = MonitorServer(self.socket, self.syncing_dir, self)
                # sync.run()
                
                receiveThread = threading.Thread(target = sync.run)
                receiveThread.start()

                w = Watcher(self.socket, self.syncing_dir)
                w.run()

                    # run monitor server

            # except Exception as e:
            #     print("You have been disconnected from the server: ", e)
            #     signal = False
            #     break


    #
    # Connection to server
    # #
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print("Could not make a connection to the server", e)
            input("Press enter to quit")
            sys.exit(0)

        receiveThread = threading.Thread(target = self.receive)
        receiveThread.start()

    #
    # Parallely sending commands to server
    # #
    def send(self):
        while True:
            message = input("Enter command:")
            self.socket.send(str.encode(message))

    def scanStruct(self):
        log = ''
        path = os.path.join('data')
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            log += indent + os.path.basename(root) + '/' + '\n'
            # print(log)
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                log += subindent + os.path.basename(f) + '/' + '\n'

        return log