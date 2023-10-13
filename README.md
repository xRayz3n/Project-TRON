# ProjectTRON : 
## *A remake of the game TRON "Light Racer" by Sébastien LAM and Théo LISSARAGUE*

### Installation :

- First be sure to use python3 and to have pygame installed
- If you want to host a game, download all the files
- If you only want to play by joining an existing server, you can just download the files "client.py", "gameclient.py" and "packets.py"

### Execution : 

- ***To create a server :*** execute the "server.py" file using :
    
```bash
python3 server.py
```
    
You have to know your IP addres to give it to the players, (you can use "ip a" command in a console),
the game will ask you to choose a port, be sure to enter an available port and to remember it to give it to the players.
    
- ***To join a game :*** execute the "client.py" file using :

```bash
python3 client.py
```

Ask to the server host for the IP and the port of the server then type them in the game console, then chose a nickname and type ready when you are.

### The game :

*In the lobby :*

- The game will start when they are at least 2 players (and at most 4) and when all players said they where ready

- A 3.2.1 counter will appear and the game will open and start in another window.

*During the game :*

- Each tick, all player will move to an adjacent cell depending of their direction
- You can change the direction you will move on the next tick using the arrow keys
- You play the racer which is filled with white (the opponents are the ones filled with black)
- When you move, you leave a wall behind you
- The purpuse of the game is to be the last player alive, knowing that you can die by crashing into the border of the screens, the other players or the walls they create (yours included !)