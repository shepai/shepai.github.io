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
from SHEP import Graph,Edge,Queue
import sys
import json
import datetime
def LoadMemory(filepath):
        #read json file
        try: #checkk file exits
            file=open(filepath, "r")
            file.close()
        except: #make file
            data={}
            with open(filepath, "w") as write_file: #write file
                json.dump(data, write_file)

        with open(filepath, "r") as read_file: #read lines
            data = json.load(read_file)
        temp={}
        for i in data:
            temp[i]=[]
            for j in data[i]: #convert list to edge
                e=Edge(j[1][0],j[1][1])
                e.name=j[0]
                e.strength=j[2]
                e.weight=j[3]
                temp[i].append(e)      
        data=temp
        graph = Graph()
        graph.data=data.copy()
        return graph
def SaveMemory(filepath,data):
    #save the data to the memory of that filepath
    temp={}
    for i in data:
        temp[i]=[]
        for j in data[i]: #convert edge to list
             temp[i].append([j.name,j.vertices,j.strength,j.weight])
        with open(filepath, "w") as write_file: #write file
            json.dump(temp, write_file)
class Log:
    def __init__(self,loc,name):
        self.name=name
        self.path=loc
    def add(self,data):
        file=open(self.path+self.name,"a")
        file.write(">"+data)
        file.close()
    def __str__(self):
        return self.name.replace(".txt","")
class ConversationData:
    #store where the conversations are held and act as a reader
    def __init__(self,folder):
        self.folder=folder
    def openDataBase(self,name):
        filepath=self.folder+name+".txt"
        try: #checkk file exits
            file=open(filepath, "r")
            file.close()
        except: #make file
            file=open(filepath, "w")
            file.close()
        file=open(filepath, "r")
        data=file.read()
        file.close()
        data=data.split(">")
        return data
class CB:
    #clever bot redesign
    def __init__(self,path):
        #for language classification
        self.LC=Bot("SHEP-classifier",path) #set up once in the memory
        self.LangC=Language(path)
        #Database pointer
        self.DBP=LoadMemory(path+"link.json")
        self.CDB=ConversationData(path)
        #Hold current information
        self.path=path
        self.convo=Queue()
        uniqueName=str(datetime.datetime.now()).replace(" ","-").replace(".","-").replace(":","-") #works for one person
        self.currentLog=Log(path,uniqueName+".txt")
    def getKEY(self,dt,s,m):
        probability,answer=self.LC.find(dt,s,m)
        KEY=""
        if probability >=0.8: #found
            KEY=answer
        elif probability >=0.5: #might have found
            KEY=answer
        else:
            #not found so add
            answer="C"+str(len(self.LC.Questions.data)) #make key unique
            v1=dt+s+m
            for i in range(3): #add three times for strong con
                for i in v1:
                    self.LC.Questions.addDirected(Edge(i,answer)) #add to graph
                    self.LC.Questions.addDirected(Edge(answer,i)) #add to graph
            SaveMemory(self.path+"questions.json",self.LC.Questions.data)
            KEY=answer
        return KEY
    def matchData(self,info,log):
        #match the information with the logFile and return the simularity
        #enter in log files as split language
        x=0
        
    def processCurrent(self,data,mess):
        #process the data in the current log
        current=self.CDB.openDataBase(str(self.currentLog))#only process up to the point
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
            count=0
            for subject in information[1]: #count if all subjects present
                if subject in d:
                    count+=1
            if count==len(information[1]): #all subjects present
                p+=0.08
            else: #not all subjects are present
                p-=0.15
            if p >=0.8: #found
                chance=p
                break
            elif p >=0.5: #might have found
                if p>ifNoBreakP:
                    chance=p
                    ifNoBreak=indexTo
            indexTo+=1
        if indexTo+2>=len(data) and ifNoBreak>0:
            indexTo=ifNoBreak
        if indexTo+2>=len(data):
            return "",0
        data=data[1:indexTo+2]
        response=data[-1] #get the outcome
        #work out simularity score with current convo
        sim=1
        matched=self.matchData(information,current)
        simularity=(chance+sim)/(1+1)
        #work out
        return response,chance
    def readDatabases(self,databases,message):
        #read each database and rank the simularity of conversation
        potentials=[]
        for i in databases:
            data=self.CDB.openDataBase(i)
            data,p=self.processCurrent(data,message)
            if data!="":
                potentials.append([data,p])
        if len(potentials)>0: #if found
            l=0
            v=""
            for i in potentials: #get largest
                if i[1]>l:
                    v=i[0]
            return v #return largest
        return ""
    def Enter(self,message):
        message=message.replace(">","").replace("\n","")
        dt,s,m=self.LC.splitLanguage(message)
        if len(dt+s+m)<2:
            s=message.split()
        self.currentLog.add(message)
        key=self.getKEY(dt,s,m) #get the key from the message
        #get the databases linked with the phrase
        ED=self.DBP.getConnected(key)
        databases=[]
        for i in ED:
            databases.append(i.vertices[1])
        #######for testing###############################################
        databases.append("testConvo")
        
        #############################################################
        outcome=self.readDatabases(databases,message)#find all posibile outcomes
        self.DBP.addDirected(Edge(key,str(self.currentLog))) #create link between data
        SaveMemory(self.path+"link.json",self.DBP.data) #save
        if outcome=="": #respond with same
            return message
        else:
            self.currentLog.add(outcome)
            return outcome #return the found data
        #get the most 
cleverBot=CB(sys.path[0].replace("\\","/")+"/testCB/")

while True:
    userInput=input(">") #get user input
    x=cleverBot.Enter(userInput)
    print(x)







"""
class AI:
    def __init__(self):
        self.SHEP=Bot("SHEP-Bot",sys.path[0]+"/") #set up once in the memory
        self.interact=botClient(self.SHEP) #set up client in memory
        self.learn=adminBot(self.SHEP,self.SHEP.database) #set up admin
        self.CC=Graph() #set up classical conditioning to find input-->output
        self.topics=Graph() #set up relation of topics Apple--10--Orange---9---Lemon
        self.Related=Graph() #set up classical conditioning to find input--input--input
        self.currentSubjects=[] #needed but not used
        #both variables below for holding the past value for conditioning
        self.previous_response=""
        self.previous_question=""
    def getSignificant(self,node):
        #get the significant nodes
        vals=self.CC.getConnected(node)
        refined=[]
        sum=0
        for i in vals: #sort out significant values
            if i.strength>3:
                refined.append(i)
            sum+=i.strength
        av=sum/len(vals)
        for i in refined: #sort out those values which rise above
            if i.strength>=av: #if rise above add as answer
                self.learn.add(node,i.vertices[1])
    def enter(self,userInput):
        #main method binding the process together
        response=self.interact.Enter(userInput,self.currentSubjects)
        posibilities=self.SHEP.potentials
        print(posibilities)
        if response[0]=="Thank you for your feedback$":
            print("learn logic")
            #attempt to find answer anyway
            x,y,z=self.SHEP.splitLanguage(userInput)
            probability,answer=self.SHEP.find(x,y,z)
            response[1]=y
            if probability >=0.8: #found
                    response[0]=answer
            elif probability >=0.5: #might have found
                if Subsentences.index(i)==0:
                    response[0]="This is something similar I found which may answer your question '"+answer+"'"
            else:
                response[0]="Sorry, I am not sure on that yet. Maybe ask again another time and you will get your answer"
        
        if response[0]=="Sorry, I am not sure on that yet. Maybe ask again another time and you will get your answer":
            #self.info(userInput,[self.currentSubjects]) #conditoin info
            self.SHEP.database.delete(userInput) #delete from confused data
            if self.previous_response!="": #if previous there
                print(self.previous_response,"-->",userInput)
                self.CC.addDirected(Edge(self.previous_response,userInput))
                self.getSignificant(self.previous_response)
            self.previous_response=userInput #unknown response
            #add to classical conditioning with previous response
        else:
             if self.previous_response!="": #if previous there
                print(self.previous_response,"-->",userInput)
                self.CC.addDirected(Edge(self.previous_response,userInput))
                self.getSignificant(self.previous_response)
             response[0]=response[0].replace("$",".").replace("This is something similar I found which may answer your question ","")#return output
             self.previous_response=response[0]
             return response[0]
        self.currentSubjects=[response[1]] #set the past subjects
        
        return "" #return nothing

shep=AI() #creat an AI in the current directory
def INPUT(string):
    #input method for the system
    return input(string)

#main loop
while True:
    userInput=INPUT(">") #get user input
    print(shep.enter(userInput)) #output response

"""
