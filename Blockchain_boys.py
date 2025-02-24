import socket
import threading
import time

# Global variables
active_peers = []
known_peers = set()
connected_peers = set()
peer_names = {}
lock = threading.Lock()
mandatory_peers = [('10.206.5.228', 6555)]

def start_server(port, name):
    """Starts the server to listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)
        print(f"\nServer listening on port {port}\n")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, name), daemon=True).start()

def handle_client(client_socket, name):
    """Handles incoming messages from peers."""
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            return
        
        try:
            sender_address, sender_name, message = data.split(" ", 2)
            sender_ip, sender_port = sender_address.split(":")
            sender_port = int(sender_port)
        except ValueError:
            return

        with lock:
            peer_names[(sender_ip, sender_port)] = sender_name

            if message.lower() == 'exit':
                active_peers[:] = [peer for peer in active_peers if peer != (sender_ip, sender_port)]
                known_peers.discard((sender_ip, sender_port))
                connected_peers.discard((sender_ip, sender_port))
                print(f"\n{sender_name} [{sender_ip}:{sender_port}] disconnected\n")
            else:
                if (sender_ip, sender_port) not in active_peers:
                    active_peers.append((sender_ip, sender_port))
                    print(f"\nNew peer found: {sender_name} [{sender_ip}:{sender_port}]")
                known_peers.add((sender_ip, sender_port))
                print(f"\nMessage from {sender_name} [{sender_ip}:{sender_port}]: {message}\n")
    finally:
        client_socket.close()

def send_message(ip, port, sender_name, sender_port, message):
    """Sends a message to a specific peer."""
    sender_ip = socket.gethostbyname(socket.gethostname())
    data = f"{sender_ip}:{sender_port} {sender_name} {message}"

    with lock:
        remote_name = peer_names.get((ip, port), "Unknown")

    try:
        with socket.create_connection((ip, port), timeout=5) as s:
            s.send(data.encode())

        with lock:
            if message.lower() == 'exit':
                known_peers.discard((ip, port))
                connected_peers.discard((ip, port))
                active_peers[:] = [peer for peer in active_peers if peer != (ip, port)]
            else:
                known_peers.add((ip, port))

        print(f"Message sent to {remote_name} [{ip}:{port}]: {message}")
        return True
    except Exception as e:
        print(f"Failed to contact {remote_name} [{ip}:{port}] - Error: {e}")
        return False

def connect_to_peer(ip, port, sender_name, sender_port):
    """Attempts to establish a connection with a peer."""
    if send_message(ip, port, sender_name, sender_port, "connect"):
        with lock:
            connected_peers.add((ip, port))

def main():
    """Main function handling user interaction."""
    while True:
        name = input("Enter Team Name (no spaces): ").strip()
        if " " not in name:
            break
        print("\nThe entered name contains spaces\n")

    try:
        port = int(input("Enter your port number: "))
    except ValueError:
        print("Invalid port number. Exiting.")
        return

    threading.Thread(target=start_server, args=(port, name), daemon=True).start()
    time.sleep(0.2)

    with lock:
        peer_names[('10.206.5.228', 6555)] = "Subhra Mazumdar Maam"

    for ip, peer_port in mandatory_peers:
        threading.Thread(target=send_message, args=(ip, peer_port, name, port, "Hello!"), daemon=True).start()

    while True:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query active peers")
        print("3. Connect to active peers")
        print("0. Quit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            ip = input("\nEnter recipient's IP address: ")
            try:
                port_peer = int(input("Enter recipient's port number: "))
            except ValueError:
                print("Invalid port number.")
                continue

            message = input("Enter your message (type 'exit' to disconnect): ")
            send_message(ip, port_peer, name, port, message)

        elif choice == '2':
            with lock:
                if known_peers:
                    print("\nActive Peers:")
                    for i, (peer_ip, peer_port) in enumerate(known_peers, 1):
                        peer_name = peer_names.get((peer_ip, peer_port), "Unknown")
                        status = "Connected" if (peer_ip, peer_port) in connected_peers else "Not connected."
                        print(f"{i}. {peer_name} [{peer_ip}:{peer_port}] - {status}")
                else:
                    print("\nNo active peers.")

        elif choice == '3':
            with lock:
                peers_to_connect = [peer for peer in known_peers if peer not in connected_peers]

            if peers_to_connect:
                print("\nActive Peers remaining for connection:\n")
                for idx, (peer_ip, peer_port) in enumerate(peers_to_connect, 1):
                    peer_name = peer_names.get((peer_ip, peer_port), "Unknown")
                    print(f"{idx}. {peer_name} [{peer_ip}:{peer_port}]")

                try:
                    selection = int(input("\nEnter the index of the peer to connect to (0 to connect to all): ").strip())
                except ValueError:
                    print("Invalid input.")
                    continue

                if selection == 0:
                    for peer_ip, peer_port in peers_to_connect:
                        threading.Thread(target=connect_to_peer, args=(peer_ip, peer_port, name, port), daemon=True).start()
                elif 1 <= selection <= len(peers_to_connect):
                    peer_ip, peer_port = peers_to_connect[selection - 1]
                    threading.Thread(target=connect_to_peer, args=(peer_ip, peer_port, name, port), daemon=True).start()
                else:
                    print("Invalid input.")

        elif choice == '0':
            for peer_ip, peer_port in list(known_peers):
                send_message(peer_ip, peer_port, name, port, "exit")
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
