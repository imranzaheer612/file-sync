import os
import shutil

CHUNK_SIZE = 1_000_000

class Sync():
    
    def __init__(self, client):
        self.client = client
    
    def ready(self):
        self.client.socket.send(str.encode("server ready"))
        self.receiveDir()


    def receiveDir(self):
        sock = self.client.socket;

        # Make a directory for the received files.
        os.makedirs('data',exist_ok=True)

        client_file = sock.makefile('rb')
        while True:

            raw = client_file.readline()
            if not raw: break

            # First read filepath.
            filename = raw.strip().decode()
            if filename == "done-transfer":
                break
            
            # Now read file size.
            length = int(client_file.readline())
            print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='',flush=True)

            # Make dir according to filepaths.
            path = os.path.join('./data', filename)
            os.makedirs(os.path.dirname(path),exist_ok=True)

            # Now read the files in chunks.
            with open(path,'wb') as f:
                while length:
                    chunk = min(length, CHUNK_SIZE)
                    data = client_file.read(chunk)
                    if not data: break
                    f.write(data)
                    length -= len(data)
                else:
                    print('Complete')
                    continue

            # socket was closed early.
            print('Incomplete')
            break

        return


    def rmFile(self, path):
        if (os.path.isfile(path)):
            os.remove(path)
        else :
            shutil.rmtree(path)


    def moveFile(self, src, dest):

        # print("sssss for ", dest)
        if (os.path.isfile(src)):
            print("file -- make dir for ", dest)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(src, dest)
        
        else :
            # pass
            print("dir -- make dir for ", dest)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            os.removedirs(src)
        
