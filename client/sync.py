
import os

CHUNK_SIZE = 1_000_000


class Sync():
    
    def __init__(self, socket):
        self.socket = socket

    def sendDir(self, syncing_dir):
        sock = self.socket

        for path,dirs,files in os.walk(syncing_dir):
            for file in files:
                filename = os.path.join(path,file)
                self.sendFile(filename)
        
        sock.send(str.encode('done-transfer') + b'\n')
        print('Done.')
        return
    
    def sendFile(self, filename):
        relpath = os.path.relpath(filename,'./data')
        filesize = os.path.getsize(filename)

        print(f'Sending {relpath}')

        with open(filename,'rb') as f:
            self.socket.send(relpath.encode() + b'\n')
            self.socket.send(str(filesize).encode() + b'\n')

            # Send the file in chunks so large files can be handled.
            while True:
                data = f.read(CHUNK_SIZE)
                if not data: break
                self.socket.sendall(data)


    def syncFile(self, file_name):
        self.sendFile(file_name)
        self.socket.send(str.encode('done-transfer') + b'\n')
        print('Done.')
        return