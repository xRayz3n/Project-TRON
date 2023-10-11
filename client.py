import socket 
import packets
import threading
import multiprocessing
import os
import pygame as pg
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
        
        match status:
            case "ready":
                print("You are now ready")
            case "unready":
                print("You are now unready")
def ReceiveMsg(sck):
     while True:
        message = packets.Packets.receive(sck)[1]
        #os.system('clear')
        if IsDisconnected(sck, message):
            break
        
        print(message)
    


def render_cell(type : int, x : int , y : int, screen : pg.display, cell_size : int, neighboor : str = ""):
    print(f"type = {type}, x = {x}, y = {y}, size =  {cell_size}")
    match type :
        case 1 :
            color = (0,0,255)
        case 2 :
            color = (255,0,0)
        case 3 :
            color = (0,255,0)
        case 4 :
            color = (0,255,255)
    match type :
        case 5 : 
            pg.draw.rect(screen, (0,255,255) , pg.Rect(x,y,cell_size,cell_size))
        case 0 : 
            pg.draw.rect(screen, (0,0,0) , pg.Rect(x,y,cell_size,cell_size))
        case _ : 
            if type > 0:
                for i in neighboor:
                    match i:
                        case "N":
                            pg.draw.line(screen, color, start_pos= (x+int(cell_size/2), y+int(cell_size/2)),end_pos= (x+int(cell_size/2), y), width=int(cell_size/3))
                        case "S":
                            pg.draw.line(screen, color, start_pos= (x+int(cell_size/2), y+int(cell_size/2)),end_pos= (x+int(cell_size/2), y+cell_size), width=int(cell_size/3))           
                        case "E":
                            pg.draw.line(screen, color, start_pos= (x+int(cell_size/2), y+int(cell_size/2)),end_pos= (x+cell_size, y+int(cell_size/2)), width=int(cell_size/3))
                        case "W":
                            pg.draw.line(screen, color, start_pos= (x+int(cell_size/2), y+int(cell_size/2)),end_pos= (x, y+int(cell_size/2)), width=int(cell_size/3))
                                         
def render_game(screen : pg.display , matrix : list[list]) -> None :
    screen.fill((0,0,0))
    cell_size = int(1000/max(len(matrix),len(matrix[0])))
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            me = matrix[i][j]
            neighboor = ""
            if me != 5 and me != 0:
                if(me == matrix[i][j-1] or me == -matrix[i][j-1]) : neighboor += 'N'
                if(me == matrix[i][j+1] or me == -matrix[i][j+1]) : neighboor += 'S'
                if(me == matrix[i+1][j] or me == -matrix[i+1][j]) : neighboor += 'E'
                if(me == matrix[i-1][j] or me == -matrix[i-1][j]) : neighboor += 'W'
            render_cell(matrix[i][j], i*cell_size, j*cell_size, screen, cell_size, neighboor)
    pg.display.flip()

if __name__ == '__main__':
    sck = Connect('172.21.72.112', 8889)
    Lobby(sck)


"""if __name__ == "__main__":

    import time
    pg.init()
    screen = pg.display.set_mode([1000, 1000])
    matrix = [[5 if i == 0 or i == 99 or j == 0 or j == 99 else 0 for i in range(100)] for j in range(100)]
    x,y = int(len(matrix)/2), int(len(matrix)-2)
    matrix[x][y] = -1
    render_game(screen,matrix)
    direction = "N"
    past = time.time()
    running = True  
    while running:
        print(past)
        if  time.time() - past > 0.01:
            past = time.time()
            matrix[x][y] = 1
            match direction :
                case "N":
                    y = y-1
                case "S":
                    y = y+1
                case "E":
                    x = x+1
                case "W":
                    x = x-1
            matrix[x][y] = -1
            render_game(screen,matrix)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    direction = "W"
                if event.key == pg.K_RIGHT:
                    direction = "E"
                if event.key == pg.K_UP:
                    direction = "N"
                if event.key == pg.K_DOWN:
                    direction = "S"
"""