import socket
import threading

def client_handler(connection, address):
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                print(f"{address} says {message}")
                broadcast(message, connection)
            else:
                remove(connection)
                break
        except:
            continue

def broadcast(message, connection):
    for client in clients:
        try:
            client.send(message.encode())
        except:
            remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 9999))
    server.listen()
    print("Server started, listening for connections...")
    
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        print(f"{addr} connected.")
        threading.Thread(target=client_handler, args=(conn, addr)).start()

clients = []
start_server()
