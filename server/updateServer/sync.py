import os
import shutil

CHUNK_SIZE = 1_000_000

class Sync():
    
    def __init__(self, client):
        self.client = client
        # self.scanStruct()
    
    def ready(self):
        # self.client.socket.send(str.encode("server ready"))
        sock = self.client.socket
        client_file = sock.makefile('rb')
        self.receiveDir(client_file)


    def receiveDir(self, client_file):
        # sock = self.client.socket;

        # Make a directory for the received files.
        os.makedirs('data',exist_ok=True)

        # client_file = sock.makefile('rb')
        while True:

            raw = client_file.readline()
            if not raw: break

            # First read filepath.
            filename = raw.strip().decode("utf-8", errors='replace')
            print("received filename: ", filename)
            
            if filename == "done-transfer":
                break
            
            # Now read file size.
            length = client_file.readline()
            print("received file_length: ", length)

            length = int(length)
            print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='')

            # Make dir according to filepaths.
            path = os.path.join(self.client.dir_path, filename)
            os.makedirs(os.path.dirname(path),exist_ok=True)

            # Now read the files in chunks.
            with open(path,'wb') as f:
                while length:
                    chunk = min(length, CHUNK_SIZE)
                    # chunk = CHUNK_SIZE
                    data = client_file.read(chunk)
                    if not len(data): break
                    f.write(data)
                    length -= len(data)
                else:
                    print('Complete')
                    # self.garbage(client_file, length)
                    continue
            
            
            # socket was closed early.
            print('Incomplete')
            break
    

        return



   

        print(log)

    def rmFile(self, path):
        path = path.replace('\\', '/')
        path = path.strip('\n')
        path = os.path.relpath(path, 'data')
        path = os.path.join(self.client.dir_path, path)
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
        dest = dest.strip('\n')
        src = os.path.relpath(src, 'data')
        dest = os.path.relpath(dest, 'data')
        src = os.path.join(self.client.dir_path, src)
        dest = os.path.join(self.client.dir_path, dest)
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
        

    # def sendDir(self, syncing_dir):
    #         sock = self.socket

    #         for path,dirs,files in os.walk(syncing_dir):
    #             for file in files:
    #                 filename = os.path.join(path,file)
    #                 self.sendFile(filename)
            
    #         sock.send(str.encode('done-transfer') + b'\n')
    #         print('Done.')
    #         return

    # def sendFile(self, filename):
    #     relpath = os.path.relpath(filename, self.client.dir_path)
    #     filesize = os.path.os.stat(filename)

    #     print(f'Sending {relpath}')

    #     with open(filename,'rb') as f:
    #         self.socket.send(relpath.encode() + b'\n')
    #         self.socket.send(str(filesize.st_size).encode() + b'\n')

    #         # Send the file in chunks so large files can be handled.
    #         while True:
    #             data = f.read(CHUNK_SIZE)
    #             if not data: break
    #             self.socket.sendall(data)