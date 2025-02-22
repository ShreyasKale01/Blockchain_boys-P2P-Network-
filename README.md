# Blockchain_boys-P2P-Network-
Its an Peer to Peer Chat Application using TCP protocol.

Team Member Names: 
1.Anshul Garg: 230004006
2.Shreyas Kale: 230051006
3.Abinsh Aacharya: 230004002
4.Maanas : 230041020

This Chatbot also solves the bonus question in the assignment


# Peer-to-Peer Chat Application

## Introduction
This is a **Peer-to-Peer (P2P) Chat Application** that allows multiple users to communicate directly over a network without relying on a central server. Each peer can send and receive messages while maintaining a list of active connections.

## Features
- Start a local chat server
- Send messages to other peers
- Maintain a list of active peers
- Connect to known peers dynamically

## Requirements
- Python 3.x
- Socket and Threading modules (pre-installed in Python)

## Installation
1. Clone or download this repository.
2. Ensure Python is installed on your system.
3. Run the script using:
   ```sh
   python Blockchain_boys.py
   ```

## How to Use
### 1. Start the Chat Server
- Run the script: `python Blockchain_boys.py`
- Enter your **IP address** (Use `0.0.0.0` to allow connections from all networks)
- Enter a **port number** (e.g., `5000`)
- Enter a **group name** to identify the chat group

### 2. Menu Options
Once the server starts, you will see a menu:
```
==== MENU ====
1. Send Message
2. Show Active Peers
3. Connect to Peers
0. Exit
```

#### **Option 1: Send a Message**
- Enter the recipient's IP and port.
- Type your message and send it.

#### **Option 2: Show Active Peers**
- Displays all connected peers.

#### **Option 3: Connect to Peers**
- Attempts to establish a connection with known peers.

#### **Option 0: Exit**
- Shuts down the application.

## Example Usage
1. **User A** starts the server on IP `192.168.1.10` and port `5000`.
2. **User B** starts their server on IP `192.168.1.11` and port `6000`.
3. **User A** sends a message to `192.168.1.11:6000`.
4. **User B** receives the message and can reply back.

## Troubleshooting
- **Connection errors?** Check firewall settings and ensure ports are open.
- **Peer not receiving messages?** Ensure both peers are using the correct IP and port.
- **Server not starting?** Make sure no other process is using the chosen port.

## Future Improvements
- Encrypt messages for better security.
- Implement NAT traversal for better peer connectivity.
- Add a user-friendly GUI.

## License
This project is open-source and free to use.

## Author
Developed by Blockchain Boys 🚀

