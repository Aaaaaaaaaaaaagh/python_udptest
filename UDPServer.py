
import socket

UDP_IP = "10.120.70.145"
UDP_PORT = 39502

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

ContactLists = []
ContactNameRegistry = []
flag = 0
count = 0
NamesInList = []

while True:
        data, addr = sock.recvfrom(1024)


        sanData = data.decode('utf-8')
        FormattedData = sanData.split(" ")
        if FormattedData[0] == "register":
                        flag = 0
                        for x in ContactNameRegistry:
                                print (x[0])
                                if x[0] == FormattedData[1]:
                                        flag = 1
                                        #print("FAILURE")
                        if flag == 0:
                                ContactNameRegistry.append([FormattedData[1],FormattedData[2],FormattedData[3]])
                                print("SUCCESS")
                        else:
                                print("FAILURE -- flag went up during testing")
        if FormattedData[0] == "create":
                        flag = 0
                        for x in ContactLists:
                                if x == FormattedData[1]:
                                        flag = 1
                        if flag == 0:
                                ContactLists.append(FormattedData[1])
                                print("SUCCESS")
                        else:
                                print("FAILURE -- name already exists")
        if FormattedData[0] == "query-lists":
                        print(ContactLists)
        if FormattedData[0] == "join":
                        for x in ContactNameRegistry:
                                print (x)
                                print (x[0], x[1], x[2])
                                if x[0] == FormattedData[2]:
                                        for x in ContactLists:
                                                if x == FormattedData[1]:
                                                        NamesInList.append([FormattedData[1], FormattedData[2]])
                                                        print("SUCCESS")
                                                else:
                                                        print("FAILURE -- couldn't match your contact list name to anything in the contact lists.")
                                else:
                                        print("FAILURE -- there's no names like this in the contact name registry")
        if FormattedData[0] == "save":
                f = open('%s.txt' % FormattedData[1], 'w')
                f.write("Number of active users: %d\n" % (len(ContactNameRegistry)))
                for x in ContactNameRegistry:
                        f.write("Contact-Name: %s " % x[0])
                        f.write("IP Address: %s " % x[1])
                        f.write("Port Number: %s \n" % x[2])
                f.write("Number of contact lists: %d\n" % (len(ContactLists)))
                for x in ContactLists:
                        count = 0
                        for y in NamesInList:
                                if NamesInList[0] == x:
                                        for z in ContactNameRegistry:
                                                if z[1] == NamesInList[1]:
                                                        print(z)
                                        count += 1
                                f.write("list %s has %d members\n" % (x, count))
        if FormattedData[0] == "exit":

                for x in ContactNameRegistry:
                        if x[1] == FormattedData[1]:
                                ContactNameRegistry.remove(x)
                for x in NamesInList:
                        if x[1] == FormattedData[1]:
                                NamesInList.remove(x)

                print("%s has been taken out of the registry and each list that included it." % FormattedData[1])


#       print("%s" % str(len(data)))
#       print("%s" % sanData)
#       print("%s" % str(addr))