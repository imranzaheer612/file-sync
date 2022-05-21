import os
import shutil

CHUNK_SIZE = 1_000_000

class SyncClient():
    
    def __init__(self, client):
        self.client = client
    
    def ready(self):
        self.client.socket.send(str.encode("client ready"))
        self.receiveDir()


    def receiveDir(self):
        sock = self.client.socket;

        # Make a directory for the received files.
        os.makedirs('data',exist_ok=True)


        client_file = sock.makefile('rb')
        # print("gonna start ")
        while True:
            
            # print("gonna read file")
            raw = client_file.readline()
            if not raw: break

            # First read filepath.
            filename = raw.strip().decode("utf-8", errors='replace')
            if filename == "done-transfer":
                break

            print("filename: ", filename)
            
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
        # self.moveFile(path, os.path.join("data","tempDel"))
        # def rmFile(self, path):
        path = path.replace('\\', '/')
        path = path.strip('\n')
        # self.moveFile(path, os.path.join("data","tempDel"))
        if (os.path.isfile(path)):
            os.remove(path)
        else :
            try:
                shutil.rmtree(path)
            except Exception as e:
                print("handel delete: ", e)



    def moveFile(self, src, dest):
        # print("given : ", src)
        src = src.replace('\\', '/')
        src = src.strip('\n')
        # print("setted: ", src)
        
        if (os.path.isfile(src)):
            try: 
                print("file -- make dir for ", dest)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.move(src, dest)
            except Exception as e:
                print("handled move rename: " , e)
        
        else :
             # pass
            try:
                print("dir -- make dir for ", dest)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.removedirs(src)
            except Exception as e:
                print("handled move rename: ", e)
