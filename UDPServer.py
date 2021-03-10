import socket
import sys

UDP_IP = "10.120.70.145" #ip of the server that holds the main python UDP server.
UDP_PORT = int(sys.argv[1]) #39502 #port number I chose that was within range. 77/2 rounded up is 39, * 1000 + (//500//1000) == 39500-39999.



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
IMFlagList = "" #set empty at first in case it's checked and needs to be compared to.

while True:
        data, addr = sock.recvfrom(1024) #take 1024 characters, no more no less.


        sanData = data.decode('utf-8') #decode the byte object that was passed through
        FormattedData = sanData.split(" ") #and split up the words into an array of strings.
        if FormattedData[0] == "debug":
                        print(NamesInList)
        if FormattedData[0] == "register":
                        flag = 0
                        for x in ContactNameRegistry:
                                if x[0] == FormattedData[1]:
                                        flag = 1 #there's already someone with this name registered. flag goes up.
                                        #print("FAILURE")
                        if flag == 0: #otherwise, add them in in a tuple of 3.
                                ContactNameRegistry.append([FormattedData[1],FormattedData[2],FormattedData[3]])
                                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[5], int(FormattedData[4])))
                                #print("SUCCESS")
                                #print(ContactNameRegistry)
                        else: #flag went up, so post failure.
                                #print("FAILURE")
                                sock.sendto(bytes("FAILURE", encoding='utf-8'),(FormattedData[5], int(FormattedData[4])))
        if FormattedData[0] == "create":
                        flag = 0
                        for x in ContactLists:
                                if x == FormattedData[1]:
                                        flag = 1 #flag goes up if a duplicate is detected.
                        if flag == 0:
                                ContactLists.append(FormattedData[1]) #add that list to the list of contactlists.
                                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[3], int(FormattedData[2]))) #send it over to the port on the server side.
                                #print("SUCCESS")
                        else:
                                #print("FAILURE")
                                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[3], int(FormattedData[2])))
        if FormattedData[0] == "query-lists":
                        print(ContactLists) #print every list. If there's no list, an empty array is printed.
                        sock.sendto(bytes(str(ContactLists), encoding = 'utf-8'),("10.120.70.106", int(FormattedData[1])))
        if FormattedData[0] == "join":
                        flag = 0
                        duplicateflag = 0
                        tempflag1 = 0
                        tempflag2 = 0
                        otherrflag = 0

                        nonolist = []
                        for x in NamesInList:
                                if x[0] == IMFlagList:
                                        nonolist.append(x[1])
                        print(nonolist)
                        for y in nonolist:
                                if y == FormattedData[2]:
                                        otherrflag = 1
                        if otherrflag == 0:
                                for x in ContactNameRegistry: #for every name in the registry
                                        print (x)
                                        print (x[0], x[1], x[2])
                                        if x[0] == FormattedData[2]: #if we match a name, and know they exist.
                                                print("Name matched!")
                                                tempflag1 = 1
                                                for x in ContactLists:
                                                        if x == FormattedData[1]: #if we match a contactlist as well.
                                                                print("ContactList Matched!")
                                                                tempflag2 = 1
                                                                for x in NamesInList:
                                                                        if x[0] == FormattedData[1]:
                                                                                if x[1] == FormattedData[2]: #if a tuple exists already, put a flag up.
                                                                                        print("duplicate goin up!")
                                                                                        duplicateflag = 1
                        if duplicateflag == 0 and tempflag1 == 1 and tempflag2 == 1: #if we did find matches, but no exact duplicates, add that person into the list.
                                        NamesInList.append([FormattedData[1], FormattedData[2]])
                                        sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                                        print("SUCCESS")
                                        print(NamesInList)
                        else:
                                        sock.sendto(bytes("FAILURE", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                                        print("FAILURE")
        if FormattedData[0] == "leave":
                linecToAdd = []
                linecToAdd.append(FormattedData[1])
                linecToAdd.append(FormattedData[2]) #what to remove if not in an IM
                forget_flag = 0
                nonolist = []
                for x in NamesInList:
                        print(x[0])
                        print(x[1])
                        if x[0] == IMFlagList:
                                nonolist.append(x[1]) #here, we go through every single name in a list, and if it's in a list that's in an interaction, add it to a subli$                for y in nonolist:
                        if y == FormattedData[2]:
                                forget_flag = 1
                print(nonolist)
                print(FormattedData[2])
                print(forget_flag)
                print(IMFlagList) #These all just give some info for what's going on in the demonstration. Below is an old implementation that didn't work out for me.
#                for x in ContactNameRegistry: #for every name in the registry
#                        if x[0] == FormattedData[2]: #if we match a name, and know they exist.
#                                for y in ContactLists:
#                                        if y == FormattedData[1]:
#                                                for z in NamesInList:
#                                                        if (linecToAdd in NamesInList):
#                                                                if lineCToAdd[1] == IMFlagName:
#                                                                        NamesInList.remove(linecToAdd)
#                                                                        sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
#                                                                        print("SUCCESS")
#                                                                        forget_flag = 1
                if forget_flag == 1: #if it failed, do the fail message and pass it back.
                        sock.sendto(bytes("FAILURE", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                        print("FAILURE")
                else:
                        NamesInList.remove(linecToAdd) #otherwise, you succeeded.
                        sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                        print("SUCCESS")
        if FormattedData[0] == "save":
                f = open('%s.txt' % FormattedData[1], 'w') #make a text file with the name we want.
                f.write("Number of active users: %d\n" % (len(ContactNameRegistry))) #write how many users there are.
                for x in ContactNameRegistry: #and for each of them, put their info.
                        f.write("Contact-Name: %s " % x[0])
                        print("Contact-Name: %s "  % x[0])
                        f.write("IP Address: %s " % x[1])
                        print("IP Address: %s " % x[1])
                        f.write("Port Number: %s \n" % x[2])
                        print("Port Number: %s \n" % x[2])
                f.write("Number of contact lists: %d\n" % (len(ContactLists))) #and also the list of contacts's length
                for x in ContactLists:
                        count = 0
                        for y in NamesInList:
                                if y[0] == x:
                                        count += 1
                        f.write("contact-list %s has %d members.\n" % (x, count)) #and how many members they have, through a loop that increments count for each particul$                        print("contact-list %s has %d members.\n" % (x, count)) #and how many members they have, through a loop that increments count for each particular$                for x in ContactLists:
                        for y in NamesInList:
                                if y[0] == x:
                                        for z in ContactNameRegistry:
                                                if y[1] == z[0]:
                                                        f.write("list %s contains member: %s, %s, %s\n" % (x, z[0], z[1], z[2])) #sameish loop as above, but prints match$                                                        print("list %s contains member: %s, %s, %s\n" % (x, z[0], z[1], z[2])) #sameish loop as above, but prints matchin$                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[3], int(FormattedData[2])))
                f.close()
        if FormattedData[0] == "load":
                bigpointer = 1
                littlepointer = 0
                otherpointer = 0 #So many pointers. They're all needed for reading the nume number, part in line sequence, etc.
                g = open('%s.txt' % FormattedData[1], "r") #open a text file to be read
                DataToParse = g.readlines() #read the lines

                Line1 = DataToParse[0].split(" ") #split each word on spaces
                ActiveUserIteration = int(Line1[4]) #how many lines to parse through next

                for x in range(1, ActiveUserIteration+1):

                        ParseHERE = DataToParse[x].split(" ")
                        input1 = ParseHERE[1]
                        input2 = ParseHERE[4]
                        input3 = ParseHERE[7]

                        lineToAdd = []

                        lineToAdd.append(input1)
                        lineToAdd.append(input2)
                        lineToAdd.append(input3)

                        ContactNameRegistry.append(lineToAdd)
                        bigpointer = bigpointer + 1 #iterate each time so that we have a count of the current line.
                Line2 = DataToParse[bigpointer].split(" ")
                ContactListIteration = int(Line2[4]) #get this number.

                bigpointer = bigpointer + 1 #becomes 5
                otherpointer = 0 #set to 0
                for x in range(bigpointer, bigpointer + ContactListIteration):
                        ParseHERE = DataToParse[x].split(" ")
                        flag = 0
                        for x in ContactLists:
                                if x == ParseHERE[1]:
                                        flag = 1 #flag goes up if a duplicate is detected.
                        if flag == 0:
                                ContactLists.append(ParseHERE[1]) #add that list to the list of contactlists.
                                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[3], int(FormattedData[2]))) #send it over to the port on the server side.
                        littlepointer = littlepointer + int(ParseHERE[3])
                        otherpointer = otherpointer + 1

                bigpointer = bigpointer + otherpointer
                for x in range(bigpointer, bigpointer + littlepointer):
                        ParseHERE = DataToParse[x].split(" ")

                        input1 = ParseHERE[1]
                        print(input1)
                        input2 = ParseHERE[4][:-1]
                        print(input2)
                        linerToAdd = []

                        linerToAdd.append(input1)
                        linerToAdd.append(input2)
                        print(linerToAdd)
                        NamesInList.append(linerToAdd)
                        print(NamesInList)
                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[3], int(FormattedData[2])))

        if FormattedData[0] == "im-start":
                IMFlagList = []
                IMFlagName = []
                linebToAdd = []
                linebToAdd.append(FormattedData[1])
                linebToAdd.append(FormattedData[2])


                #print(linebToAdd)

                count = 0
                for y in NamesInList:
                        if y[0] == FormattedData[1]:
                                count += 1

                #print(count)
                if (linebToAdd in NamesInList):
                        #print("Is In List!!!!!\n")
                        #sock.sendto(bytes("im-start", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                        output = "IM-STARTED/"
                        output = output + FormattedData[1] + "/"
                        countAsString = str(count)
                        output = output + countAsString + "/"


                        for x in ContactNameRegistry:
                                if x[0] == FormattedData[2]:
                                        output = output + ("%s %s %s" % (x[0], x[1], x[2]))
                                        output = output + "/"
                        print(NamesInList)
                        # IM-STARTED/[LIST NAME]/[COUNT]/[FIRST USER]/[EVERY OTHER USER]
                        # 0/1/2/3/4
                        newNamesInList = NamesInList.copy()
                        newNamesInList.remove(linebToAdd)
                        IMFlagList = FormattedData[1]
                        IMFlagName = FormattedData[2]

                        print(NamesInList)
                        for y in newNamesInList:
                                if y[0] == FormattedData[1]:
                                        for z in ContactNameRegistry:
                                                if y[1] == z[0]:
                                                        output = output + ("%s %s %s" % (z[0], z[1], z[2])) #sameish loop as above, but prints matching values in CN$
                                                        output = output + "/"
                        print("SUCCESS")
                        print(output)
                        sock.sendto(bytes(output, encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                        #sock.sendto(bytes("AAAAAA!", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                else:
                        print("FAILURE") #deleted at least 1 entry.
                        sock.sendto(bytes("FAILURE", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))

        if FormattedData[0] == "im-complete":
                if FormattedData[1] == IMFlagList:
                        if FormattedData[2] == IMFlagName:
                                sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
                                IMFlagList = ""
                                IMFlagName = ""
                else:
                        sock.sendto(bytes("FAILURE", encoding='utf-8'),(FormattedData[4], int(FormattedData[3])))
        if FormattedData[0] == "exit":
                flag = 0
                otherflag = 0
                nonolist = []
                for x in NamesInList:
                        if x[0] == IMFlagList:
                                nonolist.append(x[1])
                for y in nonolist:
                        if y == FormattedData[1]:
                                otherflag = 1

                if otherflag == 0:
                        for x in ContactNameRegistry:
                                if x[0] == FormattedData[1]:
                                        flag = 1
                                        ContactNameRegistry.remove(x)
                                        print("Removed an instance from CNR")
                        for x in NamesInList:
                                if x[1] == FormattedData[1]:
                                        flag = 1
                                        print("Removed an instance from NIL")
                                        NamesInList.remove(x)
                if flag == 1:
                        print("SUCCESS") #deleted at least 1 entry.
                        sock.sendto(bytes("SUCCESS", encoding='utf-8'),(FormattedData[3], int(FormattedData[2])))
                else:
                        print("FAILURE") #they didn't come up at all.
                        sock.sendto(bytes("FAILURE", encoding='utf-8'),(FormattedData[3], int(FormattedData[2])))

#       print("%s" % str(len(data)))
#       print("%s" % sanData)
#       print("%s" % str(addr)) #used for making sure values were being passed through correctly.