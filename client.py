import socket 
import packets
import threading
import multiprocessing
import os

def Connect(ip_addr : str, port : int) -> socket.socket:
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((ip_addr, port))
    print("Connected")
    return sck

def IsDisconnected(sck, status) -> bool:
    if status == "disconnect":
            print(f"Connection lost from server")
            sck.close()
            return True
    return False
def Lobby(sck):
    to_send = input("Set your nickname: ")
    nickname_packet = packets.Packets(to_send,package_type='I')
    nickname_packet.send(sck)
    print(f"Your nickname is {to_send}")
    threading.Thread(group=None, target=ReceiveMsg, args=[sck]).start()
    while True:
        status = input("\nType 'ready' when you are: ")
        ready_packet = packets.Packets(status, package_type="I")
        ready_packet.send(sck)
        
        if status == "ready":
            print("You are now ready")
        if status == "unready":
            print("You are now unready")

def ReceiveMsg(sck):
     while True:
        message = packets.Packets.receive(sck)[1]
        #os.system('clear')
        if IsDisconnected(sck, message):
            break

        print(message)
    
if __name__ == '__main__':
    sck = Connect('172.21.72.112', 8888)
    Lobby(sck)