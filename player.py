import threading
class Player:
    def __init__(self, client_socket, client_addr, name, state="available"):
        self.client_addr = client_addr
        self.client_socket = client_socket
        self.name = name
        self.state = state
        
