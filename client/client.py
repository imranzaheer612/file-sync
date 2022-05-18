import os
import socket
import threading
import sys
from monitor import Watcher
from sync import Sync



class Client(): 

    ##
    # REGISTERED --> can be in a json file
    # 
    # --> every time client reopen check if it is a registered client
    # --> if registered then skip the upload dir step and start monitoring
    # host and port can also be
    # #

    def __init__(self, host="localhost", port=int("55000")):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.REGISTERED = False
        self.syncing_dir = os.path.join("data", "myData")
        self.signal = True

    #
    # Parallely receiveing server commands
    # #
    def receive(self):
        while self.signal:
            # try:
                data = self.socket.recv(32)
                data_str = str(data.decode("utf-8"))
                print(data_str)

                if (data_str == 'server ready'):
                    
                    # upload dir for the first time
                    sync = Sync(self.socket)
                    sync.sendDir(self.syncing_dir);
                    print("sync done")
                    
                    # then sync changes
                    self.REGISTERED = True
                    w = Watcher(self.socket, self.syncing_dir)
                    w.run()

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
