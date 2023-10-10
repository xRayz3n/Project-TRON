import player
class Game:
    def __init__(self,playersList : player.Player, map_size : tuple[int,int] = (100,100), speed : float = 1.0 ) -> None:
 
        """
        This class has 5 attributes:

        nb_players => just an int to remember how many players are (between 2 and 4)
        pos_players => an array which stores the positions of the players (player 1 is index 0, player 2 is index 1...)
        state_players => an array which stores if players are eather dead or alive (player 1 is index 0, player 2 is index 1...)
        map => a matrix of size = map_size+2 that stores the state of the game at each tick (the +2 stores the borders of the map)
        speed => stores the speed of the game

        On the map : -a player is represented by the negative value of his number
                     -the walls made by them is represented by his number
                     -boundaries are represented by 5s
                     -free spaces are represented by 0s
        """
        self.playerList = playersList
        nb_players = len(playersList)
       
        pos_players = [[1,1],[map_size,map_size]]
        state_players = ["alive","alive"]

        if (nb_players >= 3):
            pos_players.append([map_size,1])
            state_players.append("alive")

        if (nb_players >= 4):
            pos_players.append([1,map_size])
            state_players.append("alive")

        self.pos_players = pos_players
        self.state_players = state_players
        
        self.map = [[0 if (i != 0 and i != map_size[0]+1) and (j != 0 and j!= map_size[1]+1) else 5 for i in range(map_size[0]+2)] for j in range(map_size[1]+2)] 
        
        self.speed = speed
        
    def update_positions(self, input : dict) -> None:

        for i in input.keys():
            
            if self.state_players[i] != "dead":
                x = self.pos_players[i][0]
                y = self.pos_players[i][1]
                match(input[i]):
                    case 'N' :
                        if(self.map[x][y -1] == 0):
                            self.map[x][y] = i
                            self.map[x][y-1] = -i
                        else : 
                            self.You_are_dead(i)
                    case 'S' :
                        if(self.map[x][y +1] == 0):
                            self.map[x][y] = i
                            self.map[x][y+1] = -i
                        else : 
                            self.You_are_dead(i)
                    case 'E' :
                        if(self.map[x+1][y] == 0):
                            self.map[x][y] = i
                            self.map[x][y-1] = -i
                        else : 
                            self.You_are_dead(i)
                    case 'W' :
                        if(self.map[x-1][y] == 0):
                            self.map[x][y] = i
                            self.map[x][y-1] = -i
                        else : 
                            self.You_are_dead(i)
                    
    def You_are_dead(self, player : int):
        self.state_players[player-1] = "dead"
        #to do : send a message to the players that he is dead (to play animation + other triggers)

