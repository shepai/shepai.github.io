"""
* SHEP self learning AI code
* 
* Written by Dexter R C Shepherd, Aged 19
* shepai.github.io
*
* Uses SHEP library 2020
* V0.0.9
"""

from SHEP import Bot,Language
from DS import Graph,Edge,Queue
import sys
import json
import datetime
import os
from random import randrange, choice

class Log:
    def __init__(self,loc,name,language):
        if not os.path.exists(loc+"log"): #create log folder
                os.mkdir(loc+"log")
        if not os.path.exists(loc+"confused"): #create confused folder
                os.mkdir(loc+"confused")
        self.name=name
        self.path=loc
        self.convo=[]
        self.convoL=[]
        self.lang=language
        self.SAVE=True
    def add(self,data):
        if self.SAVE: #if save mode on
                file=open(self.path+"log/"+self.name,"a")
                file.write(">"+data)
                file.close()
                if len(self.convo)>15: #max of 15 sentences
                        del self.convo[0]
                        del self.convoL[0]
                self.convo.append(data)
                d=self.lang.splitDirected(data)
                s=self.lang.splitSubjects(data)
                m=self.lang.splitQuestion(data)
                self.convoL.append([d,s,m])
    def __str__(self):
        return self.name.replace(".txt","")
    def check(self,val):
            for (dirpath, dirnames, filenames) in os.walk(self.path+"confused/"):
                    f=filenames
                    for i in f:
                            file=open(self.path+"confused/"+i,"r")
                            r=file.read()
                            file.close()
                            if r==val:
                                    return False
            return True
    def sendToConfused(self):
            #send the log file to the to learn area
            file=open(self.path+"log/"+self.name,"r")
            r=file.read()
            file.close()
            if self.check(r):
                    if len(self.convo)<=1:
                            os.remove(self.path+"log/"+self.name)
                    file=open(self.path+"confused/"+self.name,"w")
                    file.write(r)
                    file.close()
    def readIn(self):
            #read in data
            temp=ConversationData(self.path+"log/")
            d=temp.openDataBase(self.name)
            start=0
            if len(d)-7>0:
                    start=len(d)-7
            for i in d[start:]: #add the data
                self.convo.append(d)
                d=self.lang.splitDirected(d)
                s=self.lang.splitSubjects(d)
                m=self.lang.splitQuestion(d)
                self.convoL.append([d,s,m])
class ConversationData:
    #store where the conversations are held and act as a reader
    def __init__(self,folder):
        self.folder=folder
    def openDataBase(self,name):
        filepath=self.folder+name+".txt"
        try: #checkk file exits
            file=open(filepath, "r")
            data=file.read()
            file.close()
            data=data.split(">")
            return data
        except:
                #future remove connections in list
                return []
class CB:
    #clever bot redesign
    def __init__(self,path):
        #for language classification
        self.LC=Bot("SHEP-classifier",path) #set up once in the memory
        self.LangC=Language(path)
        #Database pointer
        self.DBP=Graph(path+"link.json")
        self.CDB=ConversationData(path)
        #Hold current information
        self.path=path
        self.convo=Queue()
        uniqueName=str(datetime.datetime.now()).replace(" ","-").replace(".","-").replace(":","-") #works for one person
        self.priority=""
        self.currentLog=Log(path,uniqueName+".txt",self.LangC)
        self.convo=[]
    def getKEY(self,dt,s,m):
        probability,answer=self.LC.find(dt,s,m)
        KEY=""
        if probability >=0.8: #found
            KEY=answer
        elif probability >=0.65: #might have found
            KEY=answer
        else:
            #not found so add
            answer="C"+str(len(self.LC.Questions.data)) #make key unique
            v1=dt+s+m
            for i in range(3): #add three times for strong con
                for i in v1:
                    self.LC.Questions.addDirected(Edge(i,answer)) #add to graph
                    self.LC.Questions.addDirected(Edge(answer,i)) #add to graph
            KEY=answer
        return KEY
    def matchData(self,info,log):
        #match the information with the logFile and return the simularity
        #enter in log files as split language
        sumOfP=0
        for i in info:
                l=0
                for j in log:
                      p=self.LC.similar(i,j) #get probability
                      count=0
                      p=self.validateProb(p,i[1],j[1])
                      if p>0.8 and p>l:
                              l=p
                sumOfP+=l
        sumOfP=sumOfP/len(info)
        return sumOfP
    def validateProb(self,p,subs,subs2):
            count=0
            for subject in subs2: #count if all subjects present
                if subject in subs:
                    count+=1
            if count==len(subs2): #all subjects present
                p+=0.08
            else: #not all subjects are present
                p-=0.15
            return p
    def processCurrent(self,data,mess):
        #process the data in the current log
        current=self.CDB.openDataBase("log/"+str(self.currentLog))#only process up to the point
        indexTo=0
        information=self.LC.splitLanguage(mess)
        language=[]
        ifNoBreak=-1
        ifNoBreakP=0
        chance=0
        for i in data:
            vals=self.LC.splitLanguage(i)
            language.append(vals)
            d=vals[0]+vals[1]+vals[2]
            info=information[0]+information[1]+information[2]
            if len(d)<2:
                d=i.split()
            if len(info)<2:
                info=mess.split()
            p=self.LC.similar(d,info)
            p=self.validateProb(p,d,information[1])
            if p >=0.8: #found
                chance=p
                indexTo+=1
                break
            elif p >0.65: #might have found
                if p>ifNoBreakP:
                    chance=p
                    ifNoBreak=indexTo
            indexTo+=1
        if indexTo+1>=len(data) and ifNoBreak>0:
            indexTo=ifNoBreak
        elif indexTo+1>len(data):
            return "",0
        start=1
        if len(data[:indexTo+1])-15>0: #only analyse the last 100 words
               start=(indexTo+1)-15
        data=data[start:indexTo+1]
        response=""
        if len(data)>1:
                response=data[len(data)-1] #get the outcome
        if chance<0.5: #if no chance 
                return "",0 #break
        #work out simularity score with current convo
        matched=self.matchData(language,self.currentLog.convoL)
        simularity=(chance+matched)/(1+1)
        chance=simularity
        #work out
        return response,chance
    def getConfusedFile(self,message):
        #read throough confused files and find most similar
        #return data log object
        f=[]
        for (dirpath, dirnames, filenames) in os.walk(self.path+"confused/"):
            f=filenames
            break
        l=0
        log=None
        for i in filenames:
               data1=self.CDB.openDataBase("confused/"+i.replace(".txt",""))
               data,p=self.processCurrent(data1,message)
               if len(data)>0:
                       if data!="" and p>l and data1[-1]!=message:
                                log=Log(self.path,i,self.LangC)
                                l=p
        if log!=None:
                os.remove(self.path+"confused/"+log.name)
                return log
        return ""
    def readDatabases(self,databases,message):
        #read each database and rank the simularity of conversation
        potentials=[]
        S=[]
        for i in databases:
            data=self.CDB.openDataBase(i)
            #data==[]
            data,p=self.processCurrent(data,message)
            
            if data!="":
                potentials.append([data,p])
                S.append(i)
        potentials2=[]
        if len(potentials)>0: #if found
            l=0
            v=""
            for i in potentials: #get largest
                if i[1]>l:
                    v=i[0]
                    l=i[1]
                if i[1]<l+0.15 and i[1]>l-0.15: #within bound
                        potentials2.append(i[0])
            if l<0.30 and len(self.currentLog.convo)>2: #if the probability is low then no longer save information to it
                    return ""
            if l>0.9: #if the conversation is really relevant
                print("*")
                return v
            print("~")
            c=0
            val=choice(potentials2) #return one of largest
            while c<len(potentials2)-1 and val in self.convo: #get one which has not been used
                del potentials2[potentials2.index(val)] #remove
                val=choice(potentials2) #return one of largest
                c+=1
            return val
        return ""
    def getRandom(self,type):
            #get a random phrase
            f=[]
            dates=[]
            for (dirpath, dirnames, filenames) in os.walk(self.path+type):
                    f=filenames
                    for i in f:
                        val=os.path.getctime(self.path+type+i)
                        dates.append(val)
                    break
            tmp=[]
            num=20
            if len(f)<20:
                num=len(f)
            for i in range(20): #get top 20
                item=max(dates)
                ind=dates.index(item)
                tmp.append(f[ind])
                del f[ind]
                del dates[ind]
            f=tmp.copy()
            data=[".."]
            val=self.convo[-1]
            count=0
            while val in self.convo and count<len(f): #try not repeat itself
                while len(data)<=1:
                                r=randrange(len(f)) #get out ofbounds
                                if r==len(f): #avoid out of bounds error
                                        r=r-1
                                i=f[r]
                                del f[r] #remove from choices
                                data=self.CDB.openDataBase(type+i.replace(".txt",""))
                                val=data[len(data)-1] #last position
                                
                count+=1
            return val
    def getShort(self,message):
            #get all short responses
            f=[]
            for (dirpath, dirnames, filenames) in os.walk(self.path+"confused/"):
                    f=filenames
                    for i in f:
                            data=self.CDB.openDataBase("confused/"+i.replace(".txt",""))
                            if len(data)==2 and data[1]!=message and data[1] not in self.convo:
                                    #delete file from log
                                    os.remove(self.path+"confused/"+i)
                                    return data[1]
                    break
            print("no short")
            return ""
    def setGetKey(self,message):
            dt,s,m=self.LC.splitLanguage(message)
            if len(dt+s+m)<2:
                    s=message.split()
            key=self.getKEY(dt,s,m) #get the key from the message
            return key
    def Enter(self,message):
        message=message.replace(">","").replace("\n","")
        self.currentLog.add(message) 
        key=self.setGetKey(message)
        #get the databases linked with the phrase
        ED=self.DBP.getConnected(key)
        databases=[]
        for i in ED:
            databases.append("log/"+i.vertices[1])
        #######for testing###############################################
        databases.append("testConvo")
        #############################################################
        outcome=self.readDatabases(databases,message)#find all posibile outcomes
        self.DBP.addDirected(Edge(key,str(self.currentLog))) #create link between data
        self.DBP.addDirected(Edge(str(self.currentLog),key)) #create link between data
        if outcome=="": #respond with same
            #gather message from
            Cfile=self.getConfusedFile(message)
            if Cfile!="":
                    #load into question queue and pick target
                    Cfile.readIn()
                    if len(Cfile.convo)>0:
                            self.currentLog=Cfile
                            return self.currentLog.convo[len(self.currentLog.convo)-1] #return last item
            self.currentLog.sendToConfused()
            uniqueName=str(datetime.datetime.now()).replace(" ","-").replace(".","-").replace(":","-") #works for one person
            self.currentLog=Log(self.path,uniqueName+".txt",self.LangC) #start again
            r=self.getRandom("confused/") #WILL RETURN RANDOM
            self.currentLog.add(r)
            print("&")
            return r
        else:
            self.currentLog.add(outcome)
            return outcome #return the found data
        #get the most
    def chat(self,message):
                self.convo.append(message)
                if len(self.convo)>15:
                        del self.convo[0]
                robotMessage=self.Enter(message)
                key=self.setGetKey(robotMessage) #set response as pointer
                self.DBP.addDirected(Edge(key,str(self.currentLog))) #create link between data
                self.DBP.addDirected(Edge(str(self.currentLog),key)) #create link between data
                self.convo.append(robotMessage)
                if len(self.convo)>15:
                        del self.convo[0]
                return robotMessage
    def train(self,array):
                #train in an array of conversation phrases
                count=0
                for message in array[:-1]:
                        key=self.setGetKey(message)
                        self.DBP.addDirected(Edge(key,str(self.currentLog))) #create link between data
                        self.currentLog.add(message)
                        self.currentLog.add(array[count+1])
                        count+=1
                        print("percentage:",str((count/len(array))*100),"%")
"""
cleverBot=CB(sys.path[0].replace("\\","/")+"/testCB/")

filen="C:/Users/Dexter Shepherd/Documents/Python/convo2.txt"
file=open(filen,"r")
r=file.read()
file.close()
slashn="""
"""
r=r.replace("bot2:","bot1:")
r=r.replace(slashn,"")
r=r.replace(".","").replace(",","").replace("?","").replace("!","")
r=r.split("bot1: ")
r=r[1:]
cleverBot.train(r)

while True:
    userInput=input(">") #get user input
    x=cleverBot.chat(userInput)
    print(x)
"""
