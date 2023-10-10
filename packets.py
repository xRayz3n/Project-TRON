import socket

class Packets:

    """
    This class has only one attribute : the bytes chain created during the __init__ depending on the type of data you want tot send :
        'D' : is a direction represented by only a chr ('N','S','E','W,)
        'M' : is the map represented by a 2-dimension matrix
        'I' : is any kind of info text info (a str) of variable length
        'T' : is a trigger (any 1-byte int to differentiate different operations)

        architechture of a socket :

        -4 bytes for the total length of the rest of the socket
        -1 byte for the type of the socket ("D","M","I","T"...)
        
        (if type == "D"):
        -1 byte for the direction

        (if type == "M"):
        -4 bytes for the number of cells in the map
        -4 bytes for the length of one row
        -each cell coded in a 1-byte signed int

        (if type == "I"):
        -the bytes corresponding to the encoding of the text in utf-8

        (if type == "T"):
        -1 byte for the id of the trigger
    """


    def __init__(self, info , *, package_type : str) -> None:
        self.package_type = package_type
        self.info = info

        pack = bytearray()

        match (package_type):

            case "D":
                pack += int.to_bytes(2,4,'big')
                pack += str(package_type).encode("utf-8")
                pack += str(info).encode("utf-8")
                
            case "M":  
                nb_of_cells = sum([len(i) for i in info])
                pack += int.to_bytes(nb_of_cells+9,4,'big')
                pack += str(package_type).encode("utf-8")
                pack += int.to_bytes(nb_of_cells,4,'big')
                pack += int.to_bytes(len(info),4,'big')
                
                for i in info :
                    for j in i :
                        pack += int.to_bytes(j,1,'big',signed='True')
            
            case "I":
                pack += int.to_bytes(len(info)+1,4,'big')
                pack += str(package_type).encode("utf-8")
                pack += str(info).encode("utf-8")

            case "T":
                pack += int.to_bytes(2,4,'big')
                pack += str(package_type).encode("utf-8")
                pack += int.to_bytes(info,1,"big")

        self.package = pack

    def send(self, target : socket):
        target.send(self.package)

    def receive(target : socket.socket):
        length = int.from_bytes(target.recv(4),'big')
        return Packets.decode(target.recv(length))

    def decode(array : bytearray):
        match array[0].to_bytes(1,'big').decode("utf-8"):
            case "D":
                return ("D",array[1].to_bytes(1,'big').decode("utf-8"))
            
            case "M":
                output = []
                nb_cells = int.from_bytes(array[1:5],'big')
                nb_rows = int.from_bytes(array[5:9],'big')
                data = array[9:]
                return ("M",[[data[i+j] for i in range(nb_rows)] for j in range(int(nb_cells/nb_rows))])
            
            case "I":
                sentence = array[1::]
                output = ""
                for i in sentence :
                    output += str(i.to_bytes(1,'big'), "utf-8")
                return ("I",output)
            
            case "T":
                return ("T",array[1])
            
if __name__ == "__main__":
    encode1 = Packets(package_type="I", info = "bonjour je suis fou")
    encode2 = Packets(package_type="D", info = "N")
    encode3 = Packets(package_type="T", info = 1)
    encode4 = Packets(package_type="M", info = [[i+j for i in range(5)] for j in range(5)])

    print(Packets.decode(encode1.package[4::]))
    print(Packets.decode(encode2.package[4::]))
    print(Packets.decode(encode3.package[4::]))
    print(Packets.decode(encode4.package[4::]))