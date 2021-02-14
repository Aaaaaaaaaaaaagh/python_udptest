import socket

UDP_IP = "10.120.70.145" #ip of the server that holds the main python UDP server.
UDP_PORT = 39502 #port number I chose that was within range. 77/2 rounded up is 39, * 1000 + (//500//1000) == 39500-39999. 

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #bind to socket
sock.bind((UDP_IP, UDP_PORT))

ContactLists = [] #empty lists and flags for responses below. ContactLists stores all the lists you enter.
ContactNameRegistry = [] #This stores each person's data, and is appended to from the register commands.
flag = 0 #set to 0 at the start of operations that could flag up if something bad is found, aborting the operation.
tempflag1 = 0
tempflag2 = 0
duplicateflag = 0 #a specific flag I used to see if entries already existed.
count = 0 #count value that is necessary for outputting to a file.
NamesInList = [] #So, the list repo and person repo are separate lists, right? This is where you assign people to a specific list.

while True:
        data, addr = sock.recvfrom(1024) #take 1024 characters, no more no less.

        sanData = data.decode('utf-8') #decode the byte object that was passed through
        FormattedData = sanData.split(" ") #and split up the words into an array of strings.
        if FormattedData[0] == "register":
                        flag = 0
                        for x in ContactNameRegistry:
                                if x[0] == FormattedData[1]:
                                        flag = 1 #there's already someone with this name registered. flag goes up.
                                        #print("FAILURE")
                        if flag == 0: #otherwise, add them in in a tuple of 3.
                                ContactNameRegistry.append([FormattedData[1],FormattedData[2],FormattedData[3]])
                                print("SUCCESS")
                                #print(ContactNameRegistry)
                        else: #flag went up, so post failure.
                                print("FAILURE")
        if FormattedData[0] == "create":
                        flag = 0
                        for x in ContactLists:
                                if x == FormattedData[1]:
                                        flag = 1 #flag goes up if a duplicate is detected.
                        if flag == 0:
                                ContactLists.append(FormattedData[1]) #add that list to the list of contactlists.
                                print("SUCCESS")
                        else:
                                print("FAILURE")
        if FormattedData[0] == "query-lists":
                        print(ContactLists) #print every list. If there's no list, an empty array is printed.
        if FormattedData[0] == "join":
                        flag = 0
                        duplicateflag = 0
                        tempflag1 = 0
                        tempflag2 = 0
                        for x in ContactNameRegistry: #for every name in the registry
                                #print (x)
                                #print (x[0], x[1], x[2])
                                if x[0] == FormattedData[2]: #if we match a name, and know they exist.
                                        #print("Name matched!")
                                        tempflag1 = 1
                                        for x in ContactLists:
                                                if x == FormattedData[1]: #if we match a contactlist as well.
                                                        #print("ContactList Matched!")
                                                        tempflag2 = 1
                                                        for x in NamesInList:
                                                                if x[0] == FormattedData[1]:
                                                                        if x[1] == FormattedData[2]: #if a tuple exists already, put a flag up.
                                                                                #print("duplicate goin up!")
                                                                                duplicateflag = 1
                        if duplicateflag == 0 and tempflag1 == 1 and tempflag2 == 1: #if we did find matches, but no exact duplicates, add that person into the list.
                                        NamesInList.append([FormattedData[1], FormattedData[2]])
                                        print("SUCCESS")
                                        #print(NamesInList)
                        else:
                                        print("FAILURE")
        if FormattedData[0] == "save": 
                f = open('%s.txt' % FormattedData[1], 'w') #make a text file with the name we want.
                f.write("Number of active users: %d\n" % (len(ContactNameRegistry))) #write how many users there are.
                for x in ContactNameRegistry: #and for each of them, put their info.
                        f.write("Contact-Name: %s " % x[0])
                        f.write("IP Address: %s " % x[1])
                        f.write("Port Number: %s \n" % x[2])
                f.write("Number of contact lists: %d\n" % (len(ContactLists))) #and also the list of contacts's length
                for x in ContactLists:
                        count = 0
                        for y in NamesInList:
                                if y[0] == x:
                                        count += 1
                        f.write("contact-list %s has %d members." % (x, count)) #and how many members they have, through a loop that increments count for each particular list.
                for x in ContactLists:
                        for y in NamesInList:
                                if y[0] == x:
                                        for z in ContactNameRegistry:
                                                if y[1] == z[0]:
                                                        f.write("list %s contains member: %s, %s, %s\n" % (x, z[0], z[1], z[2])) #sameish loop as above, but prints matching values in CNR.

#               for x in ContactLists:
#                       for y in NamesInList:
#                               count = 0
#                               if NamesInList[0] == x:
#                                       for z in ContactNameRegistry:
#                                               if z[0] == NamesInList[1]:
#                                                       print(z)
                                #f.write("list %s has %d members\n" % (x, count))
        if FormattedData[0] == "exit":
                flag = 0
                for x in ContactNameRegistry:
                        if x[0] == FormattedData[1]:
                                flag = 1
                                ContactNameRegistry.remove(x)
                for x in NamesInList:
                        if x[1] == FormattedData[1]:
                                flag = 1
                                NamesInList.remove(x)
                if flag == 1:
                        print("SUCCESS") #deleted at least 1 entry.
                else:
                        print("FAILURE") #they didn't come up at all.

#       print("%s" % str(len(data)))
#       print("%s" % sanData)
#       print("%s" % str(addr)) #used for making sure values were being passed through correctly.