import player
import packets
import multiprocessing
import threading
import time
class Game:
    def __init__(self,playersList : list[player.Player], map_size : tuple[int,int] = (100,100), speed : float = 1.0 ) -> None:
 
        """
        This class has 5 attributes:
        playerList => stores the players (object of the class Player) in a list
        pos_players => an array which stores the positions of the players (player 1 is index 0, player 2 is index 1...)
        direction_players => stores the latest direction entered by players
        map => a matrix of size = map_size+2 that stores the state of the game at each tick (the +2 stores the borders of the map)
        speed => stores the speed of the game

        On the map : -a player is represented by the negative value of his number
                     -the walls made by them is represented by his number
                     -boundaries are represented by 5s
                     -free spaces are represented by 0s
        """
        self.playerList = playersList

        nb_players = len(playersList)

        pos_players = [[int(map_size[0]/2),1],[int(map_size[0]/2),map_size[1]]]
        direction_players = {}
        direction_players.update({self.playerList[0].client_addr : "S"})
        direction_players.update({self.playerList[1].client_addr : "N"})

        if (nb_players >= 3):
            pos_players.append([1,int(map_size[1]/2)])
            direction_players.update({self.playerList[2].client_addr : "E"})
        if (nb_players >= 4):
            pos_players.append([map_size[0],int(map_size[1]/2)])
            direction_players.update({self.playerList[2].client_addr : "W"})

        for Aplayer in playersList :
            threading.Thread(group = None, target = self.change_direction_player, args= [Aplayer]).start()

        self.pos_players = pos_players
        self.direction_players = direction_players
        
        self.map = [[0 if (i != 0 and i != map_size[0]+1) and (j != 0 and j!= map_size[1]+1) else 5 for i in range(map_size[0]+2)] for j in range(map_size[1]+2)] 
        
        self.speed = speed

    def change_direction_player(self, player : player.Player):
        while True :
            new_dir = packets.Packets.receive(player.client_socket)
            self.direction_players[player.client_addr] = new_dir[1]

    def Broadcast_map_to_all(self):
        for Aplayer in self.playerList :
            packets.Packets(self.map, package_type="M").send(Aplayer.client_socket)

    def update_positions(self) -> None:

        for i in range(len(self.playerList)):
            if self.playerList[i].state != "dead":
                x = self.pos_players[i][0]
                y = self.pos_players[i][1]
                match(self.direction_players[self.playerList[i].client_addr]):
                    case 'N' :
                        if(self.map[x][y -1] == 0):
                            self.map[x][y] = i+1
                            self.map[x][y-1] = -i-1
                            self.pos_players[i][1] = y-1
                        else : 
                            self.You_are_dead(self.playerList[i])
                    case 'S' :
                        if(self.map[x][y+1] == 0):
                            self.map[x][y] = i+1
                            self.map[x][y+1] = -i-1
                            self.pos_players[i][1] = y+1
                        else : 
                            self.You_are_dead(self.playerList[i])
                    case 'E' :
                        if(self.map[x+1][y] == 0):
                            self.map[x][y] = i+1
                            self.map[x+1][y] = -i-1
                            self.pos_players[i][1] = x+1
                        else : 
                            self.You_are_dead(self.playerList[i])
                    case 'W' :
                        if(self.map[x-1][y] == 0):
                            self.map[x][y] = i+1
                            self.map[x-x][y] = -i-1
                            self.pos_players[i][1] = x-1
                        else : 
                            self.You_are_dead(self.playerList[i])
        self.Broadcast_map_to_all()

                    
    def You_are_dead(self, player : player.Player):
        player.state = "dead"
        #to do : send a message to the players that he is dead (to play animation + other triggers)

    def Start_Updating(self):
        while True:
            self.update_positions()
            time.sleep(1/self.speed)