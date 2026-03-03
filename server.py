# server.py
import socket
import threading

HOST = "0.0.0.0"
PORT = 5011

clients = []
clients_lock = threading.Lock()

def recv_loop(conn: socket.socket, addr):
    """Receive messages from ONE client."""
    try:
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                msg = data.decode("utf-8", errors="replace").rstrip()
                print(f"[FROM {addr}] {msg}")
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        print(f"[DISCONNECT] {addr}")

def accept_loop(server_sock: socket.socket):
    """Accept new clients forever."""
    while True:
        conn, addr = server_sock.accept()
        print(f"[CONNECT] {addr}")
        with clients_lock:
            clients.append(conn)
        threading.Thread(target=recv_loop, args=(conn, addr), daemon=True).start()

def broadcast(msg: str):
    dead = []
    with clients_lock:
        for c in clients:
            try:
                c.sendall((msg + "\n").encode("utf-8"))
            except OSError:
                dead.append(c)
        for c in dead:
            clients.remove(c)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] listening on {HOST}:{PORT}")

        threading.Thread(target=accept_loop, args=(s,), daemon=True).start()

        # Transmitter: type in terminal -> send to all clients
        while True:
            text = input("[SERVER SEND] ")
            if text.strip().lower() in {"quit", "exit"}:
                print("[SERVER] shutting down")
                break
            broadcast(text)

if __name__ == "__main__":
    main()