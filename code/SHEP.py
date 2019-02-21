___Version___="0.1.2"
___Author___ ="Dexter Shepherd"
import xml.etree.ElementTree as ET
#for Python version 3 or above
import sys
import os
import re
import time
import inspect
from lxml import html
from subprocess import *
import subprocess

try:
       import httplib
except:
       import http.client as httplib

from urllib.request import urlopen
import urllib

#####################################
from bs4 import BeautifulSoup
import re
import requests
import warnings

class AI:
       
       global system_pathway
       
       system_pathway = ""
       
       def __init__(myAI, name, user,file):
           myAI.name = name
           myAI.age = user
           myAI.file = file
           myAI.listOfVocab = []
           myAI.num_of_commands = 0
       def setFile(myAI,string):#set the file to a different one
              myAI.file = string
       def setpath(myAI,string):#set the file to a different one
              global system_pathway
              system_pathway = string
       def update(myAI):
              try:
                     file = open(system_pathway+"test.txt","w")
                     for line in urlopen("https://shepai.github.io/code/SHEP.py"):
                            #decode the file and write it to the Pi
                            s = line.decode('utf-8')
                            ##print(s)
                            file.write(s)
                     file.close()
                     
                     file = open(system_pathway+"test.txt","r")
                     r = file.read()
                     file.close()
                     current = open(system_pathway+"SHEP.py","r")
                     r2 = current.read()
                     current.close()
                     if(r != r2):#same
                            #update
                            #myAI.out("updating...")
                            current = open(system_pathway+"SHEP.py","w")
                            current.write(r)
                            current.close()
                            os.system("sudo reboot")    #restart with new
              except:
                     print("Error finding update")
       def PutIn(myAI,string):  #use fundtion so method of output can be changed for hardware
           myAI.out(string)#method of output
           return input()  #return input
       def out(myAI,string):    #use fundtion so method of output can be changed for hardware
           print(string)#method of output
       def getWord(myAI,word): #use an online thesarus
              try:
                     oxford="https://en.oxforddictionaries.com/thesaurus/"+word #location
                     page = requests.get(oxford)
                     tree = html.fromstring(page.content)
                     syn = tree.xpath('//span[@class="syn"]/text()') #strip html away
                     string = ""
                     for i in range(len(syn)):
                         string+=syn[i]

                     string=string.replace("'","")
                     list=string.split(",")
                     for i in range(len(syn)):
                         print(list[i])
                     return list
              except:
                     
                     return None
       def edit(myAI,sentence,replacement):
                   words = myAI.find_term(sentence) #search message for subject
                   myAI.listOfVocab = words #assign the global need          
                   AI = myAI.find(words)  #search database
                   if AI == None: #validate
                              AI = replacement
                   
                   if AI == "/00/00/00": #there is not a sentence
                       #myAI.out("This is not a sentence currently saved")
                       return "This is not a sentence currently saved"
                   else:
                             #myAI.out("What shall I replace that with? ")
                             
                             file = open(system_pathway+myAI.file,"r")    #open database
                             r = file.read() #read data
                             file.close()
                             temp = ""
                             words = myAI.find_term(sentence) #search message for subject
                             for i in range(len(words)):
                                    temp = temp + "\t<word>"+words[i]+"</word>\n"
                             
                             temp2 = temp + "\t<output>"+replacement+"</output>\n"
                             temp = temp + "\t<output>"+AI+"</output>\n"
                             r = r.replace(temp,temp2)

                             file = open(system_pathway+myAI.file,"w")    #open database
                             file.write(r) #write to file
                             file.close()
                             return "replaced"
                       
       def search(myAI,sentence):   #search through data to find if in
                   words = myAI.find_term(sentence) #search message for subject
                   myAI.listOfVocab = words #assign the global need       
                       
                   AI = myAI.find(words)  #search database
                   if AI == None: #validate
                              AI = ""
                   if AI[:3] == "!A!":
                           #action
                           #print("ACTION")
                           #output the sentence to the file.
                           file = open(system_pathway+"actions/"+input.txt,"w")
                           file.write(sentence)
                           file.close()

                           AI = AI.replace("!A! ","")
                           print("sudo python3 "+system_pathway+AI)
                           #os.popen("sudo python3 "+system_pathway+AI).read()
                           os.system("sudo python3 "+system_pathway+AI)
                           return "/actions/"
                   elif AI[:3] == "!L!":
                          #open link
                          with warnings.catch_warnings():
                                 warnings.simplefilter("ignore")#ignore promptd
                                 url=AI.replace("!L!","")#remove codes
                                 string=""
                                 html1 = urlopen(url).read()#read information
                                 page = requests.get(url)
                                 class_find = ["mod","dc_mn","rwrl rwrl_sec rwrl_padref rwrl_hastitle","rwrl rwrl_pri rwrl_padref","rcABP rcABPfocus","Z0LcW","b_focusTextLarge","b_focusTextMedium"]
                                 for i in range(len(class_find)):
                                        try: #try all the different classes
                                               soup = BeautifulSoup(html1)
                                               soup = soup.find("div", {"class":class_find[i]})
                                               # kill all script and style elements
                                               for script in soup(["script", "style"]):
                                                      script.extract()    # rip it out
                                               # get text
                                               text = soup.get_text()
                                               # break into lines and remove leading and trailing space on each
                                               lines = (line.strip() for line in text.splitlines())
                                               # break multi-headlines into a line each
                                               chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                                               # drop blank lines
                                               text = '\n'.join(chunk for chunk in chunks if chunk)
                                               string=text
                                               break #break when found (order of priority
                                        except:
                                               error=1
                          return string
                   else:
                           return AI
                           
                   
           
       def find_term(myAI,message):
              #find the word and its type
              tree = ET.parse(system_pathway+"vocab.xml")
              root = tree.getroot()
              array=[]
              string=""
              #validate the file
              file = open(system_pathway+"vocab.xml","r")
              r=file.read()
              file.close()
              
              message = message.split()
              if len(r)>16:
                     
                            for node in tree.iter('phrase'):#check each phrase
                                ips = node.findall("sub") #check each sub catogory
                                test=[]
                                for ip in ips:
                                    string+=ip.text+","
                                test = string.split(",")
                                type = ""
                                x=0
                            for i in range(len(message)):
                                       for j in range(len(test)):
                                              if " "+message[i]+" " in "  "+test[j]+"  " and message[i] != "" and test[j] != "": #check each word
                                                     x=j+1#save number
                                                     
                                       if x == 0: #word not found must be added
                                                     types=myAI.wordAdder(message[i])
                                                     
                                                     if len(types[0]) > 0:
                                                            type = "ts" #trigs and subs
                                                     elif len(types[2]) > 0:
                                                            type = "ci" #command and identifiers
                                                     elif len(types[3]) > 0:
                                                            type = "ss" #subjects and slang
                                                     else:
                                                            type = "i"
                                                     if type != "i":#save word
                                                         myAI.addWord(message[i],type)
                                                         array.append(message[i])
                                       else:
                                              array.append(message[i]) #compile list of subjects
                                       x=0
                     
              else:
                     #add words if need adding
                     for i in range(len(message)):
                            types=myAI.wordAdder(message[i])
                            
                            if len(types[0]) > 0:
                                   type = "ts" #trigs and subs
                            elif len(types[2]) > 0:
                                   type = "ci" #command and identifiers
                            elif len(types[3]) > 0:
                                   type = "ss" #subjects and slang
                            else:
                                   type = "i"
                            if type != "i":#save word
                                   myAI.addWord(message[i],type)          
                                                         
              return array #return the keywords
              

       
       def find(myAI,message):
           tree = ET.parse(system_pathway+myAI.file)
           root = tree.getroot()
           output = "none"
           num = 1
           string = ""
           x=0
           if True: #used for debugging
                     for node in tree.iter('phrase'):#check each phrase
                         ips = node.findall("word") #check each sub catogory
                         test=[]
                         num += 1 #global counter
                         for ip in ips:
                             string+=ip.text+","
                         if len(string)>1:    
                                if string[len(string)-1]==",": #remove uneeded spaces
                                       string = string[:-1]
                         
                         test = string.split(",")
                         
                         for j in range(len(message)):
                                #gather words 
                                for i in range(len(test)):
                                       
                                       if " "+test[i]+" " in "  "+message[j]+"  " and str(test[i]) != "": #check each word
                                              x+=1#gather the amount of words which are found
                                
                                       if x == (len(test)) and ((x > 3 and len(message) > 3) or (x<=3 and len(message)<=3)): #all words
                                              string=""
                                              ips = node.findall("output") #check each sub catogory
                                              
                                              for ip in ips:
                                                  string+=ip.text+","
                                              output = (string.split(","))[0] #first output
                                                 
                         
                         x=0
                         string=""
           
           myAI.num_of_commands = num
           if output == "none":    #nothing found in data
               output = "/00/00/00" #nothing in data
           
           return output
       def wordAdder(myAI,words):
                  sentence = words
                  words=words.split() #split the words
                  phrases=[[]for i in range(5)]
                  for i in range(len(words)):
                      word=words[i]
                      #get each word
                      
                      s=""
                      try:
                             
                          #get each word and find out what type of word it is           
                          oxford="https://en.oxforddictionaries.com/definition/"+word
                          page = requests.get(oxford)
                          tree = html.fromstring(page.content)
                          #get it by class of word
                          syn = tree.xpath('//span[@class="pos"]/text()')
                          
                          for i in range(len(syn)):
                              s+=syn[i]+" "
                      except:
                          print("") #no page is found
                      s = s.upper()
                      
                      
                      
                      #split all the terms down into the following
                      if  ("PRONOUN" in s) and "ADJECTIVE" not in s:
                              phrases[0].append(word) #add to the possible subjects and triggers
                              
                      elif ("NOUN" in s):
                          phrases[3].append(word)
                          phrases[4].append(s)
                      elif ("VERB" in s and "ADVERB" not in s):
                              phrases[1].append(word) #Ignore uneeded detail
                      elif "DETERMINER" in s or "ABBREVIATION" in s or "POSSESSIVE DETERMINER" in s or "ADVERB" in s or "ADJECTIVE" in s:
                          #command words and identifiers
                          phrases[2].append(word)
                      else:#the connecting words and unknown
                          #mixture of subjects and slang words
                              phrases[3].append(word)
                              phrases[4].append(s)
                      #split all the terms down into the following
                      
                      #return wanted word
                  return phrases

       def research(myAI,word):
              with warnings.catch_warnings():
                     warnings.simplefilter("ignore")#ignore promptd
                     word=word.replace("+","%2B") #if equations are wanted
                     
                     word = word.replace(" ","+")
                     string = ""
                     
                     #get links -- r.html.absolute_links
                     url = "https://www.bing.com/search?q="+word #page we want
                     try:
                                   html1 = urlopen(url).read()
                                   
                                   try:
                                        page = requests.get(url)
                                        class_find = ["dc_mn","rwrl rwrl_sec rwrl_padref rwrl_hastitle","rwrl rwrl_pri rwrl_padref","rcABP rcABPfocus","Z0LcW","b_focusTextLarge","b_focusTextMedium"]
                                        for i in range(len(class_find)):
                                               
                                               try: #try all the different classes
                                                      soup = BeautifulSoup(html1)
                                                      soup = soup.find("div", {"class":class_find[i]})
                                                      # kill all script and style elements
                                                      
                                                      for script in soup(["script", "style"]):
                                                            script.extract()    # rip it out
                                                            

                                                      # get text
                                                      text = soup.get_text()

                                                      # break into lines and remove leading and trailing space on each
                                                      lines = (line.strip() for line in text.splitlines())
                                                      # break multi-headlines into a line each
                                                      chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                                                      # drop blank lines
                                                      text = '\n'.join(chunk for chunk in chunks if chunk)
                                                      string=text
                                                      break
                                               except:
                                                      error=1
                                   except:
                                          #this part of the code takes all the information
                                          #not used yet but will be soon
                                          soup = BeautifulSoup(html1)
                                          # kill all script and style elements
                                          for script in soup(["script", "style"]):
                                              script.extract()    # rip it out

                                          # get text
                                          text = soup.get_text()
                                          text = text.lower()

                                          # break into lines and remove leading and trailing space on each
                                          lines = (line.strip() for line in text.splitlines())
                                          # break multi-headlines into a line each
                                          chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                                          # drop blank lines
                                          text = '\n'.join(chunk for chunk in chunks if chunk)
                                          
                                          string = text
                                   

                     except:
                            print("No page found")
                            #carry on as normal
                     #print(string)
                     if string != "":
                            return url #returned url so it can be researched
                                                        
                     else:
                            return ""



       def learn(myAI,sentence,words,say):
                      #teach the AI
                      output = ""
                      say=say.replace(",",".")#commas do not work
                      if "cancel" not in say or "exit" not in say:
                             file = open(system_pathway+"knowledge.xml","r")    #open database
                             r = file.read() #read data
                             file.close()
                             r = r.replace("</data>","") #remove end
                             r = r + "\t<phrase name=\"command"+str(myAI.num_of_commands)+"\">\n"
                             for i in range(len(words)): #add needed words
                                    r = r + "\t<word>"+words[i]+"</word>\n"
                             
                             r = r + "\t<output>"+say+"</output>\n"
                             r = r + "\t</phrase>\n"
                             r = r + "\t</data>\n"
                             #write to file in format
                             #print(r)
                             #time.sleep(4)
                             file = open(system_pathway+"knowledge.xml","w")    #open database
                             file.write(r) #write to file
                             file.close()
                             output = say
                      else:
                             output="cancelling"
                      return "I am adding: "+myAI.search(sentence) #show user how it will add
       def addAction(myAI,name):                      
              try:    #look for file
                     
                     file = open(system_pathway+"actions/"+name+".py","r")#check for existance
                     file.close()
                     
                     #gets here without error means file exists
                     filepathway = ("actions/"+name+".py").replace(" ","\ ")
                     say = "!A! "+ filepathway   #save in format
                     
                     
                     return say
                     #add to file and set break onn next loop
              except:
                     
                     return ">failed to add"

       def addWord(myAI,word,Type):
                      #data for the AI to add
                      
                      if word == None:
                             word=""
                      addition = ET.parse(system_pathway+"vocab.xml")
                      root = addition.getroot()
                      num = 1
                      for i in root.findall("phrase"): #finds all the things to do with this
                             num += 1
                      file = open(system_pathway+"vocab.xml","r")    #open database
                      r = file.read() #read data
                      file.close()
                      #write in format
                      r = r.replace("</data>","") #remove end
                      r = r + "\t<phrase name=\"Word"+str(num)+"\">\n"
                      
                      num=1
                      if word != "" and word != None:
                             if word[0] == " ":
                                    word=word[1:len(word)]#make sure word is good format
                             #write the sub and type into the file
                             r = r+"\t<sub>"+" "+word+"</sub>\n"
                             r = r+"\t<type>"+" "+Type+"</type>\n"
                             r = r + "\t</phrase>\n"
                             r = r + "\t</data>\n"
                             #write to file in format
                             
                             file = open(system_pathway+"vocab.xml","w")    #open database
                             file.write(r) #write to file
                             file.close()
       def listUSB(myAI):
           list = os.popen("lsblk").read()
           print(list)
           list = list.split()
           i=7
           errors=[]
           devices=[]
           pathway=[]
           
           list = os.popen("lsblk").read()
           list = list.split()
           while i < (len(list)):
               
               i+=6
               if i < (len(list)):
                       
                   if "/" not in list[i]: #no pathway so in fact
                       errors.append(list[i-6]) #make list of bad one's
                       
                       
                   else: #pathway
                       devices.append(list[i-6])
                       pathway.append(list[i])
                       i+=1
           #show to user
           print("Bad devices:")
           for i in range(len(errors)-1):
               print(errors[i])
               os.system("sudo mount -t vfat -o rw /dev/"+errors[i]+" /media/usbstick/")
               #create a mount
               if "└─" in errors[i+1]:
                   errors[i+1] = errors[i+1].replace("└─","")
                   os.system("sudo mount -t vfat -o uid=pi,gid=pi /dev/"+errors[i]+" /media/usbstick/")
               
               try:
                   myAI.copyFiles("/media/usbstick/AI/actions",system_pathway+"/action")
                   myAI.out("Files copied")
                   myAI.copyFiles(system_pathway,pathway[i]+"/AI/data")

               except:
                   print("Cannot be done!")
           print("\nGood devices:")
           for i in range(len(devices)):
               print(devices[i]+"---"+pathway[i])
               try:
                   myAI.copyFiles(pathway[i]+"/AI/actions",system_pathway+"action")
                   myAI.out("Files copied")
                   myAI.copyFiles(system_pathway,system_pathway,pathway[i]+"/AI/data")
               except:
                   print("Cannot be done!")

               
       def copyFiles(myAI,directory,to):
           # copy subdirectory example
           fromDirectory = directory
           toDirectory = to

           copy_tree(fromDirectory, toDirectory)
       def start_program(myAI):
                     exit = 0
                     while(exit ==0):
                         #print("Enter: ")    
                         user_message = myAI.PutIn("Your message: ") #get userinput
                         
                         if user_message == "/exit":
                                exit=1
                         else:
                             myAI.search(user_message)
                      


#f=AI("","","knowledge.xml") 
#x=input()
#print(f.research(x))
#f.learn(f.listOfVocab,input("answer:"))
