#clive mark 2
#Code By Dexter Shepherd aged 18
#Cognitive system to learn information and act on it in a human like way

class AI:
    def __init__(clive,systemPathway,numOfIn):
        #set up clive 
        clive.systemPathway=systemPathway
        clive.numOfInputs=numOfIn
    def setPath(clive,pathway): #set a new pathway
        clive.systemPathway=pathway
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
        structure=["item","SNT","DNT","SENT","SNTS","DNTS","SENTS"]
        file.write("<data:>\n")
        for i in range(len(structure)):
            file.write("<"+structure[i]+">"+data[i]+"</"+structure[i]+">\n")
        file.write("</data:>\n")
        file.close()
    def Increase(clive,string,substring,commas):
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
            average+=int(splitted[i])
        return average/len(splitted)
    def main(clive,inputs):
        for i in range(clive.numOfInputs): #loop through all inputs
            if(not(clive.isFile(str(inputs[i])+".xml"))): #create new nodes if not in existance
                #no file
                stringlist=""
                strengths=""
                for j in range(clive.numOfInputs): #create data needed
                    if j != i:
                        stringlist+=inputs[j]+","
                        strengths+="1,"
                print(strengths[:-1])
                data=[inputs[i],stringlist[:-1],"","",strengths[:-1],"",""] #data in form
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
            
            data=[inputs[i],currentCon,clive.readType(fileread,"DNT"),clive.readType(fileread,"SENT"),currentStr,clive.readType(fileread,"DNTS"),clive.readType(fileread,"SENTS")]   
            file.close()
            clive.writeFile(inputs[i]+".xml",data)
            average=(clive.getAverage(currentStr)) #get average
            ############################################################
            #phase2
            #print(average)
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
        return(nodes)
inputs=["Blue","Blue cup","dog"]      
f=AI("",len(inputs))
f.setPath("test/")
f.main(inputs)
inputs=["Blue","Blue cup","cat"]
f.main(inputs)
inputs=["cat","milk","dog"]
f.main(inputs)
inputs=["Blue","Blue cup","mat"]
f.main(inputs)
inputs=["cat","milk","popping candy"]
f.main(inputs)
