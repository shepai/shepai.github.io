"""Dependencies"""
#pip install wikipedia
#pip install google-api-python-client
#   if Errors: pip install --upgrade oauth2client
#pip install nltk
"""Code to download"""
#MyCalendar.py from shepai.github.io/downloads
#   You will need to create your own google calendar key
#   Use tutorial: https://www.youtube.com/watch?v=j1mh0or2CX8

import nltk
from MyCalendar import calendar
import wikipedia
import datetime as dt
from datetime import date, datetime

class chatBot:
    #simple chatbot
    #virtual assistant
    def __init__(self,name):
        self.calendar=calendar() #call in our library
        #defining key words
        self.questionTerms=["what","when","why","who","where","how","can"]
        self.mathsTerms=["plus","divided","minus","add","square root","squared",
                         "divide","subtract","multiply","add","times","NUM","multiplied","subtracted"]
        self.timeTerms=["time","date","day"]
        self.Months=["january","febuary","march","april","may","june","july","august",
                     "september","october","november","december"]
        self.calendarTerms=self.Months+["happening","going on", "calendar","monday","tuesday",
                                        "wednesday","thursday","friday","saturday","sunday","today","tomorrow"]
        self.questions={"your name":"my name is "+name,"your age":"I was made on the 21/01/21",
                        "how are you":"I am good thanks"}
        self.statement={"like you":"thanks"}
    def breakDown(self,sentence):
        sentence=sentence.lower() #convert to lower case
        tokens=nltk.word_tokenize(sentence)
        tags=nltk.pos_tag(tokens)
        sub=[]
        phrase=""
        for word,tag in tags:
            if tag=="VBZ": #add and then split
                phrase+=word+" "
                if phrase!="": sub.append(phrase)
                phrase=""
            elif tag[0]=="W" or tag=="ADJ" or tag=="IN" or tag=="CC" or tag=="TO" or tag=="VBG" or tag=="PRP$":
                #split then add
                if phrase!="": sub.append(phrase)
                phrase=""
                phrase+=word+" "
            else:
                phrase+=word+" "
        if phrase!="": sub.append(phrase)
        return sub
    def normalizeNum(self,text):
        text=text.split()
        newPhrase=""
        for tk in text:
            if tk!="":
                if tk.isnumeric():
                    newPhrase+="NUM "
                else:
                    newPhrase+=tk+" "
        return newPhrase[:-1]
    def getMeaning(self,phrases):
        questionC=0
        mathsC=0
        timeC=0
        calendarC=0
        numFound=0
        for phrase in phrases:
            phrase=self.normalizeNum(phrase)
            for i in self.mathsTerms: #maths classification done
                if i in phrase:
                    mathsC+=1
                if i=="NUM" and i in phrase:
                    numFound+=1
            for i in self.questionTerms:
                if i in phrase:
                    questionC+=1
            for i in self.calendarTerms:
                if i in phrase:
                    calendarC+=1
            for i in self.timeTerms:
                if i in phrase:
                    timeC+=1
        if questionC>0 and numFound>0 and numFound<mathsC:
            return "maths question"
        elif questionC>0 and calendarC>0:
            return "calendar question"
        elif questionC>0 and timeC>0:
            return "time question"
        elif questionC>0:
            return "question"
        else:
            return "statement"
    def checkPresent(self,sentence,data):
         #check whether sentence is in data given
         output=""
         for chunk in sentence:
              for phr in data:
                  if phr in chunk:
                      output=data[phr]
         return output
    def extractSubjects(self,sentence):
        sentence=sentence.lower()
        tokens=nltk.word_tokenize(sentence)
        tags=nltk.pos_tag(tokens)
        subs=[]
        s=""
        for word,tag in tags:
            if tag=="NN" or tag=="JJ":
                s+=word+" "
            else:
                if s!="": subs.append(s)
                s=""
        if s!="": subs.append(s)
        return subs
    def chat(self,message):
        BD=self.breakDown(message)
        Type=self.getMeaning(BD)
        output=""
        if Type=="calendar question":
            months=[]
            days=[]
            years=[]
            defaultY=date.today().strftime("%Y")
            defaultM=date.today().strftime("%m")
            defaultD=date.today().strftime("%d")
            for phr in BD:
                for i in self.Months:
                    if i in phr:
                        m=str(self.Months.index(i)+1)
                        if len(m)==1: months.append("0"+m)
                        else: months.append(m)
                for word in phr.split():
                    word=word.replace("st","").replace("cnd","").replace("rd","").replace("th","")
                    if word.isnumeric():
                        if int(word)<=31:
                            days.append(word)
                        elif int(word)>2000:
                            years.append(word)
            if years==[]:
                    years.append(defaultY)
            if len(months)==0:
                    months.append(defaultM)
            if "today" in message and len(days)==0:
                    days.append(defaultD)
            try:
                    tasks=self.calendar.getDay(days[0]+" "+months[0]+" "+years[0])
                    output="You have "
                    for task in tasks:
                        output+=task[0]+" at "+task[1]+", "
                    if output=="You have ": output+="nothing on that day"
            except:
                    pass
        elif Type=="maths question":
            refined=[]
            for word in message.split():
                if word.isnumeric() or word in self.mathsTerms:
                    refined.append(word) #collect an array of numbers and operators
            num=0
            toDo="add"
            for i in refined:
                output+=i+" "
                if i.isnumeric():
                    if "add" in toDo or "plus" in toDo:
                        num+=int(i)
                    elif "sub" in toDo or "minus" in toDo:
                        num-=int(i)
                    elif "times" in toDo or "multipl" in toDo:
                        num=num*int(i)
                    elif "divide" in toDo and int(i)!=0:
                        num=num/int(i)
                    elif int(i)==0:
                        output="I cannot do that"
                        break
                else:
                    toDo=i
            if output!="I cannot do that": output+="is "+str(num)
        elif Type=="time question":
            #day=dt.datetime.today().weekday()
            now=datetime.now()
            d=date.today()
            output="It is "+str(now.strftime("%H:%M"))+str(d.strftime(" %B %d, %Y "))#+str(day)
        if Type=="question":
            output=self.checkPresent(BD,self.questions)
            if output=="":
                subs=self.extractSubjects(message)
                try:
                    output=wikipedia.summary(subs[0]).split(".")[0]
                except:
                    pass
        elif output=="":
            output=self.checkPresent(BD,self.statement)
        if output=="":
            return "I am sorry, I can't help with that"
        else:
            return output


c=chatBot("Brian")
while True:
    print(c.chat(input(">")))
