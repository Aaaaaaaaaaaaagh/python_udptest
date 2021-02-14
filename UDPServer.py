import socket

UDP_IP = "10.120.70.145"
UDP_PORT = 39502

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
        data, addr = sock.recvfrom(1024)






        print("%s" % data)
        print("%s" % str(addr))

