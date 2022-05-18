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

from traceback import print_list
from sync import Sync


class Monitor():
    
    def __init__(self, socket, syncing_dir, client):
        self.socket = socket
        self.syncing_dir = syncing_dir
        self.client = client



    def run(self):

        sync = Sync(self.client)

        # get the commands first
        while True:
            command = self.socket.recv(1024)
            command = str(command.decode("utf-8"))
            print(command)
            command = command.split(' ')
            # print("path: ", str(command[2]))

            print(command)
            if (command[0] == 'putData'):
                sync.receiveDir()

            elif (command[0] == 'rmData'):
                sync.rmFile(command[1])
            
            elif (command[0] == 'moveData'):
                sync.moveFile(command[1],command[2])

