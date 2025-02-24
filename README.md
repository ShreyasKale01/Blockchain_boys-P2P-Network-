# Blockchain_boys-P2P-Network-
Its an Peer to Peer Chat Application using TCP protocol.

Team Member Names: 
1.Anshul Garg: 230004006
2.Shreyas Kale: 230051006
3.Abinsh Aacharya: 230004002
4.Maanas : 230041020

This Chatbot also solves the bonus question in the assignment

# P2P Chat Application

This is a simple Peer-to-Peer (P2P) chat application that allows users to communicate directly without a centralized server. It enables real-time messaging between connected peers.

---

## Features
- Decentralized communication using socket programming.
- Supports multiple peers.
- Allows sending and receiving messages.
- Tracks active and known peers.
- Connects to mandatory peers at startup.

---

## Requirements
- Python 3.x
- A local network or direct peer connectivity.

---

## Installation & Usage

### 1. **Run the Application**
Execute the script using Python:
python Blockchain_boys.py

### 2. **Set Up Your Peer**
- Enter a unique **Team Name** (without spaces).
- Choose a **port number** for your peer.

### 3. **Menu Options**
After setup, the program presents a menu:

1. **Send Message**
   - Enter the recipient’s IP and port.
   - Type a message and send.
   
2. **Query Active Peers**
   - Displays the list of known peers and their connection status.
   
3. **Connect to Active Peers**
   - Connects to all or selected peers.

0. **Quit**
   - Notifies peers and exits.

---

## Network Communication
- **Messages are sent as:**  
  `Sender_IP:Port Name Message`
- Peers are added dynamically when messages are received.
- The program automatically attempts to connect to predefined mandatory peers.

---

## Example Usage
1. Start the application and enter a **team name** and **port**.
2. Use option `1` to send a message to another peer.
3. Check active peers using option `2`.
4. Connect to peers using option `3`.
5. Exit using option `0`.

---

## Notes
- Ensure that firewall settings allow connections to the chosen port.
- The program runs a server in the background for receiving messages.
- If a peer disconnects, it is removed from the active list.





