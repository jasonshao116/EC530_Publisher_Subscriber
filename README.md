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

### broker.py
Broker/Router (server): accepts connections, forwards events to everyone (or to a topic later)

### node.py
Node (client): has a receiver thread + a sender loop and speaks in event messages (JSON)

### To Run: 
```bash
# On terminal 1
python3 broker.py
# On terminal 2 (change port # if needed)
python3 node.py OrderService 127.0.0.1 5011
# On terminal 3
python3 node.py PaymentService 127.0.0.1 5011
# On terminal 4
python3 node.py EmailService 127.0.0.1 5011
# On terminal 5
python3 node.py InventoryService 127.0.0.1 5011
```
Now send events from at least two nodes (actually, any node can):
Example:

In OrderService:
```bash
send OrderCreated order_id=1001 item=keyboard amount=59.99
```
In PaymentService:
```bash
send PaymentProcessed order_id=1001 status=success txn=abc123
```
All other nodes will print the received events.
