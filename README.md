[README.md](https://github.com/user-attachments/files/33318646/README.md)
# TCP Chat (Python)

A multi-client chat room built on raw TCP sockets. One server accepts many clients, and each message is broadcast to everyone else.

## Concepts used
- TCP client/server model with Python's `socket` module
- Multithreading (one thread per client) and a `Lock` to protect shared state
- Message broadcasting and clean disconnect handling
- Command-line arguments with `argparse`

## Run it
Open three terminals.

```bash
# Terminal 1: start the server
python server.py

# Terminals 2 and 3: connect clients
python client.py
```
Type `/quit` to leave. Use `--host` and `--port` to run across machines on the same network, for example `python server.py --host 0.0.0.0 --port 6000`.

Requires Python 3.8 or newer. No external packages.
