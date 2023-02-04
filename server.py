import socket
import threading


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "Exit!"

#Defined allowed IPs & Ports
ALLOWED_IPS =['127.0.0.1', '', '']
ALLOWED_PORTS=[80,443,22,5050]
# Defined a lock to synchronize access to the firewall rule
lock = threading.Lock()
# Create TCP/ICP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDR)

#List of connected clients
clients =[]

def broadcast(msg, conn):
    for client in clients:
        #Don't send msg to the sender
        if client != conn:
            client.send(msg)


def handle_client(conn, addr):
    try:
        clients.append(conn)
        client_ip, client_port = addr
        print(f"[+] [New Connection] {client_ip}:{client_port} connected")

        #Recieve data from client
        connected = True
        while connected:
            #Filter incoming traffic
            with lock:
                if client_ip not in ALLOWED_IPS:
                    print(f"[+] [IP is blacklisted or unknown] {client_ip}:{client_port} connection is being terminated")
                    connected = False
            
            # Filter outgoing traffic
            with lock:
                 if client_port not in ALLOWED_PORTS:
                     print(f"[+] [Port is not allowed] {client_ip}:{client_port} connection is being terminated")
                     connected = False
    
            msg_len = conn.recv(HEADER).decode(FORMAT)
            #Checking if msg is not none
            if msg_len:
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(FORMAT)
                if msg == DISCONNECT_MSG:
                    connected = False
                    #conn.send("Exit!".encode(FORMAT))
                print(f"[+] Message from {addr}: {msg}")
                #Broadcast to all connected clients
                broadcast(msg.encode(FORMAT), conn)
                #Send msg to client
                conn.send("Messsage received".encode(FORMAT))
    #Remove client after disconnect msg is sent        
    finally:
        clients.remove(conn)
        conn.close()

def add_rule(ip, port, direction):
    with lock:
        if direction == 'in':
            ALLOWED_IPS.append(ip)
        elif direction == 'out':
            ALLOWED_PORTS.append(port)

def remove_rule(ip, port, direction):
    with lock:
        if direction == 'in':
            ALLOWED_IPS.remove(ip)
        elif direction == 'out':
            ALLOWED_PORTS.remove(port)

def modify_rule(old_ip, old_port, new_ip, new_port, direction):
    with lock:
        if direction == 'in':
            ALLOWED_IPS.remove(old_ip)
            ALLOWED_IPS.append(new_ip)
        elif direction == 'out':
            ALLOWED_PORTS.remove(old_port)
            ALLOWED_PORTS.append(new_port)

def start():
    #Setting socket to listen for connection
    server.listen()
    print(f"[+] [Listening] Server is listening on {SERVER}")
    #Awaiting connection
    while True:
        print("[+] Waiting for a connection....")
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
        print(f"[+] [Active Connections] {threading.active_count() - 1}")


print("[+] Server is starting...")
start()