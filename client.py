import socket 
import packets
import threading
import multiprocessing
import os
import pygame as pg
import time
import gameclient
os.system('clear')

def Connect(ip_addr : str, port : int) -> socket.socket:
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((ip_addr, port))
    print("Connected")
    return sck

def IsDisconnected(sck, status) -> bool:
    if status == "disconnect":
            print(f"Connection lost from server")
            sck.close()
            return True
    return False
def Lobby(sck):
    to_send = input("Set your nickname: ")
    nickname_packet = packets.Packets(to_send,package_type='I')
    nickname_packet.send(sck)
    print(f"Your nickname is {to_send}")
    threading.Thread(group=None, target=ReceiveMsg, args=[sck]).start()
    while True:
        status = input("\nType 'ready' when you are: ")
        ready_packet = packets.Packets(status, package_type="I")
        ready_packet.send(sck)

def ReceiveMsg(sck):
     while True:
        status, message = packets.Packets.receive(sck)
        #os.system('clear')
        if IsDisconnected(sck, message):
            break
        if status == "T" and message == 1:
            GameClient(sck)
        
        print(message)
    
def GameClient(sck):
    pg.init()
    threading.Thread(group=None, target=Take_inputs, args=[sck]).start()
    screen = pg.display.set_mode((1000, 1000))
    while True:
        status, packet = packets.Packets.receive(sck)
        if status == 'M':
            game = gameclient.GameClient(packet)
        if status == 'U':
            game.Update_Positions(packet)
            Render_game(screen, game.map)



def Take_inputs(sck):
    while True:
        direction = " "
        for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        direction = "W"
                    if event.key == pg.K_RIGHT:
                        direction = "E"
                    if event.key == pg.K_UP:
                        direction = "N"
                    if event.key == pg.K_DOWN:
                        direction = "S"
        if direction != " ":
            keypress_packet = packets.Packets(direction, package_type="D")
            keypress_packet.send(sck)
        time.sleep(1/10)


def Render_cell(type : int, x : int , y : int, screen : pg.display, cell_size : int):
    #print(f"type = {type}, x = {x}, y = {y}, size =  {cell_size}")
    match type :
        case 0 : #Free space
            color = (0,0,0)
        case 1|-1 :
            color = (0,0,255)
        case 2|-2 :
            color = (255,0,0)
        case 3|-3 :
            color = (0,255,0)
        case 4|-4 :
            color = (255,255,0)
        case 5 : #Wall
            color = (0,255,255)
        case _ : 
            color = (255,255,255)
    pg.draw.rect(screen, color , pg.Rect(x,y,cell_size,cell_size))
                                         
def Render_game(screen : pg.display , matrix : list[list]) -> None :
    screen.fill((0,0,0))
    cell_size = int(1000/max(len(matrix),len(matrix[0])))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            Render_cell(matrix[i][j], i*cell_size, j*cell_size, screen, cell_size)
    pg.display.flip()


if __name__ == '__main__':
    sck = Connect('192.168.43.210', 8888)
    Lobby(sck)
