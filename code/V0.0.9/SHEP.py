"""
* Artificial Intelligence chat bot framework
* Code developed by Dexter R Shepherd, aged 18
* Info found at shepai.github.io
* SHEP AI 2020 see license at: https://shepai.github.io/downloads/SHEP%20AI%202020%20License.txt
"""

from DS import *


########################################################################
import nltk
import json
#from spellchecker import SpellChecker

import sqlite3
from difflib import SequenceMatcher
import sys
from itertools import permutations
import re

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
    def __init__(self,path):
        self.Sample_Questions = ["what is the weather like","where are we today","why did you do that","where is the dog","when are we going to leave","why do you hate me","what is the Answer to question 8",
                    "what is a dinosour","what do i do in an hour","why do we have to leave at 6.00", "When is the apointment","where did you go","why did you do that","how did he win","why wonÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬ ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¾ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢t you help me",
                    "when did he find you","how do you get it","who does all the shipping","where do you buy stuff","why donÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬ ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â‚¬Å¾Ã‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¡ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬ ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã†â€™Ãƒâ€šÃ‚Â¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¬ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¾ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬Ãƒâ€¦Ã‚Â¡ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â¢t you just find it in the target","why don't you buy stuff at target","where did you say it was",
                    "when did he grab the phone","what happened at seven am","did you take my phone","do you like me","do you know what happened yesterday","did it break when it dropped","does it hurt everyday",
                    "does the car break down often","can you drive me home","where did you find me"
                    "can it fly from here to target","could you find it for me","hi","hello"
                    "can i join","can i eat candy","hi there","where can i get help","where is the best place"
                    "i was wondering if you could help me","could you tell me where i can find this","thank you"
                    "thanks","what mental health support is there","where can I find the treasure","what time does the theatre open and when does it close"
                    "how do i get in cheaper and how much"]
        try:
            file=open(path+"sentenceDemos.txt","r")
            r=file.read()
            file.close()
            self.Sample_Questions=r.split(":::")
            self.Sample_Questions=self.Sample_Questions[:-1]
        except: #create file
            file=open(path+"sentenceDemos.txt","w")
            for i in self.Sample_Questions:
                file.write(i+":::")
            file.close()
    def splitQuestion(self,sentence):
        tokens = nltk.word_tokenize(sentence) #tokenize sentence
        tagged = nltk.pos_tag(tokens) #get tags
        q=[]
        for i in tagged:
            if "W" == i[1][0] or "VBP" in i[1]:
                q.append(i[0])
        return q
    def splitSubjects(self,sentence):
        tokens = nltk.word_tokenize(sentence) #tokenize sentence
        tagged = nltk.pos_tag(tokens) #get tags
        s=[]
        for i in tagged:
            if "NN" in i[1] or "IN" in i[1] or "JJ" in i[1] or "VBG" in i[1] or "VB"==i[1]:
                s.append(i[0])
        return s
    def splitDirected(self,sentence):
        tokens = nltk.word_tokenize(sentence) #tokenize sentence
        tagged = nltk.pos_tag(tokens) #get tags
        s=[]
        for i in tagged:
            if "P" in i[1][:-1]:
                s.append(i[0])
        return s
    def splitMeaning(self,sentence):
        #split the sentence into the meaning phrases and return to become nodes
        tokens = nltk.word_tokenize(sentence) #tokenize sentence
        tagged = nltk.pos_tag(tokens) #get tags
        nodes=""
        sentences=[]
        for i in tagged:
            if "CC" in i[1]:
                sentences.append(nodes[:-1])
                nodes=""
            else:
                nodes+=i[0]+" "
        if nodes!="":
            sentences.append(nodes)
        return sentences
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
    def increaseByID(self,ID):
        self.cur.execute("SELECT ID,question,priority FROM Data WHERE id=?",(ID,))
        rows = self.cur.fetchall()
        try:
            self.delete(rows[0][1])
            self.cur.execute('insert into Data values (?,?,?)',[ID,rows[0][1],rows[0][2]+1])
        except IndexError: #if error
            self.cur.execute("DELETE FROM Data WHERE ID=?",(rows[0][0],))
    def readData(self):
        self.cur.execute("SELECT * FROM Data")
        rows = self.cur.fetchall()
        return rows
    def containsLanguage(self,data):
        #find if the general saying is within the data:
        self.cur.execute("SELECT * FROM Data")
        rows = self.cur.fetchall()
        data=data.split()
        for i in rows:
            vals=i[1].split()
            if SequenceMatcher(None, vals, data).ratio()>0.9:
                return i[0]
        return None
class Bot:
    def __init__(self,ID,systemPathway):
        self.ID=ID #set an ID for the bot
        self.lang=Language(systemPathway) #Language analyzer
        self.Questions=Graph(systemPathway+"questions.json") #questions analyser
        self.Statements=dataBase(systemPathway+"Statements.db") #statements analyser
        self.systemPathway=systemPathway
        self.database=dataBase(systemPathway+"Confused.db")
        
    def similar(self,a, b):
        count=0
        for i in a:
            if i in b:
                count+=1
        count1=0
        for i in b:
            if i in a:
                count1+=1
        return (count+count1)/(len(a)+len(b))
        #return SequenceMatcher(None, a, b).ratio()
    def assignSim(self,tmp,subjects,AL):
        similarity=0
        if len([x for x in tmp if x in subjects])==len(subjects): #if both subjects present
                    similarity=AL+0.08
        else:
                    similarity=AL-0.2 #lower chance if subjects irrelevant
        return similarity
    def checkQuestion(self,nodes):
            #get the links to each question
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
            questionLinks=[]
            for j in past: #find which answers best fit
                vals=self.Questions.getConnected(j)
                tmp=[]
                for i in vals:
                    val=i.vertices[1]
                    tmp.append(val)
                questionLinks.append([j,tmp])
            return questionLinks
    def splitLanguage(self,sentence):
        directedTo=self.lang.splitDirected(sentence)
        subjects=self.lang.splitSubjects(sentence)
        meaning=self.lang.splitQuestion(sentence)
        return directedTo,subjects,meaning
    def Enter(self,sentence,previous):
        #main query function which takes in a sentence and returns likely response
        Subsentences=self.lang.splitMeaning(sentence)
        GlobalSubjects=self.lang.splitSubjects(sentence)
        lineOfSubjects=""
        response=""
        self.potentials=[] #store all potential responses (>80%)
        self.sub_potentials=[] #store all sub potential responses (>50%)
        Subsentences=[sentence]+Subsentences #try as whole then proceed to split
        for i in Subsentences:
            type=self.lang.getType(i)
            directedTo=self.lang.splitDirected(i)
            subjects=self.lang.splitSubjects(i)
            meaning=self.lang.splitQuestion(i)
            if len(directedTo+subjects+meaning)<2 and subjects: #if small iconic sentence
                directedTo=[]
                meaning=[]
                subjects=i.split()
            if type=="question":
                largestChance,answer = self.find(meaning,directedTo,subjects) #find
                probability=largestChance
                self.findAll(meaning,directedTo,subjects) #find all or the extra data
                if probability >=0.8: #found
                    if Subsentences.index(i)>0:
                        response+=answer+". "
                    else:
                        response=answer
                        break
                elif probability >=0.5: #might have found
                    if Subsentences.index(i)==0:
                        response="This is something similar I found which may answer your question '"+answer+"'"
                        break
            elif type=="statement": #potentially scrap
                #add to statements for analyses of statements
                nodes = directedTo+subjects
                string=""
                for i in nodes: #convert to string
                        string+=i+" "
                        
                id=self.Statements.containsLanguage(string[:-1])
                if id==None:
                        self.Statements.enterData(string[:-1])
                else:
                        self.Statements.increaseByID(id)
                response="Thank you for your feedback"
            if response=="":
                self.database.enterData(sentence)
        return [response,lineOfSubjects]
    def find(self,meaning,directedTo,subjects):
                nodes = meaning+directedTo+subjects
                links=self.checkQuestion(nodes)
                largestChance=0
                answer=""
                foundNodes=[]
                for z in links:
                    ###purge old formats####
                    n=[]
                    for j in z[1]:
                        n+=j.replace("C:","").split()
                    probability=self.similar(n,nodes)
                    count=0
                    
                    for subject in subjects: #count if all subjects present
                        if subject in z[1]:
                            count+=1
                    if count==len(subjects): #all subjects present
                        probability+=0.08
                    else: #not all subjects are present
                        probability-=0.1
                    if probability>largestChance:
                        largestChance=probability
                        foundNodes=z[1]
                        answer=self.removeBrackets(z[0])
                return largestChance,answer
    def findAll(self,meaning,directedTo,subjects):
                nodes = meaning+directedTo+subjects
                links=self.checkQuestion(nodes)
                largestChance=0
                answer=""
                foundNodes=[]
                for z in links:
                    ###purge old formats####
                    n=[]
                    for j in z[1]:
                        n+=j.replace("C:","").split()
                    probability=self.similar(n,nodes)
                    count=0
                    
                    for subject in subjects: #count if all subjects present
                        if subject in z[1]:
                            count+=1
                    if count==len(subjects): #all subjects present
                        probability+=0.08
                    else: #not all subjects are present
                        probability-=0.1
                    if probability>0.8:
                        self.potentials.append(self.removeBrackets(z[0]))
    def removeBrackets(self,string):
        string=re.sub('\[.*?\]', "", string)
        return string.replace("[]","")
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
        question=question.lower()
        if self.bot.Questions.getConnected(answer) !=[]: #cannot have same answer twice
            count=0
            while True: #loop testing out names
                if self.bot.Questions.getConnected(answer+"["+str(count)+"]") ==[]:
                    answer=answer+"["+str(count)+"]"
                    break
                count+=1
        v1=self.bot.lang.splitQuestion(question) #get nodes
        v1+=self.bot.lang.splitSubjects(question) #get nodes
        v1+=self.bot.lang.splitDirected(question) #get nodes
        for i in range(3): #add three times
            for i in v1:
                self.bot.Questions.addDirected(Edge(i,answer)) #add to graph
                self.bot.Questions.addDirected(Edge(answer,i)) #add to graph
        #SaveMemory(self.bot.systemPathway+"questions.json",self.bot.Questions.data) #save to file
        
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
        question=question.replace(":::","")
        
        if self.bot.lang.getType(question)!="question":
            file=open(self.bot.systemPathway+"sentenceDemos.txt","a")
            file.write(question+":::")
            file.close()
            self.bot.lang.Sample_Questions.append(question)
        if self.bot.Questions.getConnected(answer) !=[]: #cannot have same answer twice
            count=0
            while True: #loop testing out names
                if self.bot.Questions.getConnected(answer+"["+str(count)+"]") ==[]:
                    answer=answer+"["+str(count)+"]"
                    break
                count+=1
        v1=self.bot.lang.splitQuestion(question) #get nodes
        v1+=self.bot.lang.splitSubjects(question) #get nodes
        v1+=self.bot.lang.splitDirected(question) #get nodes
        for i in range(3): #add three times
            for i in v1:
                self.bot.Questions.addDirected(Edge(i,answer)) #add to graph
                self.bot.Questions.addDirected(Edge(answer,i)) #add to graph

        #SaveMemory(self.bot.systemPathway+"questions.json",self.bot.Questions.data) #save to file
        self.database.delete(question) #remove from database
    def addStatement(self,sentence):
        self.bot.Enter(sentence,[])
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
        return r #return first instance of deletion
    def getFeedback(self):
        return self.bot.Statements.readData()
    def readReport(self):
        return ReportData.readData()
    def addConfused(self,sentence):
        #add confused data
        self.bot.database.enterData(sentence)
"""
uniBot=Bot("SUSSEXBOT","") #set up once in the memory
ReportData=dataBase(""+"report.db") #set up global database for reports
client=botClient(uniBot) #set up client in memory
admin=adminBot(uniBot,uniBot.database) #set up admin
while True:
    print(client.Enter(input(">"),[]))
    toAdd=admin.getToAdd()
    for i in toAdd:
        print(i)
        val=input("How do I respond to: "+i[1])
        admin.add(i[1],val)
"""
