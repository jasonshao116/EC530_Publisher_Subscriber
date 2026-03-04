# node.py
import json
import socket
import threading
import time
import uuid
import sys

EVENT_TYPES = {
    "OrderCreated",
    "PaymentProcessed",
    "EmailSent",
    "OrderCancelled",
}

def recv_loop(sock: socket.socket, node_name: str):
    buf = ""
    while True:
        data = sock.recv(4096)
        if not data:
            print(f"[{node_name}] broker closed connection")
            break
        buf += data.decode("utf-8", errors="replace")
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Pretty print received event
            et = msg.get("event_type")
            src = msg.get("source")
            payload = msg.get("payload")
            ts = msg.get("ts")
            print(f"\n[{node_name} RECEIVED] {et} from={src} ts={ts} payload={payload}")
            print(f"[{node_name} SEND] ", end="", flush=True)

def send_event(sock: socket.socket, node_name: str, event_type: str, payload: dict):
    msg = {
        "id": str(uuid.uuid4()),
        "ts": time.time(),
        "source": node_name,
        "event_type": event_type,
        "payload": payload,
    }
    sock.sendall((json.dumps(msg) + "\n").encode("utf-8"))

def parse_kv_pairs(parts):
    payload = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            payload[k] = v
    return payload

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 node.py <NODE_NAME> [HOST] [PORT]")
        sys.exit(1)

    node_name = sys.argv[1]
    host = sys.argv[2] if len(sys.argv) >= 3 else "127.0.0.1"
    port = int(sys.argv[3]) if len(sys.argv) >= 4 else 5011

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[{node_name}] connected to broker at {host}:{port}")

        threading.Thread(target=recv_loop, args=(s, node_name), daemon=True).start()

        print(f"[{node_name}] event types: {sorted(EVENT_TYPES)}")
        print(f"[{node_name}] command format:")
        print(f"  send <EventType> key=value key=value ...")
        print(f"  ex: send OrderCreated order_id=123 amount=49.99")
        print(f"  type 'quit' to exit")

        while True:
            cmd = input(f"[{node_name} SEND] ").strip()
            if cmd.lower() in {"quit", "exit"}:
                break

            parts = cmd.split()
            if len(parts) < 2 or parts[0].lower() != "send":
                print("Invalid. Use: send <EventType> key=value ...")
                continue

            event_type = parts[1]
            if event_type not in EVENT_TYPES:
                print(f"Unknown event type: {event_type}")
                continue

            payload = parse_kv_pairs(parts[2:])
            send_event(s, node_name, event_type, payload)

if __name__ == "__main__":
    main()