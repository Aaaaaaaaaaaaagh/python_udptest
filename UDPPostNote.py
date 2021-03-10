import socket
import sys
import os

UDP_IP = str(sys.argv[1]) #takes in arguments from command line
UDP_PORT = int(sys.argv[2])
MESSAGE =  b"Test" #vestige of when I was testing items.


OWNPORT = int(sys.argv[3]) #takes in it's own port on this item. this actually lets it know where to set up, and it's used below for ms.bind.
ipv4 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0] #the own IP of this client server.

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #goto socket

ms = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #bind to socket
ms.bind((ipv4, OWNPORT))
imfirstflag = 0
passAlong = ""


while True: #infinitely loop this so as to continually read in input
        try:
                #MESSAGE = bytes(input("Enter your next command: "), encoding='utf-8') #encodes the string message in utf8 to be decoded on other side
                MESSAGE = input("Enter your next command: ")
                if (len(MESSAGE) == 0):
                        #local_ip = socket.gethostbyname(socket.gethostname())
                        #print(local_ip)
                        break
                else:
                        addition = " " + str(OWNPORT) + " " + ipv4
                        MESSAGE += addition #append the port number to the string. this can also add it's own IP, but that's going to be done later, since I am only test$                        MESSAGESTR = MESSAGE
                        MESSAGE = bytes(MESSAGE, encoding='utf-8')
                        sock.sendto(MESSAGE,(UDP_IP, UDP_PORT)) #send it over to the port on the server side.
                        data, addr = ms.recvfrom(1024) #take 1024 characters, no more no less.
                        sanData = data.decode('utf-8') #decode it into a utf-8 string.

                        #print(sanData)
                        exSanData = sanData.split("/")
                        #print(exSanData)
                        MESSAGE_split = MESSAGESTR.split(" ")
                        if MESSAGE_split[0] == "im-start": #if the command you just sent was an IM Start command, you're getting the first link back. flag up.
                                imfirstflag = 1
                                #print("IM STARTED \n")
                        if exSanData[0] == "IM-STARTED":
                                print("received word back!")
                                imEndFlag = 0
                                CurrentUser = exSanData[3].split(" ")
                                print(exSanData[3])
                                print(exSanData)
                                if CurrentUser[1] == ipv4:
                                        print("IPV4 matched!")
                                        print(CurrentUser[2])
                                        print(OWNPORT)
                                        if CurrentUser[2] == str(OWNPORT):
                                                print("own port matched!")
                                                if imfirstflag == 1:
                                                        IMMessage = input("Message to send: ")
                                                        #print(IMMessage)
                                                        IMMessage_send = bytes(IMMessage, encoding='utf-8')


                                                        first = str(CurrentUser[0]) + " " + str(CurrentUser[1]) + " " + str(CurrentUser[2]) #artifact of first user so it$                                                        #print(first)
                                                        #print(exSanData[3])
                                                        del exSanData[3]
                                                        #print(exSanData[3])
                                                        #exSanData.pop(3)
                                                        NextUser = exSanData[3].split(" ")
                                                        #print(NextUser)
                                                        sock.sendto(bytes(IMMessage, encoding='utf-8'), (NextUser[1], int(NextUser[2])))

                                                        #sanData = sanData + IMMessage + first
                                                        #print(sanData)
                                                        #print("AAAH!\n")
                                                        newSanData = ""
                                                        for x in exSanData:
                                                                newSanData += x + "/"
                                                        newSanData = newSanData[:-1]
                                                        print(newSanData)
                                                        newSanData += first
                                                        print(newSanData)
                                                        sock.sendto(bytes(newSanData, encoding='utf-8'),(NextUser[1], int(NextUser[2])))
                                                else:
                                                        print("Not the first!!\n")
                                                        del exSanData[3]
                                                        NextUser = exSanData[3].split(" ")
                                                        print(NextUser)
                                                        print(exSanData)
                                                        print(exSanData[-3])
                                                        newerSanData = ""
                                                        for x in exSanData:
                                                                newerSanData += x + "/"
                                                        newerSanData = newerSanData[:-1]
                                                        print(exSanData[3])
                                                        print(exSanData[-1])
                                                        if exSanData[3] == exSanData[-1]:
                                                                imEndFlag = 1
                                                        if imEndFlag == 0:
                                                                print("IM FLAG is 0! Not the end!!")
                                                                sock.sendto(bytes(passAlong, encoding='utf-8'), (NextUser[1], int(NextUser[2])))
                                                                sock.sendto(bytes(newerSanData, encoding='utf-8'), (NextUser[1], int(NextUser[2])))
                                                        if imEndFlag == 1:
                                                                print("IM FLAG is 1! DONE!")



                                                                sock.sendto(bytes(passAlong, encoding='utf-8'), (NextUser[1],int(NextUser[2])))


                                                                finalmsg = "im-complete" + " " + exSanData[1] + " " + NextUser[0] + " " + str(OWNPORT) + " " + ipv4
                                                                bytesFinalMSG = bytes(finalmsg,encoding='utf-8')
                                                                sock.sendto(bytesFinalMSG, (UDP_IP, UDP_PORT))
                        else:
                                print(sanData)
                                passAlong = sanData
        except Exception as e:
                print(e)

#sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))