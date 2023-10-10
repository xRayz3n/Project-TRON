import threading

class Player:
    def __init__(self, client_socket, name, state="available"):
        self.client_socket = client_socket
        self.name = name
        self.state = state
        self.thread_out = threading.Thread(group=None, )