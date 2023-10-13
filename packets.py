import socket

class Packets:

    """
    This class has only one attribute : the bytes chain created during the __init__ depending on the type of data you want tot send :
        'D' : is a direction represented by only a chr ('N','S','E','W,)
        'M' : is the map represented by a 2-dimension matrix
        'I' : is any kind of info text info (a str) of variable length
        'T' : is a trigger (any 1-byte int to differentiate different operations)
        'U' : is a string of length = number_of_players representing their different directions

        architechture of a packet :

        -1 byte for the type of the socket ("D","M","I","T" or "U")
        
        (if type == "D"):
        -1 byte for the direction

        (if type == "M"):
        -4 bytes for the total length of the rest of the packet
        -4 bytes for the number of cells in the map
        -4 bytes for the length of one row
        -each cell coded in a 1-byte signed int

        (if type == "I"):
        -4 bytes for the total length of the rest of the packet
        -the bytes corresponding to the encoding of the text in utf-8

        (if type == "T"):
        -1 byte for the id of the trigger

        (if type == "U"):
        -4 bytes for differents direction (always 4 even if there are only 3 player => no player = '_')
    """


    def __init__(self, info , *, package_type : str) -> None:
        self.package_type = package_type
        self.info = info

        pack = bytearray()
        pack += str(package_type).encode("utf-8")

        match (package_type):

            case "D":
                pack += str(info).encode("utf-8")
                
            case "M":  
                nb_of_cells = int(sum([len(i) for i in info]))
                lenght = nb_of_cells+8
                pack += int.to_bytes(lenght,4,'big')
                pack += int.to_bytes(nb_of_cells,4,'big')
                pack += int.to_bytes(len(info),4,'big')
                
                for i in info :
                    for j in i :
                        pack += int.to_bytes(j,1,'big',signed='True')
            
            case "I":
                pack += int.to_bytes(len(info),4,'big')
                pack += str(info).encode("utf-8")

            case "T":
                pack += int.to_bytes(info,1,"big")

            case "U":
                pack += str(info).rjust(4,'_').encode("utf-8")

        self.package = pack

    def send(self, target : socket):
        target.send(self.package)

    def receive(target : socket.socket):
        #try:
        to_decode = bytearray()
        to_decode += target.recv(1)
        type_input = to_decode[0].to_bytes(1,'big').decode("utf-8")
        match type_input:
            case "D":
                length = 1
            case "M":
                length = int.from_bytes(target.recv(4),'big')
            case "I":
                length = int.from_bytes(target.recv(4),'big')
            case "T":
                length = 1
            case "U":
                length = 4
        
        for i in range(length):
            to_decode += target.recv(1)
        return Packets.decode(to_decode)
        #except: return ("I", "disconnect")

    def decode(array : bytearray):
        match array[0].to_bytes(1,'big').decode("utf-8"):
            case "D":
                return ("D",array[1].to_bytes(1,'big').decode("utf-8"))
            
            case "M":
                nb_cells = int.from_bytes(array[1:5],'big')
                nb_rows = int.from_bytes(array[5:9],'big')
                data = array[9:]
                return ("M",[[data[i+j*nb_rows] for i in range(nb_rows)] for j in range(int(nb_cells/nb_rows))])
            
            case "I":
                sentence = array[1::]
                output = ""
                for i in sentence :
                    output += str(i.to_bytes(1,'big'), "utf-8")
                return ("I",output)
            
            case "T":
                return ("T",array[1])
            
            case "U":
                output = ""
                for i in array[1:]:
                    letter = i.to_bytes(1,'big').decode("utf-8")
                    if letter != "_":
                        output += letter
                return ("U", output)
    
    def __repr__(self) -> str:
        return f"info = {self.info} and type = {self.package_type}"    

if __name__ == "__main__":
    encode1 = Packets(package_type="I", info = "bonjour je suis fou")
    encode2 = Packets(package_type="D", info = "N")
    encode3 = Packets(package_type="T", info = 1)
    encode4 = Packets(package_type="M", info = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[3,3,3,3]])
    encode5 = Packets(package_type="U", info = "NSE")

    to_decode1 = bytearray()
    to_decode1 += encode1.package[0].to_bytes(1,'big')
    to_decode1 += encode1.package[5::]
    to_decode4 = bytearray()
    to_decode4 += encode4.package[0].to_bytes(1,'big')
    to_decode4 += encode4.package[5::]
    print(Packets.decode(to_decode1))
    print(Packets.decode(encode2.package))
    print(Packets.decode(encode3.package))
    print(Packets.decode(to_decode4))
    print(Packets.decode(encode5.package))