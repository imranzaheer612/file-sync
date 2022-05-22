import os
import socket
import threading
import sys
from logClient import LogClient
from updateClient.syncClient import SyncClient
from updateServer.monitorClient import Watcher
from updateClient.monitorServer import MonitorServer
from updateServer.syncServer import Sync



class Client():
    """
    Client will handle function like connecting to the server
    & monitoring file changes in parallel
    """

    

    def __init__(self, host="10.7.41.237", port=int("55000")):
        """
        Initializing socket
        :param self:
        :param host: host address (serve address)
        :param port: host port number
        :return:
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.syncing_dir = os.path.join("data", "myData")
        self.signal = True

   
    def startClient(self):
        """
        Start client and look for server commands
        if ("true") --> client already synced --> get files
        else --> client gonna sync for the firs time --> send files

        :param self:
        """

        client_log = LogClient()
        logger = client_log.getLogger()
        log = ""

        try: 
            data = self.socket.recv(32)
            data_str = str(data.decode("utf-8"))
            
            if (data_str == 'true'):
                sync = Sync(self.socket, logger)
                sync.sendDir(self.syncing_dir);
                logger.debug("sync done")

            else:
                sync = SyncClient(self, logger)
                sync.receiveDir()


            sync  = MonitorServer(self.socket, self.syncing_dir, self, logger)        
            receiveThread = threading.Thread(target = sync.run)
            receiveThread.start()

            w = Watcher(self.socket, self.syncing_dir, logger)
            w.run()

        except Exception as e:
            print("You have been disconnected from the server: ", e)
            logger.warn("You have been disconnected from the server: " + e)

    def connect(self):
        """
        Try connecting to the serve and start client thread
        """
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print("Could not make a connection to the server", e)
            input("Press enter to quit")
            sys.exit(0)

        receiveThread = threading.Thread(target = self.startClient)
        receiveThread.start()

    
    def send(self):
        """
        Used if you wanna start client receiving commands thread 
        """
        while True:
            message = input("Enter command:")
            self.socket.send(str.encode(message))


    def scanStruct(self):
        """
        Scan the dir structure. You can use it compare tree with serve
        """
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