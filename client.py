import socket 
import packets

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(('172.21.72.112', 8887))

print("Connected")

while True : 
    to_send = input("Set your nickname: ")
    nickname_packet = packets.Packets(to_send,package_type='I')
    sck.send()
    print("ok sent well !")
