# client.py
import socket
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import threading

from util import generate_key, format_key

def receive_messages(sock, fernet):
    while True:
        try:
            response = sock.recv(1024)
            response_decrypted = fernet.decrypt(response)
            print(f'\nReceived: {response_decrypted.decode()}')
        except:
            break

def main():
    host = input('\nHost to connect: ').strip()
    port = int(input('\nPort to connect: ').strip())

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    # receive username prompt and send username
    username_prompt = sock.recv(1024).decode()
    print(username_prompt)
    username = input().strip()
    sock.send(username.encode())

    common = generate_key()
    secret = generate_key()
    public = common + secret

    # sending common key to server
    sock.send(str(common).encode())

    # getting public key from peer and sending own key
    public_peer = int(sock.recv(1024).decode())
    sock.send(str(public).encode())

    message_secret = secret + public_peer
    print(f'- Encrypt key is: {format_key(message_secret)}')

    key_bytes = message_secret.to_bytes(32, byteorder='little')
    fernet = Fernet(urlsafe_b64encode(key_bytes))

    print('=' * 20)

    receive_thread = threading.Thread(target=receive_messages, args=(sock, fernet))
    receive_thread.start()

    try:
        while True:
            recipient = input('\nRecipient username: ').strip()
            message = input('\nmessage> ').strip()
            message_to_send = f'{recipient} {message}'
            encrypted_msg = fernet.encrypt(message_to_send.encode())
            sock.send(encrypted_msg)
    except KeyboardInterrupt:
        print('\nBye.')
        sock.close()

main()