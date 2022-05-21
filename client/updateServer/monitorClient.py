import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# from sync import Sync
from updateServer.syncServer import Sync

CLIENT_SOCKET = None
DIRECTORY_TO_WATCH = None
READY = "READY-TO-SYNC"
READY_ACK = "READY-TO-OBSERVE"
PAUSED = False

class Watcher():
    
    # DIRECTORY_TO_WATCH = os.path.join("data", "mydata")

    def __init__(self, socket, dir):
        global CLIENT_SOCKET, DIRECTORY_TO_WATCH
        
        self.observer = Observer()
        DIRECTORY_TO_WATCH = dir
        CLIENT_SOCKET = socket



    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()



class Handler(FileSystemEventHandler):

    global PAUSED

    @staticmethod
    def on_created(event):
        if (not PAUSED):
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path)
            data_path = event.src_path
            
            # tell server to put this file
            CLIENT_SOCKET.send(str.encode('makeData ' + data_path) + b'\n')
            sync = Sync(CLIENT_SOCKET)
                
            if (os.path.isfile(data_path)):    
                # send the file
                sync.syncFile(data_path)

            else: 
                # send the dir
                sync.sendDir(data_path)
        else:
            print("event is paused ---")
            return

    @staticmethod
    def on_modified(event):
        if (not PAUSED):
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)

            file_path = event.src_path

            if (os.path.isfile(file_path)): 
                # tell server to put this file
                CLIENT_SOCKET.send(str.encode('putData ' + file_path) + b'\n')
                
                # send the file
                sync = Sync(CLIENT_SOCKET)
                sync.syncFile(file_path)
        else:
            print("event is paused ---")
            return

    @staticmethod
    def on_deleted(event):
        if (not PAUSED):
            print ("Received deleted event - %s." % event.src_path)
            data_path = event.src_path
            
            # tell server to delete this file
            CLIENT_SOCKET.send(str.encode('rmData ' + data_path) + b'\n')

        else:
            print("event is paused ---")
            return
    
    @staticmethod
    def on_moved(event):
        if (not PAUSED):
            print ("Received moved event - from %s." % event.src_path, "to ", event.dest_path)
            src = event.src_path
            dest = event.dest_path
            
            # tell server to delete this file
            CLIENT_SOCKET.send(str.encode('moveData ' + src + ' ' + dest) + b'\n')

        else:
            print("event is paused ---")
            return


        ##
        # sync will notify server
        # new dir--> sync.putdir(path)#
        # deleted dir--> sync.removedir(path)
        # 
        # new file --> sync.put(path)
        # deleted file --> sync.remove(path)#

# if __name__ == '__main__':
#     w = Watcher()
#     w.run()