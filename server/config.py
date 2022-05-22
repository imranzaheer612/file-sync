import json

from cv2 import add

class Config():
    """
    Help parsing config.json and retrieve clients data
    """

    def __init__(self):
        """
        init file path
        """
        self.file_path = "config.json"


    def writeClient(self):
        """
        write sample client data struct
        """
        client = {
            "clients" : [
            ]
        }

        json_object = json.dumps(client, indent = 4)
        with open(self.file_path , "w") as outfile:
            outfile.write(json_object)


    def getClientWatch(self , address):
        """
        Look value for client watch key
        :param address: client address to search
        """

        data = None
        add, port = address
        with open(self.file_path, 'r') as openFile:
            data = json.load(openFile)
        
        result = [x for x in data['clients'] if x["id"]==add]
        # print("result: ", result)
        # print("searched: ", address)
        watcher = result[0]['watcher']
        # print("checked --->", watcher)

        return watcher


    def setClientWatch(self, address, watchValue):
        """
        Set watch key-value for a client
        :param address: client address
        :param watchValue: value to be passed
        """
        
        data = None
        add, port = address

        with open(self.file_path, 'r') as openFile:
            data = json.load(openFile)
        
        for client in data['clients']:
            if client['id'] == add:
                client['watcher'] = watchValue

        json_object = json.dumps(data, indent = 4)

        with open(self.file_path , "w") as outfile:
            outfile.write(json_object)

        # print("value set: : "  ,watchValue)

    def clientExits(self, address):
        """
        Check if a client exits
        :param address: client's address
        """
        
        add, port = address
        # print("search--> ", add)
        data = None
        with open(self.file_path, 'r') as openFile:
            data = json.load(openFile)
            # print(data)
        
        result = [x for x in data['clients'] if x["id"]==add]
        
        if (result):
            return True
        else:
            return False

    def registerClient(self, address):
        """
        Register a new client to the server
        :param address: client address to register
        """

        add, port = address
        with open(self.file_path, 'r+') as f:
            data = json.load(f)

        # print("apending", address)
        data["clients"].append(
                {
                    "id" : add,
                    "watcher" : False
                }
            )

        json_object = json.dumps(data, indent = 4)
        with open(self.file_path , "w") as outfile:
            outfile.write(json_object)