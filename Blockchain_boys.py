import socket
import threading

connected_peers = set()

def launch_server(host_ip, host_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host_ip, host_port))
    server_socket.listen(5)
    print(f"[SERVER] Running on {host_ip}:{host_port}")

    while True:
        client_conn, client_addr = server_socket.accept()
        threading.Thread(target=process_client, args=(client_conn, client_addr)).start()

def process_client(client_conn, client_addr):
    try:
        data = client_conn.recv(1024).decode().strip()
        if data:
            details = data.split(" ", 2)
            if len(details) == 3:
                sender_data, group_name, message_content = details
                sender_ip, sender_port = sender_data.split(":")
                sender_port = int(sender_port)

                connected_peers.add((sender_ip, sender_port))
                print(f"[MESSAGE] {sender_ip}:{sender_port} ({group_name}): {message_content}")
            else:
                print("[WARNING] Received malformed message.")
    except Exception as error:
        print(f"[ERROR] Message processing failed: {error}")
    finally:
        client_conn.close()

def transmit_message(dest_ip, dest_port, local_port, group_name, content):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        client_socket.connect((dest_ip, dest_port))
        
        formatted_content = f"{local_ip}:{local_port} {group_name} {content}"
        client_socket.send(formatted_content.encode())
        print(f"[SENT] Message to {dest_ip}:{dest_port}")

        response = client_socket.recv(1024).decode().strip()
        if response:
            print(f"[RESPONSE] From peer: {response}")
    except Exception as error:
        print(f"[ERROR] Failed to send message to {dest_ip}:{dest_port} - {error}")
    finally:
        client_socket.close()

def display_peers():
    if connected_peers:
        print("\n[ACTIVE PEERS]")
        for peer in connected_peers:
            print(f"-> {peer[0]}:{peer[1]}")
    else:
        print("[INFO] No active peers available.")

def initiate_connections(local_port, group_name):
    if not connected_peers:
        print("[INFO] No peers to connect to.")
        return

    for peer_ip, peer_port in connected_peers:
        print(f"[CONNECTING] Attempting {peer_ip}:{peer_port}...")
        transmit_message(peer_ip, peer_port, local_port, group_name, "Hello, establishing connection!")

def main():
    host_ip = input("Enter your IP (Use 0.0.0.0 for all networks): ").strip()
    host_port = int(input("Enter your port: ").strip())
    group_name = input("Enter your group/team name: ").strip()

    threading.Thread(target=launch_server, args=(host_ip, host_port), daemon=True).start()

    while True:
        print("\n==== MENU ====")
        print("1. Send Message")
        print("2. Show Active Peers")
        print("3. Connect to Peers")
        print("0. Exit")

        option = input("Choose an option: ").strip()

        if option == "1":
            recipient_ip = input("Recipient IP: ").strip()
            recipient_port = int(input("Recipient Port: ").strip())
            msg_content = input("Message: ").strip()
            transmit_message(recipient_ip, recipient_port, host_port, group_name, msg_content)

        elif option == "2":
            display_peers()

        elif option == "3":
            initiate_connections(host_port, group_name)

        elif option == "0":
            print("[EXIT] Shutting down...")
            break

if __name__ == "__main__":
    main()
