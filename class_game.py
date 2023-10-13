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

        pos_players = [ [int(map_size[0]/2),1], [int(map_size[0]/2),map_size[1]] ]
        direction_players = {}
        sended = {}
        direction_players.update({self.playerList[0].client_addr : "S"})
        sended.update({self.playerList[0].client_addr : False})
        direction_players.update({self.playerList[1].client_addr : "N"})
        sended.update({self.playerList[1].client_addr : False})

        if (nb_players >= 3):
            pos_players.append([1,int(map_size[1]/2)])
            direction_players.update({self.playerList[2].client_addr : "E"})
            sended.update({self.playerList[2].client_addr : False})
        if (nb_players >= 4):
            pos_players.append([map_size[0],int(map_size[1]/2)])
            direction_players.update({self.playerList[3].client_addr : "W"})
            sended.update({self.playerList[3].client_addr : False})
        
        self.pos_players = pos_players
        self.direction_players = direction_players
        self.sended = sended        

        map = [[0 if (i != 0 and i != map_size[0]+1) and (j != 0 and j!= map_size[1]+1) else 5 for i in range(map_size[0]+2)] for j in range(map_size[1]+2)] 
        for i in range(len(pos_players)) :
            map[pos_players[i][0]][pos_players[i][1]] = -i-1

        self.map = map
        self.speed = speed

        for Aplayer in playersList :
            Aplayer.state = "alive"
            threading.Thread(group=None, target=self.change_direction_player, args=[Aplayer]).start()
            threading.Thread(group=None, target=self.update_positions, args=[Aplayer]).start()

    def change_direction_player(self, player : player.Player): #MULTITHREAD A
        while player.state == "alive" :
            type, new_dir = packets.Packets.receive(player.client_socket)

            match new_dir:
                case "N":
                    if self.direction_players[player.client_addr] != "S":
                        self.direction_players[player.client_addr] = new_dir
                case "S":
                    if self.direction_players[player.client_addr] != "N":
                        self.direction_players[player.client_addr] = new_dir
                case "W":
                    if self.direction_players[player.client_addr] != "E":
                        self.direction_players[player.client_addr] = new_dir
                case "E":
                    if self.direction_players[player.client_addr] != "W":
                        self.direction_players[player.client_addr] = new_dir
            
            time.sleep(1/30)

    def Broadcast_map_to_player(self, player : player.Player): 
            to_send = packets.Packets(self.map, package_type="M")
            to_send.send(player.client_socket)

    def Broadcast_directions_to_player(self, player : player.Player): #MULTITHREAD B
        
        if not(self.sended[player.client_addr]):
            outputDirection = ""
            for aPlayer in self.playerList:
                outputDirection += self.direction_players[aPlayer.client_addr]

            to_send = packets.Packets(outputDirection, package_type="U")
            to_send.send(player.client_socket)
            #counter.custom += 1
                


    def update_positions(self, player : player.Player) -> None: #MULTITHREAD B
        counter = threading.local()
        counter.custom = 0
        self.Broadcast_map_to_player(player)
        while True:
            i = self.playerList.index(player)
            if player.state != "dead":
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
                            self.pos_players[i][0] = x+1
                        else : 
                            self.You_are_dead(self.playerList[i])
                    case 'W' :
                        if(self.map[x-1][y] == 0):
                            self.map[x][y] = i+1
                            self.map[x-1][y] = -i-1
                            self.pos_players[i][0] = x-1
                        else : 
                            self.You_are_dead(self.playerList[i])
            self.sended[i] = False
            self.Broadcast_directions_to_player(player)
            if counter.custom > 20:
                self.Broadcast_map_to_player(player)
                counter.custom = 0
                print(f"map sent to {player.name}")
            counter.custom += 1

            time.sleep(1/self.speed)
                    
    def You_are_dead(self, player : player.Player):
        player.state = "dead"
        print(f"{player.name} is dead!")
        #to do : send a message to the players that he is dead (to play animation + other triggers)

    def Start_Updating(self):
        while True:
            time.sleep(1/self.speed)