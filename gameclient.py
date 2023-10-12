import pygame as pg


class GameClient:
    def __init__(self, map):
        self.map = map
        self.pos_players = [[],[],[],[]]

        for i in range(len(map)): #get the position of the players from initial map
            for j in range(len(map[i])):
                match map[i][j]:
                    case 255:
                        self.pos_players[0] = [i,j] 
                    case 254:
                        self.pos_players[1] = [i,j]
                    case 253:
                        self.pos_players[2] = [i,j]
                    case 252:
                        self.pos_players[3] = [i,j]
        for i in range(3):
            if self.pos_players[3-i] == []:
                del self.pos_players[3-i]
    
    def Update_Positions(self, direction_players) -> None:
        for i in range(len(self.pos_players)):
            x = self.pos_players[i][0]
            y = self.pos_players[i][1]
            match(direction_players[i]):
                case 'N' :
                    if(self.map[x][y -1] == 0):
                        self.map[x][y] = i+1
                        self.map[x][y-1] = -i-1
                        self.pos_players[i][1] = y-1
                case 'S' :
                    if(self.map[x][y+1] == 0):
                        self.map[x][y] = i+1
                        self.map[x][y+1] = -i-1
                        self.pos_players[i][1] = y+1
                case 'E' :
                    if(self.map[x+1][y] == 0):
                        self.map[x][y] = i+1
                        self.map[x+1][y] = -i-1
                        self.pos_players[i][0] = x+1
                case 'W' :
                    if(self.map[x-1][y] == 0):
                        self.map[x][y] = i+1
                        self.map[x-1][y] = -i-1
                        self.pos_players[i][0] = x-1
        
        print(self.map)