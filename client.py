import socket 

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(('172.21.72.112', 8887))

print("Connected")

while True : 
    to_send = input("Set your nickname: ")
    to_send.rjust(16," ")
    sck.send(to_send.encode())
    print("ok sent well !")
