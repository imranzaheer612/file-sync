import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from updateServer.syncServer import Sync

CLIENT_SOCKET = None
DIRECTORY_TO_WATCH = None
LOGGER = None

class Watcher():
    """
    Class help scanning any changes in the given dir
    """
    
    def __init__(self, socket, dir, logger):
        """
        Init dirs
        :param self:
        :param socket: Pass socket
        :param dir: Pass dir you wanna sync
        :param logger: logger
        :return:
        """
        
        global CLIENT_SOCKET, DIRECTORY_TO_WATCH, LOGGER

        self.observer = Observer()
        LOGGER = logger
        DIRECTORY_TO_WATCH = dir
        CLIENT_SOCKET = socket



    def run(self):
        """
        Start file observer thread
        :param self:
        :return:
        """
        
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            LOGGER.error("Error")

        self.observer.join()



class Handler(FileSystemEventHandler):
    """
    Handler class for observer() events
    Detect file changes and send commands to the server
    """

    @staticmethod
    def on_created(event):
        LOGGER.debug("Received created event - " + event.src_path)
        data_path = event.src_path
        
        CLIENT_SOCKET.send(str.encode('makeData ' + data_path) + b'\n')
        sync = Sync(CLIENT_SOCKET, LOGGER)
            
        if (os.path.isfile(data_path)):    
            sync.syncFile(data_path)

        else: 
            sync.sendDir(data_path)


    @staticmethod
    def on_modified(event):
        LOGGER.debug("Received modified event - "  + event.src_path)
        file_path = event.src_path

        if (os.path.isfile(file_path)): 
            CLIENT_SOCKET.send(str.encode('putData ' + file_path) + b'\n')
            sync = Sync(CLIENT_SOCKET, LOGGER)
            sync.syncFile(file_path)


    @staticmethod
    def on_deleted(event):
        LOGGER.debug("Received deleted event - " + event.src_path)
        data_path = event.src_path
        
        # tell server to delete this file
        CLIENT_SOCKET.send(str.encode('rmData ' + data_path) + b'\n')


    
    @staticmethod
    def on_moved(event):
        LOGGER.debug("Received moved event - from " % event.src_path + "to " +event.dest_path)
        src = event.src_path
        dest = event.dest_path
        
        # tell server to delete this file
        CLIENT_SOCKET.send(str.encode('moveData ' + src + ' ' + dest) + b'\n')
