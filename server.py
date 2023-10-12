import socket
import threading
import multiprocessing
import class_game
import player
import packets
import os
import time
playerConnection_queue = multiprocessing.Queue()
playerList = []

maxplayers = 4

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
    playerList.append(playerInfo)

    message = f"{playerInfo.name} is the player {playerList.index(playerInfo) + 1}, "
    Broadcast_ToAllPlayers(message, "I")

    while True:
        try:
            type, status = packets.Packets.receive(client_socket)
        except: print("weird thing")

        match status:
            case "disconnect":
                print(f"Connection lost from {playerInfo.name}")
                playerList.remove(playerInfo)
                client_socket.close()
                break
            case "ready":
                playerInfo.state = "ready"
                print(f"{playerInfo.name} is now ready")
                Broadcast_ToAllPlayers(f"{playerInfo.name} is now ready", "I")
                break
            case "unready":
                playerInfo.state = "unready"
                print(f"{playerInfo.name} is now unready")
                Broadcast_ToAllPlayers(f"{playerInfo.name} is no more ready", "I")
            case "ls": #Send the list of players to the command sender
                message = "\nPlayer list: "
                for i in range(0,len(playerList)):
                    aPlayer = playerList[i]
                    message += f"\nPlayer {i + 1}: {aPlayer.name} "
                packets.Packets(message, package_type="I").send(client_socket)
            case _:
                print("something went wrong in server.py/getplayers")
        
        
            
        print(f"{playerInfo.name}: {status}")

def Broadcast_ToAllPlayers(message, type):
    for playerInfo in playerList:
        packet = packets.Packets(message, package_type=type)
        packet.send(playerInfo.client_socket)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    threading.Thread(group=None, target=OpenConnections).start()
    while True:
        if all(aPlayer.state == "ready" for aPlayer in playerList) and len(playerList)>1:
            message = ('All players are ready, starting in')
            Broadcast_ToAllPlayers(message, "I")
            for i in range(3,0,-1):
                Broadcast_ToAllPlayers(f"\n{i}...", 'I')
                time.sleep(1)
            Broadcast_ToAllPlayers("Game started!", "I")
            Broadcast_ToAllPlayers(1, "T")
            print("Game started")
            class_game.Game(playerList,(100,100), 10)