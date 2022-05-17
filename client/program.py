from client import Client


client = Client()

# start a parallel connection for recv
client.connect()

# start a parallel process for sending commands
client.send()