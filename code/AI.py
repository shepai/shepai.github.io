"""
* Artificial Intelligence chat bot framework
* Code developed by Dexter R Shepherd, aged 18
* Info found at shepai.github.io
"""

#graph machine learning
class Queue:
    #queue data structure 
    def __init__(self):
        self.data=[]
    def push(self,item):
        self.data.append(item)
    def pop(self):
        item = self.data[0]
        del self.data[0]
        return item
    def size(self):
        return len(self.data)
class Edge:
    def __init__(self,vertex1,vertex2):
        self.name=""
        self.vertices=[vertex1,vertex2]
        self.strength=0
        self.weight=0
class Graph:
    #graph data structure for associative learning
    def __init__(self):
        self.data={}
    def addDirected(self,edge):
        #add data
        try:
            val=self.data[edge.vertices[0]]
            changes=False
            for i in range(len(val)):
                #print(edge.vertices[0],val[i].vertices[1],edge.vertices[1])
                if val[i].vertices[1]==edge.vertices[1]: #if found increase strength connection
                    val[i].strength+=1
                    changes=True
            if changes==False: #if not yet in
               val.append(edge) #add
               try: #check if real
                   val=self.data[edge.vertices[1]]
               except:
                    self.data[edge.vertices[1]]=[] #add node with no connections
            else:
                self.data[edge.vertices[0]]=val
        except:
            self.data[edge.vertices[0]]=[edge] #add node with no connections
            self.data[edge.vertices[1]]=[]
    def addUndirected(self,edge):
        #add data undirected (so for both nodes)
        self.addDirected(edge) #add edge
        edge=self.getEdge(edge.vertices[0],edge.vertices[1]) #get new connetion
        vertices=edge.vertices #reverse edge connection
        strength=edge.strength
        edge=Edge(vertices[1],vertices[0]) #new edge to not confuse with old memory
        edge.strength=strength
        self.addDirected(edge) #add edge 
    def show(self):
        for i in self.data:
            print(i)
            for j in self.data[i]:
                print(j.vertices,j.strength)
    def delete(self,vertex):
        try:
            cons=self.getConnected(vertex)
            for i in cons: #remove each connection to if undirected
                current=self.data[i.vertices[1]]
                while vertex in current: #delete where it appears
                    del current[current.index(vertex)]
            return self.data.pop(vertex, None) #finally remove
        except: #nothing in the data
            return None
    def getConnected(self,vertex):
        #return all directly connected to the given vertex
        data=[]
        try:
            return self.data[vertex]
        except:
            return []
    def allReachable(self,vertex,offlimits):
        #Get a path to see if two points are reachable
        #uses breadth-first algorithm
        visited=[]
        q=Queue()
        q.push(vertex)
        visited.append(vertex)
        while q.size()>0:
            v=q.pop() #get the next connected item
            connections=self.getConnected(v)
            for i in connections:
                if i.vertices[1] not in visited and i.vertices[1] not in offlimits: #accurate
                    visited.append(i.vertices[1])
                    q.push(i.vertices[1])
        return visited
    def getEdge(self,vertex1,vertex2):
        for i in self.data[vertex1]:
            if i.vertices[1]==vertex2:
                return i
    def shortestRoute(self,start,end,offlimit):
        q=Queue()
        q.push(start)
        cameFrom={}
        cost={}
        cameFrom[start]=None
        cost[start]=0
        while q.size()>0: #sort paths 
            current=q.pop()
            if current == end:
                break
            for next in self.getConnected(current):
                new_cost=cost[current]+next.weight
                if next.vertices[1] not in offlimit:
                    if next.vertices[1] not in cost or new_cost<cost[next.vertices[1]]:
                        cost[next.vertices[1]]=new_cost
                        q.push(next.vertices[1])
                        cameFrom[next.vertices[1]]=current
        try:
            key=cameFrom[end]
        except: #error as it is not connected
            return None
        #find direct route
        cameFromKeys=list(reversed(sorted(cameFrom)))
        path=[]
        key=end
        path.append(key)
        while key!=start:
            key=cameFrom[key]
            path.append(key)
        return list(reversed(path))
    def strongest(self,vertex):
        connections=self.getConnected(vertex)
        if len(connections)>0:
            sum=0
            for i in connections:
                sum+=i.strength
            average=sum/len(connections)
            nodes=[]
            for i in connections:
                if i.strength>average:
                    nodes.append(i.vertices[1])
            return nodes
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
########################################################################
import nltk
import json
#from spellchecker import SpellChecker
import threading
import sqlite3
from difflib import SequenceMatcher
import asyncio
import websockets
import sys


class SpellEngine:
    #def __init__(self):
        #self.spell = SpellChecker()
    def getCorrected(self,sentence):
        sentence=sentence.replace("?",".").replace("!",".").replace(";",".") #split sentences
        #misspelled = self.spell.unknown(sentence.replace(".","").split())
        #for word in misspelled:
        #    # Get the one `most likely` answer
        #    correct=self.spell.correction(word)
        #    sentence=sentence.replace(word,correct)
        sentence=sentence.split(".")
        i=0
        while i<len(sentence): #delete empty
            if sentence[i]=="":
                del sentence[i]
                i-=1
            i+=1
        return sentence
class Language:
    def __init__(self):
        self.Sample_Questions = ["what is the weather like","where are we today","why did you do that","where is the dog","when are we going to leave","why do you hate me","what is the Answer to question 8",
                    "what is a dinosour","what do i do in an hour","why do we have to leave at 6.00", "When is the apointment","where did you go","why did you do that","how did he win","why wonÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢t you help me",
                    "when did he find you","how do you get it","who does all the shipping","where do you buy stuff","why donÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢t you just find it in the target","why don't you buy stuff at target","where did you say it was",
                    "when did he grab the phone","what happened at seven am","did you take my phone","do you like me","do you know what happened yesterday","did it break when it dropped","does it hurt everyday",
                    "does the car break down often","can you drive me home","where did you find me"
                    "can it fly from here to target","could you find it for me","hi","hello"
                    "can i join","can i eat candy","hi there","where can i get help","where is the best place"
                    "i was wondering if you could help me","could you tell me where i can find this","thank you"
                    "thanks","what mental health support is there","where can I find the treasure"]
    def splitMeaning(self,sentence):
        #split the sentence into the meaning phrases and return to become nodes
        tokens = nltk.word_tokenize(sentence) #tokenize sentence
        tagged = nltk.pos_tag(tokens) #get tags
        nodes=[]
        string="C:"
        for i in tagged:
            if "W" in i[1] or "VB" == i[1] or "CD" in i[1] or "IN" in i[1]:
                string+=i[0]+" " #change to i[1] to get tokens instead
            elif "NN" in i[1] or "RB" in i[1] or "JJ" in i[1] or "VBP" in i[1] or "PR" in i[1]:
                nodes.append(string[:-1]) #add chunks of wordsor
                string="C:"
                nodes.append(i[0])
            else:
                nodes.append(string[:-1]) #add chunks of words
                string="C:"
        if string!="":
            nodes.append(string[:-1])
        i=0
        while i<(len(nodes)): #remove empty spaces
            if nodes[i] == "" or nodes[i]=="C":
                del nodes[i]
                i-=1
            i+=1
        if len(nodes)==0 and len(sentence.split())<4:
            #small phrase
            nodes=sentence.split() #add small phrases anyway
        return nodes
    def getType(self,sentence):
        for Ran_Question in self.Sample_Questions:
            Question_Matcher = SequenceMatcher(None, Ran_Question, sentence).ratio()
            if Question_Matcher > 0.5:
                        return "question"
        return "statement"
class dataBase:
    def __init__(self,name):
        self.name=name
        found=True
        try:
            file=open(name,"r")
            file.close()
        except: #check if database needs forming
            found=False
        try:
            self.conn = sqlite3.connect(name)
            self.cur=self.conn.cursor()
            if found==False: #if not yet created
                self.cur.execute("CREATE TABLE Data(id INT, question STRING, priority INT)") #store input row
                self.conn.commit()
        except (RuntimeError, TypeError, NameError) as e:
            raise e("Cannot connect to the database!")
        self.getPK()
    def getPK(self):
        self.cur.execute("SELECT * FROM Data")
        rows = self.cur.fetchall()
        self.PK=len(rows)+1
    def enterData(self,question):
        self.cur.execute("SELECT ID,priority FROM Data WHERE question=?",(question,))
        rows = self.cur.fetchall()
        p=0
        if len(rows)!=0:
            self.delete(question)
            p=rows[0][1]+1
        self.cur.execute('insert into Data values (?,?,?)',[self.PK,question,p])
        self.conn.commit()
        self.PK+=1
    def delete(self,question):
        self.cur.execute("DELETE FROM Data WHERE question=?",(question,))
        self.conn.commit()
    def readData(self):
        self.cur.execute("SELECT * FROM Data")
        rows = self.cur.fetchall()
        return rows
class Bot:
    def __init__(self,ID,systemPathway):
        self.ID=ID #set an ID for the bot
        self.lang=Language() #Language analyzer
        self.Questions=LoadMemory(systemPathway+"questions.json") #questions analyser
        self.Statements=LoadMemory(systemPathway+"statements.json") #statements analyser
        self.systemPathway=systemPathway
        self.database=dataBase(systemPathway+"Confused.db")
        self.AutomaticSave() #run save method in background
    def AutomaticSave(self):
          #save the data at intervals
          threading.Timer(60, self.AutomaticSave).start() #in seconds
          #SaveMemory(self.systemPathway+"sentence.json", self.Statements.data)
          processThread = threading.Thread(target=SaveMemory, args=(self.systemPathway+"statements.json", self.Statements.data));
          processThread.start();
    def similar(self,a, b):
        return SequenceMatcher(None, a, b).ratio()
    def Enter(self,sentence,previous):
        #main query function which takes in a sentence and returns likely response
        type=self.lang.getType(sentence)
        nodes=self.lang.splitMeaning(sentence)
        subjects=[]
        for i in nodes: #gather the subjects
                if "C:" not in i:
                    subjects.append(i)
        response=""
        if type=="question":
            #query question data base
            past=[]
            for i in nodes: #gather the subject responses
                vals=self.Questions.getConnected(i)
                tmp=[]
                for j in vals:
                    val=j.vertices[1]
                    if val not in past:
                        tmp.append(val)
                past+=tmp
            largest=0
            value=""
            for j in past: #find which answers best fit
                vals=self.Questions.getConnected(j)
                tmp=[]
                for i in vals:
                    val=i.vertices[1]
                    tmp.append(val)
                if len([x for x in tmp if x in subjects])==len(subjects): #if both subjects present
                    similarity=self.similar(tmp,nodes)
                else:
                    similarity=self.similar(tmp,nodes)-0.2 #lower chance if subjects irrelevant
                if similarity>largest: #get most simular
                    largest=similarity
                    value=j
            print(largest)
            if largest<0.80: #if the data is not significant
                #process simular
                if largest>=0.5:
                    response="This is something similar I found which may answer your question '"+value+"'"
                else:
                    if subjects==[]: #vague sentence
                        print("no subjects")
                    self.database.enterData(sentence)
            else:
                response=value
        elif type=="statement":
            #add to statements for analyses of statements
            subjects.append("C-feedback")
            for i in subjects:
                for j in subjects:
                    if i!=j:
                        self.Statements.addDirected(Edge(i,j)) #add to graph
            x=0
            response="Thank you for your feedback"
        return [response,subjects]
    
class botClient:
    #built to use less memory and provide an interface with the main bot
    #responsible for interacting
    def __init__(self,bot):
        self.bot=bot
        self.SC=SpellEngine() #deploy the spell check engine
    def Enter(self,userInput,subjects):
        if userInput!="":
            sentences=self.SC.getCorrected(userInput)
            responses=""
            for i in sentences:
                returned=self.bot.Enter(i,subjects)
                responses+=returned[0]+"$"
                subjects=returned[1]
            responses=responses.replace("..",".")
            responses=responses.replace(". .",".")
            if responses.replace("$","")=="":
                responses="Sorry, I am not sure on that yet. Maybe ask again another time and you will get your answer"
            string=""
            for i in subjects:
                string+=i+","
            return [responses,string[:-1]]
        return ""
    def add(self,question,answer):
        if self.bot.Questions.getConnected(answer) !=[]: #cannot have same answer twice
            count=0
            while True: #loop testing out names
                if self.bot.Questions.getConnected(answer+"["+str(count)+"]") ==[]:
                    answer=answer+"["+str(count)+"]"
                    break
                count+=1
            print("changing name to",answer)
        v1=self.bot.lang.splitMeaning(question) #get nodes
        for i in v1:
            self.bot.Questions.addDirected(Edge(i,answer)) #add to graph
        for i in v1:
            self.bot.Questions.addDirected(Edge(answer,i)) #add to graph
        SaveMemory(self.bot.systemPathway+"questions.json",self.bot.Questions.data) #save to file
        
    def feedback(self,type,sentence):
        if type=="negative":
            self.bot.database.enterData(sentence)
    def report(self,question):
        #report the data to the admin
        ReportData.enterData(question)
class adminBot:
    #built to use less memory and provide an interface with the main bot
    #responsible for teaching and managing
    def __init__(self,bot,database):
        self.bot=bot
        self.database=database
    def getToAdd(self):
        return self.database.readData()
    def add(self,question,answer):
        if self.bot.Questions.getConnected(answer) !=[]: #cannot have same answer twice
            count=0
            while True: #loop testing out names
                if self.bot.Questions.getConnected(answer+"["+str(count)+"]") ==[]:
                    answer=answer+"["+str(count)+"]"
                    break
                count+=1
            print("changing name to",answer)
        v1=self.bot.lang.splitMeaning(question) #get nodes
        for i in v1:
            self.bot.Questions.addDirected(Edge(i,answer)) #add to graph
        for i in v1:
            self.bot.Questions.addDirected(Edge(answer,i)) #add to graph
        SaveMemory(self.bot.systemPathway+"questions.json",self.bot.Questions.data) #save to file
        self.database.delete(question) #remove from database
    def delete(self,question):
        self.database.delete(question) #remove from database
    def deleteQ(self,question):
        a=self.bot.Enter(question,[])
        r=self.bot.Questions.delete(a[0])
        if r!=None:
            f=r.copy()
            while f!=None:
                a=self.bot.Enter(question,[])
                f=self.bot.Questions.delete(a[0])
                print("delete",f)
        return r #return first instance of deletion
    def getFeedback(self):
        #get the bot graph to return the most said phrases
        cons=self.bot.Statements.getConnected("C-feedback")
        #organize into most frequent
        temp=[]
        for i in range(len(cons[:-1])):
            currentStrength=cons[i].strength
            next=cons[i+1].strength
            num=i
            while next<currentStrength and num>0:
                print(cons)
                temp=cons[num]
                cons[num]=cons[num+1]
                cons[num+1]=temp
                num-=1
                currentStrength=cons[num].strength
        feedback=""
        for i in cons:
            feedback+=i.vertices[1]+":::"
            if len(feedback)>500: #too many to send
                break
        return feedback
    def readReport(self):
        return ReportData.readData()
    def addConfused(self,sentence):
        #add confused data
        self.bot.database.enterData(sentence)
uniBot=Bot("SUSSEXBOT","/var/www/html/") #set up once in the memory
ReportData=dataBase("/var/www/html/"+"report.db") #set up global database for reports
client=botClient(uniBot) #set up client in memory
admin=adminBot(uniBot,uniBot.database) #set up admin
Admins=[]
file=open("/home/shep/Desktop/pw.txt","r") #store codes here
r=file.read()
file.close()
codes=r.split("-")
print("opening server")
async def clientReply(websocket, path):
    try:
        async for message in websocket:
            #will need to split down
            if "FEEDBACKN" in message: #negative feedback add sentence to confused
                client.feedback("negative",message.replace("FEEDBACKN",""))
            elif "FEEDBACKP" in message:
                a=message.replace("FEEDBACKP","").split("---")
                client.add(a[0],a[1])
            elif "REPORT" in message:
                print("report")
                client.report(message.replace("REPORT",""))
            else:
                message=message.split("---")
                arr=[]
                for i in message[1].split(","):
                    arr.append(i)
                x=client.Enter(message[0],arr)
                await websocket.send(x[0]+"---"+x[1])
    except websockets.exceptions.ConnectionClosedError:
        print("User disconnected")
async def adminReply(websocket, path):
    print("admin")
    try:
        async for message in websocket:
            #will need to split down
            if "signInRequest:" in message:
                #sign in
                message=message.replace("signInRequest:","")
                message=message.split("--")
                if message[0]==codes[0] and message[1]==codes[1]:
                    print(websocket,"has joined the administration")
                    Admins.append(websocket)
                    await websocket.send("signInRequestGranted")
                else:
                    await websocket.send("ERROR")
            elif message=="VIEWDATA" and websocket in Admins:
                print("view")
                #return the data
                string=""
                d=admin.getToAdd()
                for i in d:
                    string+=i[1]+":::"
                    if len(string)>500: #prevent websocket error
                        break
                await websocket.send(string[:-3]) #send list of to add
            elif message=="VIEWFEEDBACK" and websocket in Admins:
                #return the feedback statements
                data=admin.getFeedback()
                await websocket.send(data)
            elif "RADD" in message and websocket in Admins:
                #add for reporting
                a=message.replace("RADD","")
                a=a.split("---")
                ReportData.delete(a[0]) #delete from database
                admin.deleteQ(a[0]) #delete from memory
                admin.add(a[0],a[1]) #add to the bot
            elif "QADD" in message and websocket in Admins:
                #add a question back using undo method
                admin.addConfused(message.replace("QADD",""))
            elif "ADD" in message and websocket in Admins:
                print("add",message.replace("ADD",""))
                a=message.replace("ADD","")
                a=a.split("---")
                admin.add(a[0],a[1]) #add to the bot
            elif "DELETER" in message and websocket in Admins:
                ReportData.delete(message.replace("DELETER",""))
            elif "DELETE" in message and websocket in Admins:
                print("delete",message.replace("DELETE",""))
                admin.delete(message.replace("DELETE",""))
            elif "DELQUE" in message and websocket in Admins:
                print("delete",message.replace("DELQUE",""))
                val=admin.deleteQ(message.replace("DELQUE",""))
                if val==None:
                    await websocket.send("ERROR")
            elif "REPORT" in message and websocket in Admins:
                string=""
                d=admin.readReport()
                for i in d:
                    string+=i[1]+":::"
                await websocket.send(string[:-3]) #send list of to add
    except websockets.exceptions.ConnectionClosedError:
            print("remove admin", websocket)
            del Admins[Admins.index(websocket)]
asyncio.get_event_loop().run_until_complete(
websockets.serve(clientReply, port=50007)) #listen for clients
asyncio.get_event_loop().run_until_complete(
websockets.serve(adminReply, port=8080)) #listen for clients
asyncio.get_event_loop().run_forever()
