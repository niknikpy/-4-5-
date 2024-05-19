from socket import *
from threading import *

def handleClient(conn, addr):
    print(f"Соединение {addr} было установленно\r\n")
    connected = True
    while connected:
        msg = conn.recv(1024).decode("utf-8")
        if msg == "!DISCONNECT":
            connected = False
            print(f"Соединение {addr} разорвано")
        elif "!GET" == msg[:4]:
            filename = msg[5:]
            msg = ""
            try:
                with open(filename) as f:
                    data = f.read()
                    for i in range(len(data)):
                        msg += data[i]
                    msg += "\r\n"
                msg = msg.encode()
                conn.send(str(len(msg)).encode())
                conn.sendall(msg)
            except IOError:
                msg = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"
                msg = msg.encode()
                conn.send(str(len(msg)).encode())
                conn.send(msg)
        else:
            print(f"{addr}: {msg}")
            msg = f"Сообщение получено: {msg}"
            msg = msg.encode()
            conn.send(str(len(msg)).encode())
            conn.send(msg)
    conn.close()

ip = gethostbyname(gethostname())
port = 6789
serverAddr = (ip, port)

print("Запуск сервера...")
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddr)
serverSocket.listen()
print("Сервер прослушивает...")

while True:
    print("Готов к работе...")
    connectionSocket, addr = serverSocket.accept()
    thread = Thread(target=handleClient, args=(connectionSocket, addr))
    thread.start()
    print(f"Активных потоков: {active_count()-1}")
    #try:
        #message = connectionSocket.recv(1024)
        #filename = message.split()[1]
        #f = open(filename[1:])
        #outputdata = f.read()
        #connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        #for i in range(len(outputdata)):
            #connectionSocket.send(outputdata[i].encode())
        #connectionSocket.send("\r\n".encode())
        #connectionSocket.close()
    #except IOError:
        #connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        #connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #connectionSocket.close()
serverSocket.close()
