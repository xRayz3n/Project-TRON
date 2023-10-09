import socket
import class_game

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('172.21.72.112', 8887))
server_socket.listen()
client_socket, client_addr = server_socket.accept()
print(f'New connection from {client_addr}')

input = ""
while True:
    car = client_socket.recv(1).decode("utf-8")
    if car == "\0":
        break
    input += car
print(input)

client_socket.close()
server_socket.close()
