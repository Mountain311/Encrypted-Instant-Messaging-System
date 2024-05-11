# Encrypted Instant Messaging System

## 1. Introduction

Instant messaging (IM) has revolutionized the way we communicate in the digital age, enabling real-time text-based communication between individuals across the globe. This project aims to develop a robust and secure IM system that facilitates instantaneous communication between two users simultaneously. The system comprises a server component responsible for managing message transfers and a client component for user interaction.

The IM system is designed with the following key characteristics:

1. **Real-time Communication**: The system facilitates instantaneous message exchange, allowing users to send and receive messages without noticeable delays.

2. **Two-Party Communication**: The system supports conversations between two individuals concurrently, enabling private and focused communication.

3. **Text-Based Communication**: The primary mode of communication within the system is through text messages, excluding voice and video functionalities.

4. **Network Connectivity**: Users can participate in conversations from remote locations, connected to the system over the internet.

5. **User Interface (Optional)**: The project provides the flexibility to implement a graphical user interface (GUI) for the client component, enhancing the user experience.

The project's implementation encompasses various aspects, including system architecture, design, components, workflow, deployment instructions, and security considerations, which will be discussed in detail throughout this report.

## 2. System Architecture

The IM system follows a client-server architecture, where the server acts as a central hub for managing connections and message transfers, while the clients represent the individual users interacting with the system. The communication between the client and server components is facilitated through sockets, enabling seamless network connectivity.

The system architecture is illustrated in Figure 1 (provided in the project description).

### 2.1. Server Component

The server component is responsible for handling client connections, managing user sessions, and facilitating message transfers between clients. It listens for incoming connections on a specified IP address and port, and upon successful connection, it prompts the client for a username. The server maintains a list of connected clients, along with their respective usernames and encryption keys.

### 2.2. Client Component

The client component serves as the user interface for interacting with the IM system. Upon establishing a connection with the server, the client is prompted to enter a username. Once authenticated, the client can initiate conversations with other connected users by specifying the recipient's username and typing the message content.

### 2.3. Communication Flow

The communication flow between the client and server components follows these steps:

1. The client establishes a connection with the server by providing the server's IP address and port number.
2. The server prompts the client for a username, which is then broadcasted to other connected clients.
3. The client and server exchange encryption keys to enable secure communication.
4. The client specifies the recipient's username and enters the message content.
5. The client encrypts the message using the shared encryption key and sends it to the server.
6. The server decrypts the message, identifies the recipient based on the username, and re-encrypts the message using the recipient's encryption key.
7. The server sends the encrypted message to the intended recipient.
8. The recipient client decrypts the message using the shared encryption key and displays the sender's username and message content.

## 3. Design and Implementation

The IM system is implemented in Python, leveraging the `socket` module for network communication and the `cryptography` library for encryption and decryption operations. The project consists of three main components: `server.py`, `client.py`, and `util.py`.

### 3.1. Server Component (`server.py`)

The `server.py` file contains the implementation of the server component. It includes the following key functionalities:

1. **Server Setup**: The server initializes a socket, binds it to a local IP address and port, and listens for incoming client connections.

2. **Client Handling**: When a new client connects, the server prompts the client for a username and broadcasts the user's join message to other connected clients. It also performs key exchange with the client to establish secure communication.

3. **Message Handling**: The server receives encrypted messages from clients, decrypts them, identifies the intended recipient based on the username, re-encrypts the message using the recipient's key, and forwards the encrypted message to the recipient.

4. **Client Management**: The server maintains a list of connected clients, their usernames, and encryption keys. It handles client disconnections by removing the client from the lists and broadcasting a leave message to other clients.

5. **Broadcasting**: The server can broadcast messages to all connected clients, except the sender, for system-wide notifications or announcements.

### 3.2. Client Component (`client.py`)

The `client.py` file contains the implementation of the client component. It includes the following key functionalities:

1. **Server Connection**: The client prompts the user for the server's IP address and port number, establishes a connection with the server, and sends the user's username.

2. **Key Exchange**: The client performs a key exchange with the server to establish secure communication.

3. **Message Sending**: The client prompts the user for the recipient's username and message content, encrypts the message using the shared encryption key, and sends the encrypted message to the server.

4. **Message Receiving**: The client listens for incoming encrypted messages from the server, decrypts them using the shared encryption key, and displays the sender's username and message content.

5. **Multi-threading**: The client utilizes multi-threading to simultaneously handle message sending and receiving, ensuring a seamless user experience.

### 3.3. Utility Module (`util.py`)

The `util.py` file contains utility functions used by both the server and client components. It includes the following functionalities:

1. **Key Generation**: The `generate_key()` function generates a random key of a specified length (128 bits) using the `secrets` module.

2. **Key Formatting**: The `format_key()` function formats the generated key into a more readable format by inserting spaces every four characters.

### 3.4. Encryption and Security

To ensure secure communication between clients, the IM system employs encryption techniques using the `cryptography` library. The encryption process follows these steps:

1. **Key Exchange**: When a client connects to the server, they exchange encryption keys using a secure key exchange protocol. The server generates a common key and a secret key, combines them to form a public key, and sends the common key to the client. The client generates its own secret key, combines it with the received common key to form its public key, and sends it back to the server.

2. **Key Derivation**: Both the client and server derive the final encryption key by combining their respective secret keys with the received public key from the other party.

3. **Encryption and Decryption**: The `Fernet` class from the `cryptography.fernet` module is used for encryption and decryption operations. Messages are encrypted before being sent and decrypted upon receipt, ensuring end-to-end security.

4. **Key Management**: The server maintains a dictionary of connected clients and their respective encryption keys, facilitating secure communication between clients.

## 4. Deployment and Usage

To deploy and use the IM system, follow these steps:

1. **Dependencies**: Ensure that you have Python 3.x installed on your system. Additionally, install the required dependencies.
   
2. **Server Setup**: Run the `server.py` file on the machine that will act as the server. The server will print its IP address and port number, which clients will need to connect.

3. **Client Setup**: On the client machines, run the `client.py` file. When prompted, enter the server's IP address and port number to establish a connection.

4. **Username Entry**: Both the server and clients will prompt for a username. Enter a unique username to identify yourself in the IM system.

5. **Messaging**: Once connected, the client will display a prompt to enter the recipient's username and the message content. Type the recipient's username and your message, then press Enter to send the message.

6. **Receiving Messages**: When the intended recipient receives a message, it will be displayed on their console with the sender's username and message content.

7. **Disconnecting**: To disconnect from the IM system, press `Ctrl+C` on the client console. The client will gracefully disconnect, and the server will broadcast a leave message to other connected clients.

## 5. Conclusion

The Instant Messaging System project successfully implements a secure and real-time communication platform for two-party text-based messaging. The system leverages Python's socket programming capabilities and the cryptography library to facilitate secure communication between clients. The client-server architecture, encryption techniques, and multi-threading ensure a robust and efficient messaging experience.

The project demonstrates the application of various concepts, including network programming, client-server communication, encryption and decryption, and multi-threading. It provides a solid foundation for further enhancements and additional features, such as group messaging, file transfers, and graphical user interfaces.
