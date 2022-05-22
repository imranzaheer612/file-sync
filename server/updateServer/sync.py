import os
import shutil

CHUNK_SIZE = 1_000_000

class Sync():
    
    def __init__(self, client, logger):
        """
        :param client: client class object
        :param  logger: logger object for logging to a file
        """
        self.logger = logger
        self.client = client
    
    def ready(self):
        """
        Receiving whole dir
        """
        sock = self.client.socket
        client_file = sock.makefile('rb')
        self.receiveDir(client_file)


    def receiveDir(self, client_file):
        """
        Receiving a dir
        :param client_file: socket client file
        """
        
        os.makedirs('data',exist_ok=True)
        
        while True:
            raw = client_file.readline()
            if not raw: break

            # First read filepath.
            filename = raw.strip().decode("utf-8", errors='replace')
            # print("received filename: ", filename)
            
            if filename == "done-transfer":
                break
            
            # Now read file size.
            length = client_file.readline()
            # print("received file_length: ", length)

            length = int(length)
            self.logger.debug(f'Downloading {filename}...\n  Expecting {length:,} bytes...')

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
                    self.logger.debug('Complete')
                    # self.garbage(client_file, length)
                    continue
            
            
            # socket was closed early.
            self.logger.debug('Incomplete')
            break
    

        return


    def rmFile(self, path):
        """
        remove a file
        :param path: file path
        """
        path = path.replace('\\', '/')
        path = path.strip('\n')
        path = os.path.relpath(path, 'data')
        path = os.path.join(self.client.dir_path, path)

        if (os.path.isfile(path)):
            os.remove(path)
        else :
            try:
                shutil.rmtree(path)
            except Exception as e:
                self.logger.error("[-]handled delete: ", e)


    def moveFile(self, src, dest):
        src = src.replace('\\', '/')
        src = src.strip('\n')
        dest = dest.strip('\n')
        src = os.path.relpath(src, 'data')
        dest = os.path.relpath(dest, 'data')
        src = os.path.join(self.client.dir_path, src)
        dest = os.path.join(self.client.dir_path, dest)
        
        if (os.path.isfile(src)):
            try: 
                # print("file -- make dir for ", dest)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.move(src, dest)
            except Exception as e:
                self.logger.error("[-]handled move: " , e)
        
        else :
            try:
                # print("dir -- make dir for ", dest)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                os.removedirs(src)
            except Exception as e:
                self.logger.error("[-]handled move : ", e)
