import socket

HEADER = 64
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostbyname())
SERVER = '' #<- May need to edit
SERVER_ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "Exit!"

# Create TCP/ICP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

#Send msgs to server
def send(msg):
    msg = msg.encode(FORMAT)
    msg_len = len(msg)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(msg)
    print(client.recv(2048).decode(FORMAT))

# Read messages from the server
# def receive():
#     data = client.recv(HEADER).decode(FORMAT)
#     if data:
#         msg_len = int(data)
#         msg = client.recv(msg_len).decode(FORMAT)
#         return msg
#     return None

#Take user input
def text():
    print("[+] Welcome! Enter text, type 'Exit!' to disconnect")
    while True:
        entered_text = input()
        send(entered_text)
        if entered_text == DISCONNECT_MSG:
            break
        # received_msg = receive()
        # if received_msg:
        #     print(received_msg)
text()