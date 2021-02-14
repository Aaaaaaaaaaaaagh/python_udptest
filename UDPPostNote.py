import socket
import sys

UDP_IP = str(sys.argv[1]) #takes in arguments from command line
UDP_PORT = int(sys.argv[2])
MESSAGE =  b"Test" #vestige of when I was testing items.

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #goto socket



while True: #infinitely loop this so as to continually read in input
        try:
                MESSAGE = bytes(input("Enter your next command: "), encoding='utf-8') #encodes the string message in utf8 to be decoded on other side
                if (len(MESSAGE) == 0):
                        print("Write something into the command line.") #didn't enter anything in?
                        break
                else :
                        sock.sendto(MESSAGE,(UDP_IP, UDP_PORT)) #send it over to the port on the server side.

        except Exception as e:
                print (e)

#sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))