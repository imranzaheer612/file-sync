import socket
import threading
import sys
from time import sleep
from sync import Sync


#
# Parallely receiveing server commands
# #
def receive(socket, signal):
    while signal:
        # try:
            data = socket.recv(32)
            data_str = str(data.decode("utf-8"))
            print(data_str)

            if (data_str == 'server ready'):
                sync = Sync(socket)
                sync.start();
                print("sync done")

        # except Exception as e:
        #     print("You have been disconnected from the server: ", e)
        #     signal = False
        #     break

#Get host and port
host = "localhost"
port = int("55000")

#Attempt connection to server
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except Exception as e:
    print("Could not make a connection to the server", e)
    input("Press enter to quit")
    sys.exit(0)

#Create new thread to wait for data
receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

#
# Parallely sending commands to server#
while True:
    message = input("Enter command:")
    sock.send(str.encode(message))
