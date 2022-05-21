
import os

CHUNK_SIZE = 1_000_000


class SyncClient():
    
    def __init__(self, socket):
        self.socket = socket

    def sendDir(self, syncing_dir):
        sock = self.socket

        for path,dirs,files in os.walk(syncing_dir):
            for file in files:
                filename = os.path.join(path,file)
                self.sendFile(filename, syncing_dir)
        
        sock.send(str.encode('done-transfer') + b'\n')
        print('Done.')
        return
    
    def sendFile(self, filename, dir):
        print("filename--> ", filename)
        relpath = os.path.relpath(filename, dir)
        filesize = os.stat(filename)

        print(f'Sending {relpath}')

        with open(filename,'rb') as f:
            print()
            self.socket.sendall(relpath.encode() + b'\n')
            self.socket.sendall(str(filesize.st_size).encode() + b'\n')

            # Send the file in chunks so large files can be handled.
            while True:
                data = f.read(CHUNK_SIZE)
                if not data: break
                self.socket.sendall(data)


    def syncFile(self, file_name, dir):
        self.sendFile(file_name, dir)
        self.socket.sendall(str.encode('done-transfer') + b'\n')
        print('Done.')
        return