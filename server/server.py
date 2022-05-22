import os
import socket
import threading
from time import sleep
from config import Config
from logClients import LogClients
from updateClient.syncClient import SyncClient

from updateServer.sync import Sync
from updateServer.monitor import Monitor

#Variables for holding information about connections
connections = []
total_connections = 0



class Client(threading.Thread):
    """
    Class for handling client connected with the server
    """
    
    def __init__(self, socket, id, name, signal):
        """
        :param self:
        :param socket: connect socket with the respective client
        :param id: connection id
        :param name: name to the client
        :param signal: help client start & stop
        :return:
        """
        
        threading.Thread.__init__(self)
        self.socket = socket
        
        add, port = socket.getsockname()
        self.address = add
        
        self.client_add, port = socket.getpeername()
        self.dir_path = os.path.join('data', str(self.client_add))
        
        self.id = id
        self.name = name
        self.signal = signal
        self.syncing_dir = os.path.join("data")
        
        
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    

    def run(self):
        try:
            client_log = LogClients()
            logger = client_log.getLogger(self.client_add)
            log = ""

            config = Config()
            client_name = self.socket.getpeername()
            client_exits = config.clientExits(client_name)
            
            if (not client_exits):
                logger.warning("[-]client not exits")
                config.registerClient(client_name)
                self.socket.send(str.encode("true"))
                sync = Sync(self, logger)
                sync.ready()
                logger.debug("[+]sync done")
            
            else:
                self.socket.send(str.encode("false"))
                logger.debug("[+]client exits")
                sync = SyncClient(self.socket, logger)
                sleep(1)
                sync.sendDir(self.dir_path)    

            # watcher  = Watcher(self.socket, self.syncing_dir)
            # sync.run()

            # receiveThread = threading.Thread(target = watcher.run)
            # receiveThread.start()

            sync2 = Sync(self, logger)
            mon = Monitor(sync2, self.socket, logger)
            mon.run()

        except Exception as e:
            msg = "Client " + str(self.address) + " has disconnected: " + str(e)
            logger.error(msg)
            self.signal = False
            connections.remove(self)


# class def ended
########################################################################################

def newConnections(socket):
    """
    Accept connections and add to thread
    :param socket: connection socket
    """
    while True:
        sock, address = socket.accept()

        global total_connections
        connections.append(Client(sock, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def scanStruct(dir_path):
    """
    :param dir_path: dir you wanna scan its tree
    """
    log = ''
    path = os.path.join('data', dir_path)
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        log += indent + os.path.basename(root) + '/' + '\n'
        # print(log)
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            log += sub_indent + os.path.basename(f) + '/' + '\n'

    return log


def main():
    host = ''
    port = int('55000')

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()
    print('Listening for clients...')

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()



