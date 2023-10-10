import socket 
import packets

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.connect(('172.21.72.112', 8889))

print("Connected")


to_send = input("Set your nickname: ")
nickname_packet = packets.Packets(to_send,package_type='I')
nickname_packet.send(sck)
print(f"Your nickname is {to_send}")
readiness = 0
while True:
    status = input("Type 'ready' when you are: ")
    ready_packet = packets.Packets(status, package_type="I")
    ready_packet.send(sck)
    
    if status == "ready" and readiness == 0:
        print("You are now ready")
        readiness = 1
    if status == "unready" and readiness == 1:
        print("You are now unready")
        readiness = 0