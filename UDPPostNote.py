import socket

UDP_IP = "10.120.70.145"
UDP_PORT = 39502
MESSAGE =  b"Test"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
        try:
                MESSAGE = bytes(input("Enter your next command: "), encoding='utf-8')
                if (len(MESSAGE) == 0):
                        print("Write something into the command line.")
                        break
                else :
                        sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))

        except Exception as e:
                print (e)

#sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))#sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))
