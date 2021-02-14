import socket

UDP_IP = "10.120.70.145"
UDP_PORT = 39502

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

ContactLists = []
ContactNameRegistry = []

while True:
        data, addr = sock.recvfrom(1024)


        sanData = data.decode('utf-8')
        FormattedData = sanData.split(" ")
        if FormattedData[0] == "register":
                        ContactNameRegistry.append([FormattedData[1],FormattedData[2],FormattedData[3]])
                        print(ContactNameRegistry)
        if FormattedData[0] == "create":
                        ContactLists.append(FormattedData[1])
        if FormattedData[0] == "query-lists":
                        print(ContactLists)
        if FormattedData[0] == "join":
                        for x in ContactNameRegistry:
                                if x[0] == FormattedData[2]:
                                        tempName = FormattedData[2]
                                        for x in ContactLists:
                                                print(x)
                                                if x == FormattedData[1]:
                                                        ContactLists[x].append(FormattedData[2])
                                                        print(ContactLists)
                                                else:
                                                        print("FAILURE -- couldn't match your contact list name to anything in the contact lists.")
                                else:
                                        print("FAILURE -- there's no names like this in the contact name registry")
        if FormattedData[0] == "save":
                print("saved")
        if FormattedData[0] == "exit":
                print("exited")


#       print("%s" % str(len(data)))
#       print("%s" % sanData)
#       print("%s" % str(addr))
