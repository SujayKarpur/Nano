# Nano
Nano is a persistent, secure, key-value store I built from scratch in python to understand how sockets, async i/o, and LSM Trees work 

## Usage

Clone the repository 
```sh
$ git clone https://github.com/SujayKarpur/plox.git
$ cd plox
```

Set up and activate a python virtual environment
```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Installs and Permissions...
```sh
$ pip install -r requirements.txt
$ sudo chmod +x nano
```

Start the server
```sh
$ python -m server 
```

Open a new tab and run the client
```sh
$ ./nano
```

## API
-fill

## I. Key Value Stores
key-value stores are the simplest kind of databases - they are just mappings from keys to values.

Nano implements a basic in-memory key-value store using python dictionaries that supports some simple operations:

![Alt text](assets/images/commands.png)


## II. Networking
![Alt text](assets/images/simple_socket_protocol.png)


## III. Handling Multiple Clients


## IV. Concurrent Client Handling


## V. Persistence

## VI. LSM Trees 

## VII. Security 

## VIII. Rewrite in Go

## IX. Distribute 

## X. Future Improvements
