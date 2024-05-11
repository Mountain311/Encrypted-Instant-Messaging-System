# server.py
import socket
import netifaces as ni
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import threading

from util import generate_key, format_key

SERVER_PORT = 5500

clients = {}
keys = {}
usernames = {}



def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # Doesn't need to be reachable
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"  # If not connected to any network, use loopback
    finally:
        s.close()
    return IP


def handle_client(conn, addr):
    print(f"New connection from {addr}")

    # get username
    conn.send(b"Enter your username: ")
    username = conn.recv(1024).decode().strip()
    usernames[conn] = username
    broadcast(f"{username} has joined the chat", conn)

    # keys received and generated
    common = int(conn.recv(1024).decode())
    secret = generate_key()
    public = common + secret

    # sending "public" key and waiting for peer's public key
    conn.send(str(public).encode())
    public_peer = int(conn.recv(1024).decode())
    message_secret = public_peer + secret

    key_bytes = message_secret.to_bytes(32, byteorder="little")
    fernet = Fernet(urlsafe_b64encode(key_bytes))

    keys[conn] = fernet
    clients[conn] = conn

    while True:
        try:
            data = conn.recv(1024)
            decrypted_data = fernet.decrypt(data)
            handle_message(decrypted_data, conn)
        except:
            remove_client(conn)
            break


def handle_message(message, sender):
    parts = message.decode().split(" ", 1)
    recipient_username = parts[0]
    message_content = parts[1]

    for conn, username in usernames.items():
        if username == recipient_username:
            recipient_conn = conn
            break
    else:
        sender_username = usernames[sender]
        sender.send(f"User {recipient_username} not found".encode())
        return

    sender_username = usernames[sender]
    encrypted_msg = keys[recipient_conn].encrypt(
        f"{sender_username}: {message_content}".encode()
    )
    recipient_conn.send(encrypted_msg)


def broadcast(message, sender):
    for client in clients.values():
        if client != sender:
            try:
                encrypted_msg = keys[client].encrypt(message.encode())
                client.send(encrypted_msg)
            except:
                remove_client(client)


def remove_client(conn):
    if conn in keys:
        username = usernames[conn]
        del keys[conn]
        del clients[conn]
        del usernames[conn]
        conn.close()
        broadcast(f"{username} has left the chat", conn)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((get_local_ip(), SERVER_PORT))
    server_socket.listen(5)

    print(f"Server listening on {server_socket.getsockname()}\n")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    main()
