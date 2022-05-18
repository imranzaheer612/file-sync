import os
from sync import Sync
import socket
import threading

from monitor import Monitor

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
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    

    def run(self):
        # while self.signal:
        try:
            print("[+]waiting for  new data")
            data = self.socket.recv(32)
        except:
            print("Client " + str(self.address) + " has disconnected")
            self.signal = False
            connections.remove(self)
            # break
        if data != "":
            command = str(data.decode("utf-8"))
            print(command)
            if command == "sync new" :
                # msg = "we gonna sync your folder"
                # self.socket.send(str.encode(msg))
                sync = Sync(self)
                sync.ready()
                print("[+]sync done")
                # SyncAdd(self)

                ##
                # register for syncing & monitoring changed
                # --> then start monitoring
                # #
                mon = Monitor(self.socket, self.syncing_dir, self)
                mon.run()


            else: 
                self.socket.send(str.encode("unknown command!"))
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
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def main():
    #Get host and port
    host = 'localhost'
    port = int('55000')

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print('Listening for clients...')

    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,))
    newConnectionsThread.start()
    
main()