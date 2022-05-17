import os


class DownloadDir():
    
    def __init__(self, client):
        self.client = client
    
    def ready(self):
        self.client.socket.send(str.encode("server ready"))
        self.receive()


    def receive(self):
        CHUNKSIZE = 1_000_000
        sock = self.client.socket;

        # Make a directory for the received files.
        os.makedirs('data',exist_ok=True)

        clientfile = sock.makefile('rb')
        while True:

            raw = clientfile.readline()
            if not raw: break

            # First read filepath.
            filename = raw.strip().decode()
            if filename == "done-transfer":
                break
            
            # Now read file size.
            length = int(clientfile.readline())
            print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='',flush=True)

            # Make dir according to filepaths.
            path = os.path.join('./data', filename)
            os.makedirs(os.path.dirname(path),exist_ok=True)

            # Now read the files in chunks.
            with open(path,'wb') as f:
                while length:
                    chunk = min(length,CHUNKSIZE)
                    data = clientfile.read(chunk)
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