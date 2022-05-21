import json

from cv2 import add

class Config():


    def __init__(self):
        self.file_path = "config.json"

    def writeClient(self, address):
        add, port = address
        # Data to be written
        client = {
            "clients" : [
                {
                    "id" : add,
                    "watcher" : False
                }
            ]
        }

        json_object = json.dumps(client, indent = 4)

        with open(self.file_path , "w") as outfile:
            outfile.write(json_object)

    def getClientWatch(self , address):
        # Opening JSON file
        data = None
        add, port = address
        with open(self.file_path, 'r') as openFile:
        
            # Reading from json file
            data = json.load(openFile)
            # print(data)
        
        result = [x for x in data['clients'] if x["id"]==add]
        # print("result: ", result)
        # print("searched: ", address)
        watcher = result[0]['watcher']
        print("checked --->", watcher)

        return watcher

    def setClientWatch(self, address, watchValue):
        data = None
        add, port = address
        with open(self.file_path, 'r') as openFile:
        
            # Reading from json file
            data = json.load(openFile)
            # print(data)
        
        for client in data['clients']:
            if client['id'] == add:
                client['watcher'] = watchValue

        
        json_object = json.dumps(data, indent = 4)

        with open(self.file_path , "w") as outfile:
            outfile.write(json_object)

        print("value seted: : "  ,watchValue)

    def clientExits(self, address):
        add, port = address
        # Opening JSON file
        print("search--> ", add)
        data = None
        with open(self.file_path, 'r') as openFile:
        
            # Reading from json file
            data = json.load(openFile)
            # print(data)
        
        result = [x for x in data['clients'] if x["id"]==add]
        
        if (result):
            return True
        else:
            return False

    def registerClient(self, address):

        add, port = address
        with open(self.file_path, 'r+') as f:
            data = json.load(f)

        print("apending", address)
        # for name in firstNameList:
        data["clients"].append(
                {
                    "id" : add,
                    "watcher" : False
                }
            )

        json_object = json.dumps(data, indent = 4)

        with open(self.file_path , "w") as outfile:
            outfile.write(json_object)