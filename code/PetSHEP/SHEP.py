#clive mark 2

#Code By Dexter Shepherd aged 18

#Cognitive system to learn information and act on it in a human like way



class AI:

    def __init__(clive,systemPathway,numOfIn):

        #set up clive

        clive.systemPathway=systemPathway

        clive.numOfInputs=numOfIn

        clive.pastNode=[]

    def setPath(clive,pathway): #set a new pathway

        clive.systemPathway=pathway

    def setNum(clive,num): #set the number of inputs

        clive.numOfInputs=num

    def readType(clive,file,Type):

        #read the line of the type

        pos=0

        MAX=len(file)

        string=""

        while not(("<"+Type+">") in string) and pos<MAX:

            string = clive.readLine(file,pos)

            pos+=len(string)+1 #include slash n

        if Type in string:

            string=string.replace("<"+Type+">","")

            string=string.replace("</"+Type+">","")

        return string

    def readLine(clive,string,pos):

        b=""

        substring=""

        while b!="\n" and pos<=len(string): #loop through and gather line at pos

            b=string[pos]

            pos+=1

            substring+=b



        return substring[:-1] #cut off new line

    def isFile(clive,name):

        try:

            file =open(clive.systemPathway+name,"r")

            file.close()

            return True

        except:

            return False

    def writeFile(clive,filename,data): #write in format

        file=open(clive.systemPathway+filename,"w")

        structure=["item","SNT","DNT","SENT","SNTS","DNTS","SENTS","NODESFROM"]

        file.write("<data:>\n")

        for i in range(len(structure)):

            file.write("<"+structure[i]+">"+data[i]+"</"+structure[i]+">\n")

        file.write("</data:>\n")

        file.close()

    def negFeedback(clive,output,inputs):

        #when negative feedback is called this function is executed

        for i in range(len(inputs)):

            print(inputs[i])

            #loop through inputs to remove

            file=open(clive.systemPathway+inputs[i]+".xml","r")

            fileread=file.read()

            file.close()

            DNT=clive.readType(fileread,"DNT")

            splitted=DNT.split(",")

            index=-1

            print(DNT,"remove",output)

            for j in range(len(splitted)):

                if splitted[j] == output:

                    index=j

            if index!=-1: #it is found

                DNTS=clive.readType(fileread,"DNTS")

                DNT=DNT.replace(output,"")

                DNT=DNT.replace(",,",",")

                list1=DNTS.split(",")

                del list1[index]

                str1=","

                str1=str1.join(list1) #remove node

                DNTS=str1

                if DNT[0]==",":

                    DNT=DNT[1:len(DNT)-1]

                if DNT[len(DNT)-1]==",":

                    DNT=DNT[0:len(DNT)-2]

                data=[clive.pastNode[i],clive.readType(fileread,"SNT"),DNT,clive.readType(fileread,"SENT"),clive.readType(fileread,"SNTS"),DNTS,clive.readType(fileread,"SENTS"),clive.readType(fileread,"NODESFROM")]

                clive.writeFile(inputs[i]+".xml",data)



    def Increase(clive,string,substring,commas):

        #increase the current value by

        position=string.find(substring)

        counter=0

        newstring=""

        for i in range(position): #count each position before

            if string[i]==",":

                counter+=1

        splitted=commas.split(",")

        if int(splitted[counter])+1 < 20: #20 is threshold

            splitted[counter]=str(int(splitted[counter])+1)

        for i in range(len(splitted)):

            newstring+=splitted[i]+","

        return newstring[:-1]

    def getAverage(clive,con):

        splitted=con.split(",")

        average=0

        for i in range(len(splitted)):

            if splitted[i]!='':

                average+=int(splitted[i])

        return average/len(splitted)

    def main(clive,inputs):

        inputs=clive.validate(inputs)

        for i in range(clive.numOfInputs): #loop through all inputs

            if(not(clive.isFile(str(inputs[i])+".xml"))): #create new nodes if not in existance

                #no file

                stringlist=""

                strengths=""

                for j in range(clive.numOfInputs): #create data needed

                    if j != i:

                        stringlist+=inputs[j]+","

                        strengths+="1,"

                data=[inputs[i],stringlist[:-1],"","",strengths[:-1],"","",""] #data in form

                clive.writeFile(inputs[i]+".xml",data) #write data

        #all nodes should now exist

        nodes=[]

        for i in range(clive.numOfInputs): #loop through all inputs

            file=open(clive.systemPathway+inputs[i]+".xml",'r') #open current file

            fileread=file.read()

            currentStr=clive.readType(fileread,"SNTS")

            currentCon=clive.readType(fileread,"SNT")

            for j in range(clive.numOfInputs): #loop through all inputs again O(n^2)

                if j!= i: #do not judge same one

                    if inputs[j] in currentCon:

                        #input currently found

                        currentStr=clive.Increase(currentCon,inputs[j],currentStr)

                    else:

                        #input not yet connected

                        currentCon+=","+inputs[j]

                        currentStr+=",1"

            data=[inputs[i],currentCon,clive.readType(fileread,"DNT"),clive.readType(fileread,"SENT"),currentStr,clive.readType(fileread,"DNTS"),clive.readType(fileread,"SENTS"),clive.readType(fileread,"NODESFROM")]

            file.close()

            clive.writeFile(inputs[i]+".xml",data)

            average=(clive.getAverage(currentStr)) #get average

            ############################################################

            #phase2

            #check node strengths to find significant nodes

            #loop through all nodes

            amount=currentStr.count(",")+1

            startpos=0

            startpos1=0

            posCount=0

            string1=""

            string2=""

            for j in range(amount): #loop through all positions without using array (good practise)

                #get each position of the nodes

                endpos=(currentCon[len(string1):len(currentCon)]+",").index(",")

                endpos2=(currentStr[len(string2):len(currentStr)]+",").index(",")

                string=currentCon[len(string1):endpos+len(string1)]

                stringS=currentStr[len(string2):endpos2+len(string2)]

                string1+=string+","

                string2+=stringS+","

                #will need to check that the node is >= to the average

                if int(stringS)>=average:

                    #this node will need to be a current input

                    if string in inputs:

                        #if both met, add it to a list

                        if string not in nodes: #prevent duplicates

                            nodes.append(string)

                #non current but strong inputs are added to a missing part

        #add direct nodes to previous

        if clive.pastNode!=[]: #the array is not empty meaning something happened before

            for i in range(len(clive.pastNode)): #loop round all nodes

                file=open(clive.systemPathway+str(clive.pastNode[i])+".xml","r")

                #open up the node

                fileread=file.read()

                file.close()

                increased=""

                currentCon=clive.readType(fileread,"DNT")

                currentStr=clive.readType(fileread,"DNTS")

                if currentStr!="" and currentCon!="": #some will not have connections if machine turned off or finished execution

                    for j in range(len(nodes)):

                        if nodes[j] != clive.pastNode[i]:

                            if (","+nodes[j]+"," in ","+currentCon+","): #the link does exist

                                #increase node strength

                                if nodes[j] not in increased:

                                    currentStr=clive.Increase(currentCon,nodes[j],currentStr)

                                    increased+=nodes[j]+","

                            else: #the direct link doesn't exist

                                currentCon+=","+nodes[j]

                                currentStr+=","+"1"

                                if currentStr[0]==",":

                                    currentStr=currentStr[1:len(currentStr)]

                                if currentCon[0]==",":

                                    currentCon=currentCon[1:len(currentCon)]

                else:

                    for k in range(clive.numOfInputs):

                        currentCon+=inputs[k]+","

                        currentStr+="1,"

                    currentStr=currentStr[:-1]

                    currentCon=currentCon[:-1]

                data=[clive.pastNode[i],clive.readType(fileread,"SNT"),currentCon,clive.readType(fileread,"SENT"),clive.readType(fileread,"SNTS"),currentStr,clive.readType(fileread,"SENTS"),clive.readType(fileread,"NODESFROM")]

                clive.writeFile(clive.pastNode[i]+".xml",data)



        clive.pastNode=inputs

        return(nodes)

    def validate(clive,inputs):

        for i in range(clive.numOfInputs):

            if "," in inputs[i]:

                inputs[i]=inputs[i].replace(",","-") #replace forbidden ,

        inputs=list(dict.fromkeys(inputs)) #remove duplicates

        clive.numOfInputs=len(inputs) #change input entrance size

        return inputs

    def findValues(clive,inputs):

        nodes=clive.main(inputs)

        #find the sequential nodes

        possible=[]

        probability=[]

        for i in range(len(nodes)): #find strong DNTS

            file=open(clive.systemPathway+nodes[i]+".xml","r")

            fileread=file.read()

            file.close()

            DNT=clive.readType(fileread,"DNT")

            DNTS=clive.readType(fileread,"DNTS")

            average=clive.getAverage(DNTS)

            DNTS=DNTS.split(",") #Make lists

            DNT=DNT.split(",")

            if DNT!=[''] and DNTS!=['']:

                print(DNT,DNTS)

                for i in range(len(DNTS)):

                    if int(DNTS[i]) >= 2 and int(DNTS[i]) >= average and DNT[i] not in possible:

                        possible.append(DNT[i])

                        probability.append(int(DNTS[i]))

            largest=0

            value=""

            for i in range(len(possible)):

                if probability[i] > largest:

                    value=possible[i]

                    largest=probability[i]

                elif probability[i]==largest and possible[i] not in inputs:

                    value=possible[i]

                    largest=probability[i]

            return value



class Language:

    #class to organize and manage language to then input into the main AI class

    #acting as the Temporal lobe to comprehend language

    def __init__(clive,systemPathway):

        clive.systemPathway=systemPathway

    def readType(clive,file,Type):

        #read the line of the type

        pos=0

        MAX=len(file)

        string=""

        while not(("<"+Type+">") in string) and pos<MAX:

            string = clive.readLine(file,pos)

            pos+=len(string)+1 #include slash n

        if Type in string:

            string=string.replace("<"+Type+">","")

            string=string.replace("</"+Type+">","")

        return string

    def readLine(clive,string,pos):

        b=""

        substring=""

        while b!="\n" and pos<=len(string): #loop through and gather line at pos

            b=string[pos]

            pos+=1

            substring+=b



        return substring[:-1] #cut off new line

    def writeToFile(clive,name,data):

        #write data to file

        #data format [nodes to,times used]

        FORMAT=["nodes","used"]

        file =open(clive.systemPathway+name,"w")

        file.write("<data:>\n")

        for i in range(len(data)): #loop through all words

            file.write("<"+FORMAT[i]+">"+data[i]+"</"+FORMAT[i]+">\n")

        file.write("</data:>\n")

        file.close()

    def checkFile(clive,words):

        #find words

        wordhold=words

        words=words.split() #create list

        threshold=0

        nums=[]

        for i in range(len(words)):

            file=0#File file

            try: #try open it

                file =open(clive.systemPathway+words[i]+".xml","r")

            except: #does not exist

                connections=""

                if i+1 < len(words):

                    connections=words[i+1]

                data=[connections,"1"]

                clive.writeToFile(words[i]+".xml",data)

                file =open(clive.systemPathway+words[i]+".xml","r")

            fileread=file.read()

            file.close()

            connect=clive.readType(fileread,"nodes")

            num=clive.readType(fileread,"used")

            if i+1 < len(words): #check

                    if words[i+1] not in connect:

                        #print("not found")

                        connect+=","+words[i+1] #add new ones

                        num=str(int(num)+1) #increased used

            data=[connect,num]

            clive.writeToFile(words[i]+".xml",data) #write changes

            threshold+=int(num)

            nums.append(int(num))

        average=int(threshold/len(words))-(int((3*threshold)/(4*len(words))))

        significant=[]

        for i in range(len(words)): #add all the significant words

            if nums[i] > average:

                significant.append(words[i])



        return significant

    def analyzeLanguage(clive,speech):

        #return what is being asked

        speechArray=speech.split()

        splitted=clive.checkFile(speech)

        sentenceT=""

        sentenceS=""

        for i in range(len(splitted)):

            posibilities=""

            temp=""

            for j in range(len(splitted)):

                #go through each returned element and add to the sentenceT where it is consistant

                posibilities+=splitted[j]+" "

                if posibilities in speech:

                    temp=posibilities

            if len(temp.split()) > len(sentenceT.split()): #get largest connected text

                sentenceT=temp

        sentenceTemp=""

        for i in range(len(speechArray)): #remove splitted values

            if speechArray[i] not in splitted:

                sentenceTemp+=speechArray[i]+" "

        if len(sentenceTemp)>0:

            #values entered

            #clear blank space

            sentenceTemp=sentenceTemp[0:len(sentenceTemp)-1]

            sentenceS=sentenceTemp

        if len(sentenceT)>0:

            #values entered

            #clear blank space

            sentenceT=sentenceT[0:len(sentenceT)-1]

        return [sentenceT,sentenceS]

    def info(clive,speech): #output information to the user

        values=clive.analyzeLanguage(speech)

        print("You are using:",values[0])

        print("about:",values[1])

class sound():

    #breaks up sound strings into numeric words

    #acting as the Temporal lobe to hear and break up hearing

    def __init__(clive,threshold):

        clive.threshold=threshold

    def Break(clive,sound):

        #break up the large string of microphone values

        #this will find the words in the sentence spoken

        sound=sound.split(",")

        i=0

        total=len(sound)

        while i<total:

            #loop round and remove multiple

            counter=0

            if sound[i]==str(clive.threshold):

                j=i+1

                while j<len(sound):

                    if sound[j]==str(clive.threshold): #if multiple

                        counter+=1 #count how many

                    else:

                        break #get out of code if nothing found

                    j+=1

            if counter > 0:

                del sound[i:i+counter]

            total=len(sound) #change size as loop goes on

            i+=1

        #reform words

        string=""

        for i in range(len(sound)):

                string+=sound[i]+","

        sound=string.split(str(clive.threshold)+",")

        #clear up sentence

        soundArray=[]

        for i in range(len(sound)): #final loop

            if sound[i]!='':

                #nothing there

                string=sound[i]

                if string[len(string)-1]==",":

                    string=string[:-1]

                soundArray.append(string)

        return soundArray

