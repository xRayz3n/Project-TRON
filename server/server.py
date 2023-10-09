
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8888))
server_socket.listen()
client_socket, client_addr = server_socket.accept()
print(f'New connection from {client_addr}')

while True:
    input = ""
    car = client_socket.recv(1).decode("utf-8")
    if car == "\0":
        break
    input += car

client_socket.close()
server_socket.close()
