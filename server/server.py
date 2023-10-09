
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8888))
server_socket.listen()

def receive_string(so: socket.socket, encoding = "utf-8") -> str:
    """
    Receive a string from the socket by first reasing the size of the str
    and the then the string itself
    """
    length = int.from_bytes(so.recv(4),'big')
    return so.recv(length).decode(encoding)


client_socket, client_addr = server_socket.accept()
print(f'New connection from {client_addr}')
file_name   = receive_string(client_socket)
file_length = int.from_bytes(client_socket.recv(4),'big')
print(f'Receiving {file_name} of size {file_length} bytes')


received_bytes = 0
with open(file_name, 'wb') as fh:
    while received_bytes < file_length:
        buffer = client_socket.recv(1024)
        fh.write(buffer)
        received_bytes += len(buffer)
client_socket.close()
server_socket.close()
