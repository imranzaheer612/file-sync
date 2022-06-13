# File Synchronizer

Implemented a file synchronizer in python.

![working system](https://media0.giphy.com/media/i8ut1ISFHHkZpqeAdk/giphy.gif?cid=790b761108620415beff7b682fc59978f17cc306ddd295cb&rid=giphy.gif&ct=g)

## Description

On Client Side.
* Save your data in dir **./mydata**
* Start the server.
* The client will be synced with the server
* In case files are misplaced by the user
* Start the client-side again
* The files will be recovered

## Getting Started

### Dependencies

* Python
* watchdogs

```
pip install watchdog
```

### Installing

* Clone the repo
```
git clone https://github.com/imranzaheer612/file-sync.git
```
* Start the server first on the same network (LAN)
* In **program.py** give the host **IP** and **Port number** to the client
```
client = Client('localhost', 55000)
client.connect()
```  

### Executing program

* Start the server first on LAN
* Then start the client

## Help

You case some error occurred you can see the logged files on the client or server side.


## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details