# client.py
import socket
import threading
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000

def recv_loop(sock: socket.socket):
    while True:
        data = sock.recv(4096)
        if not data:
            print("[CLIENT] server closed connection")
            break
        print("[FROM SERVER]", data.decode("utf-8", errors="replace").rstrip())

def main():
    host = SERVER_HOST
    port = SERVER_PORT
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[CLIENT] connected to {host}:{port}")

        threading.Thread(target=recv_loop, args=(s,), daemon=True).start()

        while True:
            text = input("[CLIENT SEND] ")
            if text.strip().lower() in {"quit", "exit"}:
                break
            s.sendall((text + "\n").encode("utf-8"))

if __name__ == "__main__":
    main()