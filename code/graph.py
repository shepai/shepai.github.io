"""
                                                
          Artificial neural network code
          By Dexter R Shepherd, aged 18
          SHEP software version V0.0.8

          An Abstract attempt to model a robotic brain
                                                                         
                      *                                                    
               #     ,                                                     
     .    */    #    #   ***.                                              
            ,##*****/#.                                                    
             %****/*/.*,                                                   
    .,   */,. /.,////##%                                                   
              ( .,,(,..  /(, *                                             
            .      ,       */                                              
         ,.                  (#,  .*              ./((((((*                
                 . .            /(..    ,/,%,     ..*( (...,,.      /   *# 
                                   //#%*. *((%,#/*.          , ((,         
                                                                /   ,.     
                                                                .     /    
                                                                  %,.


        The code uses a series of classes to represent parts of the brain simplified
        The main class, Brain(), is responsible for linking up the individual components such as
        the Parietal_lobe(), responsible for language analyses, shortTerm(), responsible for learning
        correlations between stimulus, and these made up of neuron data structures.
        cellBodyLayer(), dendrite(), axonTerminal()

        Inputs are already tokenized using the nltk library to save writing a learning algorithm for
        word distribution and meaning.
        

        For more information visit https://shepai.github.io/
        
        Code started 08/04/2020

        References:
            [1] Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
         

"""
import os
import sys
import nltk #[1]
import psutil

class dendrite:
    #holds each input into the system
    def __init__(neuron,value,Type):
        neuron.value=value
        neuron.Type=Type
        #save the dendrite
    def getIn(neuron):
        return neuron.value
    def getType(neuron):
        return neuron.Type
class cellBodyLayer:
    #this is the main part of the software
    #This takes in the data from dendrites
    #finds a corrisponding action and checks if the action potential is reached
    #if it is then it refers the inputs onto the
    def __init__(neuron,dentrites):
        neuron.d=dendrites
        #look for current neuron
        #
class axonTerminal:
    #this class will take in an item and type to decide how to use it
    #if the type of input is movement of human the corrosponding input will be movement of robot
    #if the input was sound then the output is text to speech
    def __init__(neuron,item,Type):
        x=0

class Brain:
    #combine the long term and short term memory together
    #manage inputs with cell layers
    #manage tokenization of language
    def __init__(brain,sysPath):
        brain.path=sysPath
        brain.tools=utility()
        if not(os.path.isdir(sysPath)):  #make a pathway
            paths=sysPath.split("/")
            file_exists=""
            for i in range(len(paths)): #loop through creating the folders specified
                try:
                    os.mkdir(file_exists+paths[i])
                    file_exists+=paths[i]+"/"
                except:
                    file_exists+=paths[i]+"/"
        if not(os.path.isdir(sysPath+"ShortTerm")): #create both together
            os.mkdir(sysPath+"ShortTerm") #folder for short term
            os.mkdir(sysPath+"ShortTerm/syntax#") #folder for short term
            os.mkdir(sysPath+"LongTerm") #folder for long term
            os.mkdir(sysPath+"LongTerm/"+"syntax") #folder for long term syntax
            os.mkdir(sysPath+"LongTerm/"+"flow") #folder for storing the flow of words
            os.mkdir(sysPath+"LongTerm/"+"words") #folder for long term words
        brain.ST=shortTerm(sysPath+"ShortTerm/") #create short term memory
        brain.language=parietal_lobe(sysPath+"LongTerm/") #create long term memory language analyser
    def enterStimulus(brain,inputs,types):
        #enter the inputs from sensors into the system
        #this can be made up of touch, visual, sound stimulus as well as already processed language
        language=""
        brain.ST.enterItems(inputs) #enter the inputs into the system to determine what is relevant
        for i in range(len(inputs)):
            if types[i]=="lang": #append lang
                language=inputs[i] #will need to split audio some how
                inputs.remove(language) #remove
        brain.enterLanguage(language) #enter the language in seperatly
    def enterLanguage(brain,information):
        #enter the language into the system
        brain.language.enterWords(information) #enter data in to information
        if brain.language.isSyntax(): #analyze the language
            print("is structure")
        else:
            brain.language.teachGrammar() #teach the grammar to the system
        brain.ST.previous=information
        
class shortTerm:
    #this area manages what information correlates with eachother
    def __init__(brain,sysPath):
        brain.path=sysPath
        brain.previous=""
        brain.tools=utility()
    def enterItems(brain,data):
        for i in range(len(data)):
            if not(os.path.exists(brain.path+data[i]+"/")):
                #is not path so create
                os.mkdir(brain.path+data[i])
                #link to all other inputs
            temp=data.copy()
            temp.remove(data[i])
            brain.linkToItems(data[i],temp)
    def linkToItems(brain,pathway,items):
        #loop through items given and add them to the pathway
        #if already exists increase the weight of the connection
        for i in range(len(items)):
            if brain.tools.isFile(brain.path+pathway+"/"+items[i]+".txt"):
                file=open(brain.path+pathway+"/"+items[i]+".txt","r")#readCurrent
                r=file.read()
                r=int(r)+1
                file.close()
                file=open(brain.path+pathway+"/"+items[i]+".txt","w")#readCurrent
                file.write(str(r))
                file.close()
            else:
                file=open(brain.path+pathway+"/"+items[i]+".txt","w") #create
                file.write("1")
                file.close()
    def getLinks(brain,items):
        #gather the items which are strongly linked with items
        #filters out irrelevent
        #return the relevent to all nodes as an array
        filesIn=[]
        nums=[]
        averages=[]
        for i in range(len(items)): #gather file names and averages of each folder's edges
            SUM=0
            amount=0
            for root, dirs, files in os.walk(brain.path+items[i]):
                filesIn.append(files)
                nom=[]
                for j in range(len(files)):
                    file=open(brain.path+items[i]+"/"+files[j],"r")
                    r=int(file.read())
                    file.close()
                    nom.append(r)
                    SUM+=r
                    amount+=1
                nums.append(nom) #collect number strengths
            if amount==0: #avoid errors
                averages.append(0)
            else:
                averages.append(SUM/amount) #collect averages
        nodes=[]
        for i in range(len(filesIn)): #loop through and pick out nodes
            for j in range(len(filesIn[i])): #loop through all files of item i held in filesIn[i]
                if averages[i]<=nums[i][j] and filesIn[i][j].replace(".txt","") not in nodes: #keep relevant information
                    nodes.append(filesIn[i][j].replace(".txt","")) #add if greater than or equal to average
        return nodes #return the linked inputs
    def gatherLowestRanking(brain,items):
        #gather the lowest links between items to show when there is change
        #this will only work in scenarios when all data entered is known to be linked in one way
        filesIn=[]
        nums=[]
        averages=[]
        for i in range(len(items)): #gather file names and averages of each folder's edges
            SUM=0
            amount=0
            for root, dirs, files in os.walk(brain.path+items[i]):
                filesIn.append(files)
                nom=[]
                for j in range(len(files)):
                    file=open(brain.path+items[i]+"/"+files[j],"r")
                    r=int(file.read())
                    file.close()
                    nom.append(r)
                    SUM+=r
                    amount+=1
                nums.append(nom) #collect number strengths
            if amount==0: #avoid errors
                averages.append(0)
            else:
                averages.append(SUM/amount) #collect averages
        nodes=[]
        for i in range(len(filesIn)): #loop through and pick out nodes
            for j in range(len(filesIn[i])): #loop through all files of item i held in filesIn[i]
                if averages[i]>=nums[i][j] and filesIn[i][j].replace(".txt","") not in nodes: #keep less-relevant information
                    nodes.append(filesIn[i][j].replace(".txt","")) #add if greater than or equal to average
        return nodes #return the linked inputs
class parietal_lobe:
    #manages language comprehension
    #creates the rules of understood language and links language with the appropriete
    #methods of response.
    def __init__(brain,pathway):
        brain.path=pathway
        brain.tools=utility()
        brain.subjects=[] #store the previous subjects which can be reffered too when confused
        #brain.ST=shortTerm(pathway.replace("LongTerm/","shortTerm/syntax#/"))
    def enterWords(brain,words):
        #tokenize words once to save memory
        brain.tokens=nltk.pos_tag(nltk.word_tokenize(words))
        brain.wordArray=[]
        brain.wordTokens=[]
        SubTrig=["NN","IN","NNS","NNP","VBP"] #tokens for subjects
        DetTrig=["PRPS","PRP","PRP$","EX"] #tokens for details
        #set empty lists to save the data to
        subs=[]
        detail=[]
        trigs=[]
        for i in range(len(brain.tokens)):
            brain.wordTokens.append(brain.tokens[i][1])
            brain.wordArray.append(brain.tokens[i][0])
            if brain.tokens[i][1] in SubTrig: #subject found
                subs.append(brain.tokens[i][0])
            elif brain.tokens[i][1] in DetTrig: #tokens on
                detail.append(brain.tokens[i][0])
            else:
                trigs.append(brain.tokens[i][0])
        #brain.ST.enterItems(brain.wordTokens) #find correlation in types of words
        if subs==[]: #always make a subject
            subs=detail
            detail=[]
        brain.subjects=subs # set the current subjects in the brain
        brain.saveData(subs,trigs,detail,"") #save the format the system will use
        brain.saveFlow(words.split()) #save the word flow
    def isSyntax(brain):
        #checks whether the words comply with the current known syntax of the language it
        #has learned so far
        path=brain.path+"syntax/" 
        wordList=brain.wordTokens
        direct=""
        for i in range(len(wordList)):
            if os.path.isdir(brain.path+"syntax/"+direct+wordList[i]):
                direct+=wordList[i]+"/" #add to dir
            else:
                #does not fit current syntax
                return False
        return True #syntax matched
    def teachGrammar(brain):
        #teach the grammar to the system
        direct=""
        for i in range(len(brain.wordTokens)):
            if not(os.path.isdir(brain.path+"syntax/"+direct+brain.wordTokens[i])):
                #not found so add
                os.mkdir(brain.path+"syntax/"+direct+brain.wordTokens[i])
            direct+=brain.wordTokens[i]+"/" #add to dir
    def getSentence(brain,path,info,details):
        #recurse round the data in order to locate the likely sentence
        #takes in the current path and word to stem from
        #further takes in details about
        if os.path.isdir(brain.path+"flow/"+path+info):
            arr = os.listdir(brain.path+"flow/"+path+info)
            arr=[ x for x in arr if ".txt" not in x ] #remove text files
            likelihood=[]
            if arr!=[]: #if array has data
                for i in range(len(arr)): ##find liklihood
                    count=0
                    file=open(brain.path+"flow/"+path+info+"/"+arr[i]+".txt","r")#check files within to find links
                    temp=file.read().split(",")[:-1] #get all items
                    file.close()
                    for j in range(len(details)): #will need to loop round
                        #calculate chance using such
                        if details[j] in temp: #if the next word is found
                             count+=1
                    likelihood.append([arr[i],count])     
                #sort the highest ranking
                largest=likelihood[0][1]
                current=likelihood[0][0]
                for i in range(len(likelihood)):
                    if likelihood[i][1]>largest:
                        largest=likelihood[i][1]
                        current=likelihood[i][0]
                return info+" "+brain.getSentence(path+info+"/",current,details+[info]) #recurse find
            return info
        return "" #if it does not exist
    def saveFlow(brain,words):
        #save the language in the flow of it
        #this will be used to process and write language
        for i in range(len(words)):
            path="flow/"
            for j in range(i,len(words)):
                if not(os.path.isdir(brain.path+path+words[j]+"/")): #if not current
                    os.mkdir(brain.path+path+words[j]+"/")
                    file=open(brain.path+path+"/"+words[j]+".txt","w") #place in folder before
                    temp=words[:j]
                    for z in range(len(temp)): #add each item
                        file.write(temp[z]+",")
                    file.close()
                path+=words[j]+"/"
    def saveData(brain,subs,trig,detail,output):
        #save data in the specific structure
        #if output present then add it
        #if output not present then do not
        direct="words/"
        if os.path.isdir(brain.path+direct+brain.tools.listToString(subs)):
            direct+=brain.tools.listToString(subs)+"/"
        elif subs !=[] : #can only proceed
            direct+=brain.tools.listToString(subs)
            os.mkdir(brain.path+direct)
            direct+="/"
        if os.path.isdir(brain.path+direct+brain.tools.listToString(detail)):
            direct+=brain.tools.listToString(detail)+"/"
        elif detail!=[]:
            direct+=brain.tools.listToString(detail)
            os.mkdir(brain.path+direct)
            direct+="/"
        if os.path.isdir(brain.path+direct+brain.tools.listToString(trig)):
            direct+=brain.tools.listToString(trig)+"/"
        elif trig!=[]:
            direct+=brain.tools.listToString(trig)
            os.mkdir(brain.path+direct)
            direct+="/"
        if output!="":
            print("data to save:",output)
        print("save")
    def findData(brain,subs,trigs,detail):
        #search data using specific method
        #if data not found then attempt to learn based off of training data logs
        #if training data found then attempt it and add it to attempt log
        #if data not found then return not found
        #use neural network style search method
        print("search")
class utility:
    #all the utility methods to be performed throughout the 'brain'
    def getSpace(u):
        #return space left
        obj_Disk = psutil.disk_usage('/')
        left=obj_Disk.free / (1024.0 ** 3)
        return left
    def isFile(u,filename):
        #reeturn if the file exists
        try:
            file=open(filename,"r")
            file.close()
            return True
        except:
            return False
    def listToString(u,s):  
        str1 = ""     
        # traverse in the string   
        for ele in s:  
            str1 += ele +" "  
        # return string   
        return str1[:-1]

x=input("enter a word: ")
pt=parietal_lobe("testGraph/LongTerm/")
x=x.split()
x=pt.getSentence("",x[len(x)-1],x[0:len(x)-1])
print(x)
brain=Brain("testGraph/")
while True:
    x=input(">")
    brain.enterStimulus([x],["lang"])

    
"""                              
               ,,,,,,,,,,,,,,,,,,,,,              
           ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,          
        ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,       
      ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,     
    ,,,,,,,,,,,/@*,,,,,,,,,,,,,,,,,,,,,,,,,,,   
   ,,,,,,,,,,@@@         ,,,,,,,,,,,,,,,,  
  ,,,,,,,,,,&@@@         .,,,,,,,,,,,,,, 
 ,,,,,,,,,,,,,@@              ,,,,,,,,,,,,,,
 ,,,,,,,,,,,,                        ,,,,,,,,,,,,,
 ,,,,,,,,,,,,                        ,,,,,,,,,,,,,
 ,,,,,,,,,,,,                        ,,,,,,,,,,,,,
 ,,,,,,,,,,,,,                      ,,,,,,,,,,,,,,
  ,,,,,,,,,,,,,,                  ,,,,,,,,,,,,,,, 
   ,,,,,,,,,,,,,,,,             ,,,,,,,,,,,,,,,,  
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,   
      ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,     
        ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,       
           ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,          
               ,,,,,,,,,,,,,,,,,,,,.


         Property of SHEP AI
         Use of code must be credited to the developers at SHEP AI
         For more info please contact:
         shep.ai.industries@gmail.com

         Insta: @shep.ai

         

"""
