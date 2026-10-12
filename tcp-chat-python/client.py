"""Chat client: one thread prints incoming messages, the main thread sends yours."""
import argparse
import socket
import sys
import threading


def receive(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            sys.stdout.write(data.decode("utf-8"))
            sys.stdout.flush()
    except OSError:
        pass
    print("\nDisconnected from server.")


def main():
    parser = argparse.ArgumentParser(description="TCP chat client")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((args.host, args.port))
    except OSError as e:
        print(f"Could not connect to {args.host}:{args.port} ({e})")
        return

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    try:
        for line in sys.stdin:
            sock.sendall(line.encode("utf-8"))
            if line.strip() == "/quit":
                break
    except (KeyboardInterrupt, OSError):
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    main()
