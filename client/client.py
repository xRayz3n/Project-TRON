import socket 

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(('127.0.0.1', 8888))

print("Connected")

while True : 
    to_send = input("What do you want to send : ? \0")

    if(to_send == ""):
        break

    sck.send(to_send.encode())
    print("ok sended well !")

print("Done")