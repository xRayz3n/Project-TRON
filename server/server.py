import socket
import threading
import multiprocessing
import class_game

playerConnection_queue = multiprocessing.Queue()

def OpenConnections(): #keeps the connection open

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('172.21.72.112', 8887))
    while True:
        
        print("Looking for the next player...")
        server_socket.listen()
        client_socket, client_addr = server_socket.accept()
        playerConnection_queue.put(client_socket)
        print(f'New connection from {client_addr}')
        threading.Thread(group=None, target=GetPlayers,args=client_socket).start()

def GetPlayers(client_socket): #acquire player info

    nickname = client_socket.recv(16).decode("utf-8") #receive player nickname, 16 char max
    print(nickname)


connection_thread = threading.Thread(group=None, target=OpenConnections)
connection_thread.start()
"""
input = ""
while True:
    car = client_socket.recv(1).decode("utf-8")
    if car == "\0":
        break
    input += car
print(input)
"""

#server_socket.close()