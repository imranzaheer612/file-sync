
import os

class UploadDir():
    
    def __init__(self, socket, syncing_dir):
        self.socket = socket
        self.syncing_dir = syncing_dir


    def start(self):
                
        CHUNKSIZE = 1_000_000

        sock = self.socket
        # sock.bind(('',5000))
        # sock.listen(1)

        # while True:
            # print('Waiting for a client...')
            # client,address = sock.accept()
            # print(f'Client joined from {address}')
            # with client:
        for path,dirs,files in os.walk(self.syncing_dir):
            for file in files:
                filename = os.path.join(path,file)
                relpath = os.path.relpath(filename,'./data')
                filesize = os.path.getsize(filename)

                print(f'Sending {relpath}')

                with open(filename,'rb') as f:
                    sock.send(relpath.encode() + b'\n')
                    sock.send(str(filesize).encode() + b'\n')

                    # Send the file in chunks so large files can be handled.
                    while True:
                        data = f.read(CHUNKSIZE)
                        if not data: break
                        sock.sendall(data)
        
        sock.send(str.encode('done-transfer') + b'\n')
        print('Done.')
        return