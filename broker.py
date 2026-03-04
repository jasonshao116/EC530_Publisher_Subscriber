# broker.py
import json
import socket
import threading
from typing import Dict, Tuple

HOST = "0.0.0.0"
PORT = 5011

clients: Dict[socket.socket, Tuple[str, int]] = {}
lock = threading.Lock()

def safe_send(conn: socket.socket, payload: dict):
    data = (json.dumps(payload) + "\n").encode("utf-8")
    conn.sendall(data)

def broadcast(payload: dict, exclude: socket.socket | None = None):
    dead = []
    with lock:
        for c in clients.keys():
            if exclude is not None and c is exclude:
                continue
            try:
                safe_send(c, payload)
            except OSError:
                dead.append(c)
        for c in dead:
            clients.pop(c, None)

def handle_client(conn: socket.socket, addr):
    buf = ""
    try:
        with conn:
            with lock:
                clients[conn] = addr
            print(f"[BROKER] CONNECT {addr}")

            while True:
                data = conn.recv(4096)
                if not data:
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

                    # Forward to everyone else
                    broadcast(msg, exclude=conn)

    finally:
        with lock:
            clients.pop(conn, None)
        print(f"[BROKER] DISCONNECT {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[BROKER] listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()