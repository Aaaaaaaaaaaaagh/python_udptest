import socket
import sys

UDP_IP = str(sys.argv[1]) #takes in arguments from command line
UDP_PORT = int(sys.argv[2])
MESSAGE =  b"Test" #vestige of when I was testing items.


OWNPORT = int(sys.argv[3])


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #goto socket

ms = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #bind to socket
ms.bind(("10.120.70.106", OWNPORT))



while True: #infinitely loop this so as to continually read in input
        try:
                #MESSAGE = bytes(input("Enter your next command: "), encoding='utf-8') #encodes the string message in utf8 to be decoded on other side
                MESSAGE = input("Enter your next command: ")
                if (len(MESSAGE) == 0):
                        #local_ip = socket.gethostbyname(socket.gethostname())
                        #print(local_ip)
                        print("Write something into the command line.") #didn't enter anything in?
                        break
                else:
                        addition = " " + str(OWNPORT)
                        MESSAGE += addition
                        MESSAGE = bytes(MESSAGE, encoding='utf-8')
                        sock.sendto(MESSAGE,(UDP_IP, UDP_PORT)) #send it over to the port on the server side.
                        data, addr = ms.recvfrom(1024) #take 1024 characters, no more no less.
                        sanData = data.decode('utf-8')
                        print(sanData)
        except Exception as e:
                print (e)

#sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))