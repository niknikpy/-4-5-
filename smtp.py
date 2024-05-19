from socket import * 
from base64 import *
import ssl
import os

def send_SMTP(socket, data = "", code = "250", b64encoding = False, file="".encode()):
    if data != "":
        if b64encoding:
            command = b64encode(data.encode()) + "\r\n".encode()
        else:
            command = data.encode() + file + "\r\n".encode()
        socket.send(command)
    recv = socket.recv(1024).decode("UTF-8")
    print(recv)
    if recv[:3] != code:
        print(f"Код {code} от сервера не получен")
        exit()
        
def send_MSG(socket, data, attachments = []):
    header = "MIME-Version: 1.0\r\n"
    header += "Content-Type: multipart/mixed; boundary=bd42\r\n"
    bd = "--bd42\r\n"
    headertxt = "Content-Type: text/plain; charset=UTF-8\r\nContent-Disposition: inline\r\n"
    command = (header+bd+headertxt+data+"\r\n").encode()
    for filename in attachments:
        fname = os.path.basename(filename)
        headerAtt = f"Content-Type: image/png\r\nContent-Disposition: attachment; filename={fname}\r\n"
        headerAtt += "Content-Transfer-Encoding: base64\r\n"
        with open(filename, 'rb') as f:
            fdata = b64encode(f.read())
        command += (bd+headerAtt).encode() + fdata + "\r\n".encode()
    command += ".\r\n".encode()
    socket.send(command)
    recv = socket.recv(1024).decode("UTF-8")
    print(recv)
    if recv[:3] != "250":
        print("Код 250 от сервера не получен")
        exit()

with open("email.txt", 'r') as f:
    data = f.read().split(" ")
    emailUser = data[0]
    emailPass = f"{data[1]} {data[2]} {data[3]} {data[4]}"

# Выбираем почтовый сервер
mailserver = "smtp.gmail.com"
# Создаем сокет clientSocket и устанавливаем TCP-соединение
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 587))

send_SMTP(clientSocket, code="220")
# Отправляем команду HELO и выводим ответ сервера.
send_SMTP(clientSocket, "HELO Alice")
send_SMTP(clientSocket, "STARTTLS", "220")
sslClientSocket = ssl.create_default_context().wrap_socket(clientSocket, server_hostname=mailserver)
send_SMTP(sslClientSocket, "HELO Alice")

send_SMTP(sslClientSocket, "AUTH LOGIN", "334")
send_SMTP(sslClientSocket, emailUser, "334", True)
send_SMTP(sslClientSocket, emailPass, "235", True)
# Отправляем команду MAIL FROM и выводим ответ сервера.
send_SMTP(sslClientSocket, "MAIL FROM:<MySMTP@gmail.ru>")
# Отправляем команду RCPT TO и выводим ответ сервера.
send_SMTP(sslClientSocket, f"RCPT TO:<{emailUser}>")
# Отправляем команду DATA и выводим ответ сервера.
send_SMTP(sslClientSocket, "DATA", "354") 
# Отправляем данные сообщения.
attachments = []
msg = input("Введите сообщение: ")
while True:
    data = input("Введите название файла или 'q' если больше файлов нет: ")
    if data == "q":
        break
    attachments.append(data)
    
send_MSG(sslClientSocket, msg, attachments)
# Отправляем команду QUIT, получаем ответ сервера
send_SMTP(sslClientSocket, "QUIT", "221")
# Закрываем соединение. 
clientSocket.close()
print("Соединение закрыто")
