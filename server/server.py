import os
import socket
import threading
from time import sleep
from config import Config
from updateClient.syncClient import SyncClient

from updateServer.sync import Sync
from updateServer.monitor import Monitor
from updateClient.monitorServer import Watcher

#Variables for holding information about connections
connections = []
total_connections = 0


##
# save registered clients in a json
# 
# -> if connected client is registered then skip download and start monitoring
# #

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.syncing_dir = os.path.join("data")
        host, port = socket.getpeername()
        self.dir_path = os.path.join('data', str(host))
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    

    def run(self):
        # while self.signal:
        # try:
        #     print("[+]waiting for  new data")
        #     data = self.socket.recv(32)
        # except:
        #     print("Client " + str(self.address) + " has disconnected")
        #     self.signal = False
        #     connections.remove(self)
            # break

        config = Config()
        client_name = self.socket.getpeername()
        client_exits = config.clientExits(client_name)
        if (not client_exits):
            print("client not exits")
            config.registerClient(client_name)
            self.socket.send(str.encode("true"))
            sync = Sync(self)
            sync.ready()
            print("[+]sync done")
        
        else:
            self.socket.send(str.encode("false"))
            print("client exits")
            sync = SyncClient(self.socket)
            sleep(1)
            sync.sendDir(self.dir_path)
        

        # if data != "":
            # command = str(data.decode("utf-8"))
            # print(command)
            # if command == "sync new" :
                # msg = "we gonna sync your folder"
                # self.socket.send(str.encode(msg))
                
                
            
            # SyncAdd(self)

        # watcher  = Watcher(self.socket, self.syncing_dir)
        # sync.run()

        # receiveThread = threading.Thread(target = watcher.run)
        # receiveThread.start()

        ##
        # register for syncing & monitoring changed
        # --> then start monitoring
        # #
        sync2 = Sync(self)
        mon = Monitor(sync2, self.socket)
        mon.run()


            # else: 
            #     self.socket.send(str.encode("unknown command!"))
            # print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
            # for sending data to all clients
            # for client in connections:
            #     if client.id != self.id:
            #         client.socket.sendall(data)

#
# Waiting for new connections
# and serving old connection
# #
def newConnections(socket):
    while True:
        sock, address = socket.accept()


        #add to client configs
        # config = Config()
        # config.writeClient(str(address))
        # config.getClientWatch(str(address))


        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def scanStruct(dir_path):
        log = ''
        path = os.path.join('data', dir_path)
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * (level)
            log += indent + os.path.basename(root) + '/' + '\n'
            # print(log)
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                log += subindent + os.path.basename(f) + '/' + '\n'

        return log

def main():
    #Get host and port
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



