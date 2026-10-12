"""Multi-client TCP chat server. Each client runs in its own thread."""
import argparse
import socket
import threading

clients = {}                 # socket -> username
clients_lock = threading.Lock()


def broadcast(message, sender=None):
    """Send a message to every connected client except the sender."""
    data = (message + "\n").encode("utf-8")
    with clients_lock:
        for sock in list(clients):
            if sock is sender:
                continue
            try:
                sock.sendall(data)
            except OSError:
                pass         # that client's own thread will clean it up


def handle_client(conn, addr):
    try:
        conn.sendall(b"Enter a username: ")
        name = conn.makefile("r", encoding="utf-8").readline().strip()
        if not name:
            return
        with clients_lock:
            clients[conn] = name
        print(f"[+] {name} connected from {addr[0]}:{addr[1]}")
        broadcast(f"* {name} joined the chat", sender=conn)
        conn.sendall(b"Welcome! Type /quit to leave.\n")

        reader = conn.makefile("r", encoding="utf-8")
        for line in reader:
            text = line.strip()
            if text == "/quit":
                break
            if text:
                broadcast(f"{name}: {text}", sender=conn)
    except OSError:
        pass
    finally:
        with clients_lock:
            name = clients.pop(conn, None)
        conn.close()
        if name:
            print(f"[-] {name} disconnected")
            broadcast(f"* {name} left the chat")


def main():
    parser = argparse.ArgumentParser(description="TCP chat server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((args.host, args.port))
    server.listen()
    print(f"Server listening on {args.host}:{args.port} (Ctrl+C to stop)")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
