
from dataclasses import replace
import os

CHUNK_SIZE = 1_000_000


class Sync():
    """
    Class use the keep server synced by sending files
    """
    
    def __init__(self, socket, logger):
        """
        Init socket
        :param socket: socket
        """
        
        self.socket = socket
        self.logger = logger


    def sendDir(self, syncing_dir):
        """
        Send dir to server scan files and send one by one
        :param syncing_dir: Dir you wanna send
        """

        sock = self.socket
        for path,dirs,files in os.walk(syncing_dir):
            for file in files:
                filename = os.path.join(path,file)
                self.sendFile(filename)
        
        sock.send(str.encode('done-transfer') + b'\n')
        # print('Done.')
        return
    

    def sendFile(self, filename):
        """
        Sending file to server
        :send file_name first
        :then file_size
        :then file_data

        :param filename: file_path you wanna send
        """
        
        relpath = os.path.relpath(filename,'./data')
        filesize = os.path.os.stat(filename)

        self.logger.debug('Sending {' + relpath + '}')

        with open(filename,'rb') as f:
            self.socket.send(relpath.encode() + b'\n')
            self.socket.send(str(filesize.st_size).encode() + b'\n')

            # Send the file in chunks so large files can be handled.
            while True:
                data = f.read(CHUNK_SIZE)
                if not data: break
                self.socket.sendall(data)


    def syncFile(self, file_name):
        self.sendFile(file_name)
        self.socket.send(str.encode('done-transfer') + b'\n')
        self.logger.debug('Done.')
        return