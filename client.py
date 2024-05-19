from socket import *
from threading import *

ip = input("Введите хост сервера> ")
if ip == "std":
    ip = gethostbyname(gethostname())
port = int(input("Введите номер порта> "))
serverAddr = (ip, port)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverAddr)
print("Соединение с сервером установлено")

connected = True
while connected:
    msg = input("> ")
    clientSocket.send(msg.encode())
    if msg == "!DISCONNECT":
        connected = False
    else:
        msglen = int(clientSocket.recv(1024).decode("utf-8"))
        msg = clientSocket.recv(msglen).decode("utf-8")
        print(f"Получено сообщение с сервера: {msg}")
clientSocket.close()
