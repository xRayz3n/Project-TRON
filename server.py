import socket
import threading
import multiprocessing
import class_game
import player
import packets
playerConnection_queue = multiprocessing.Queue()
playerList = []

def OpenConnections(): #keeps the connection open
    server_socket.listen()
    print("Opening server...")
    while True:
        client_socket, client_addr = server_socket.accept()
        print(f'New connection from {client_addr}')
        threading.Thread(group=None, target=GetPlayers,args=[client_socket,client_addr]).start()

def GetPlayers(client_socket, client_addr): #acquire player info

    #nickname = client_socket.recv(16).decode("utf-8") #receive player nickname, 16 char max
    nickname = packets.Packets.receive(client_socket)[1]
    print(f"Ip {client_addr} named to {nickname}")
    playerInfo = player.Player(client_socket, client_addr,nickname)
    playerList.append(player)
    while True:
        try:
            type, status = packets.Packets.receive(client_socket)
        except:
            print(f"Connection lost from {playerInfo.name}")
            client_socket.close()
            break
        if status == "ready":
            playerInfo.state = "ready"
            print(f"{playerInfo.name} is now ready")
        if status == "unready":
            playerInfo.state = "unready"
            print(f"{playerInfo.name} is now unready")

        print(status)



if __name__ == '__main__':

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8889))
    connection_thread = threading.Thread(group=None, target=OpenConnections)
    connection_thread.start()