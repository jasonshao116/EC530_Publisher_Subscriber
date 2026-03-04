# EC530_Publisher_Subscriber
This Repo contains activities of Publisher-Subscriber systems from EC530 


## Step 1 

### server.py (Transmitter) 
- Listens to clients 
- For each client, a background thread receives messages 
- Main thread reads your terminal input and broadcasts to all clients 

### client.py (Receiver)
- Background thread receives messages from the server
- The main thread lets you type messages to the server

### To Run: 
```bash
# On terminal 1
python3 server.py
# On terminal 2 (change port # if needed)
python3 client.py 127.0.0.1 5011
# On terminal 3
python3 client.py 127.0.0.1 5011
```


## Step 2

