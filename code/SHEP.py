___Version___="0.1.1"
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
import warnings

class AI:
       
       global system_pathway
       
       system_pathway = ""
       
       def __init__(myAI, name, user,file):
           myAI.name = name
           myAI.age = user
           myAI.file = file
           myAI.subject = ""
           myAI.trigger = ""
           myAI.command = ""
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
           #edit the sentence the user has inputted
           trigger=myAI.find_term(sentence,"trigger")  #search string for trigger word in database
           if trigger!="#@false":
               subject = myAI.find_term(sentence,"subject") #search message for subject
               if subject!="#@false":
                   command = myAI.find_term(sentence,"command") #search message for command
                   if command!="#@false":
                       AI = myAI.find(trigger,subject,command)  #search database
                       if AI == "/00/00/00": #there is not a sentence
                              #myAI.out("This is not a sentence currently saved")
                              return "This is not a sentence currently saved"
                       else:
                             #myAI.out("What shall I replace that with? ")
                             
                             file = open(system_pathway+myAI.file,"r")    #open database
                             r = file.read() #read data
                             file.close()
                             temp = ""
                             temp = temp + "\t<trigger>"+trigger+"</trigger>\n"
                             temp = temp + "\t<subject>"+subject+"</subject>\n"
                             temp = temp + "\t<command>"+command+"</command>\n"
                             temp2 = temp + "\t<output>"+replacement+"</output>\n"
                             temp = temp + "\t<output>"+AI+"</output>\n"
                             r = r.replace(temp,temp2)
                             #myAI.out("replacing...")
                             #write to file in format
                             ##print(r)
                             #time.sleep(4)
                             file = open(system_pathway+myAI.file,"w")    #open database
                             file.write(r) #write to file
                             file.close()
                             return "replaced"
                       
                   else:   #no command word found
                       #myAI.out("No command found")
                       time.sleep(1)
                       return "No command"
               else:   #no subject found
                   #myAI.out("No subject found")
                   time.sleep(1)
                   return "No subject"
           else:   
               #myAI.out("No trigger found")
               time.sleep(1)
               #add_word(myAI,sentence,'t')
               return "No trigger"
       def search(myAI,sentence):   #search through data to find if in
           #print("searching '"+sentence+"'")
           trigger=myAI.find_term(sentence,"trigger")  #search string for trigger word in database
           if trigger!="#@false":
               subject = myAI.find_term(sentence,"subject") #search message for subject
               if subject!="#@false":
                   command = myAI.find_term(sentence,"command") #search message for command
                   if command!="#@false":
                       #all words needed found
                       myAI.subject = subject
                       myAI.trigger = trigger
                       myAI.command = command
                       AI = myAI.find(trigger,subject,command)  #search database
                       if AI == None: #validate
                              AI = ""
                       if AI[:3] == "!A!":
                           #action
                           #print("ACTION")
                           AI = AI.replace("!A! ","")
                           print("sudo python3 "+system_pathway+AI)
                           os.system("sudo python3 "+system_pathway+AI)
                           return "/actions/"
                       else:
                           return AI
                           
                   else:   #no command word found
                       #myAI.out("No command found")
                       return "No command"
               else:   #no subject found
                   #myAI.out("No subject found")
                   return "No subject"
           else:   #no trigger found
               #myAI.out("No trigger found")
               return "No trigger"
       def addSubject(myAI,message):
           #automatically add subject with left over strings
           string=""
           word = message.split()
           trig = myAI.find_term(message,"trigger")
           com = myAI.find_term(message,"command")
           
           if trig != "#@false" and com != "#@false" and myAI.find_term(message,"subject") == "#@false":
               #use left over as subject
               
               message = message.replace(trig,".") #remove words whih found their way in
               message = message.replace(com,".") #^
               
               
               use = message.split(".")
               string=""#reset string
               temp = 0
               
               for i in range(len(use)): #find largest word for subject
                   
                   if len(use[i]) >= temp:
                       temp =len(use[i])
                       string = use[i]
               myAI.addWord(string,"subject")
           
       def find_term(myAI,message,Stype):
              #find the word and its type
              tree = ET.parse(system_pathway+Stype+".xml")
              root = tree.getroot()
              array=[]
              string=""
              x=-1
              try:
                     for node in tree.iter('phrase'):#check each phrase
                         ips = node.findall("sub") #check each sub catogory
                         test=[]
                         for ip in ips:
                             string+=ip.text+","
                         
                         test = string.split(",")
                         
                         for i in range(len(test)):
                                if test[i] in " "+message+" " and test[i] != "": #check each word
                                       x+=1
                                       array.append(test[i]) #compile list of subjects
              except:
                     print("--")
              if x >= 0:
                   return array[x] #return the keyword
              else:
                   return "#@false" #the command to say nothing found

       
       def find(myAI,trigger, subject, command):
           tree = ET.parse(system_pathway+myAI.file)
           root = tree.getroot()
           output = "none"
           num = 1
           for i in root.findall("phrase"): #finds all the things to do with this
               trig = i.find("trigger").text
               sub = i.find("subject").text
               com = i.find("command").text
               if trig == trigger and sub == subject and com == command:   #locates data
                   output = i.find("output").text  #find the saved output
               ##print(trig+sub+com)
               num += 1
           myAI.num_of_commands = num
           if output == "none":    #nothing found in data
               output = "/00/00/00" #nothing in data
           
           return output
       def findWiki(myAI,word,command):
              with warnings.catch_warnings():
                     warnings.simplefilter("ignore")
                     
                     word = word.replace(" ","_")
                     string = ""

                     try:
                                   url = "https://en.wikipedia.org/wiki/"+word #wiki page we want
                                   html = urlopen(url).read()
                                   soup = BeautifulSoup(html)

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
                                   #print(text+"\n\n\n\n\n\n")
                                   ToGo = []
                                   if command in text: #the command is found
                                          
                                          #find the words
                                          p2 = [m.start() for m in re.finditer(" "+command+" ", text)]
                                          for i in range(len(p2)): #loop through all the positions
                                                 position = p2[i] #get first position
                                                 

                                                 #print (position)
                                                 sentence = False
                                                 string = ""
                                                 while sentence == False: #get position at begining of sentence
                                                        position-=1
                                                        
                                                        if text[position] == "\n" or position == 0 or position == ".":
                                                               sentence = True
                                                        
                                                 sentence = False #reuse variable for memory speed
                                                 
                                                 while sentence == False:
                                                        
                                                        position+=1
                                                        
                                                        string+=text[position]
                                                        if text[position] == "." or text[position] == "\n" or position == len(text):
                                                               sentence = True
                                                 
                                                 ToGo.append(string)
                                          string = ""
                                          newWord = word.split("_")
                           
                                          for i in range(len(ToGo)):
                                                 counter = 0
                                                 
                                                 for y in range(len(newWord)):
                                                        #accurate finder
                                                        if " "+newWord[y]+" " in " "+ToGo[i]+" " and "this article" not in ToGo[i]: #try find accurate answer
                                                               counter +=1
                                                 if counter == len(newWord):
                                                        string = ToGo[i]
                                                        break #first is most accurate
                                                 #print(ToGo[i])
                                          if string == "": #if none found go with first
                                                 string = ToGo[0]
                                          #return to user below                                          #returned to the user
                                          

                     except:
                            print("No page found")
                            #carry on as normal
                     return string



       def learn(myAI,trigger,subject,command,say):
                      
                      
                      #teach the AI
                      output = ""
                      if "cancel" not in say or "exit" not in say:
                             file = open(system_pathway+"knowledge.xml","r")    #open database
                             r = file.read() #read data
                             file.close()
                             r = r.replace("</data>","") #remove end
                             r = r + "\t<phrase name=\"command"+str(myAI.num_of_commands)+"\">\n"
                             r = r + "\t<trigger>"+trigger+"</trigger>\n"
                             r = r + "\t<subject>"+subject+"</subject>\n"
                             r = r + "\t<command>"+command+"</command>\n"
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
                      return "I am adding: "+output
       def addAction(myAI,name):
              
                                     
              try:    #look for file
                     
                     file = open("action/"+name+".py","r")#check for existance
                     file.close()
                     say = "!A! "+"action/"+name+".py"    #save in format
                     exit = 0
                     file = open(system_pathway+myAI.file,"r")    #open database
                     r = file.read() #read data
                     file.close()
                     r = r.replace("</data>","") #remove end
                     r = r + "\t<phrase name=\"command"+str(myAI.num_of_commands)+"\">\n"
                     r = r + "\t<trigger>"+myAI.trigger+"</trigger>\n"
                     r = r + "\t<subject>"+myAI.subject+"</subject>\n"
                     r = r + "\t<command>"+myAI.command+"</command>\n"
                     r = r + "\t<output>"+say+"</output>\n"
                     r = r + "\t</phrase>\n"
                     r = r + "\t</data>\n"
                     #write to file in format
                     file = open(system_pathway+myAI.file,"w")    #open database
                     file.write(r) #write to file
                     file.close()
                     
                     return ">added"
                     #add to file and set break onn next loop
              except:
                     
                     return ">failed to add"

       def addWord(myAI,word,Type):
                      #data for the AI to add
                      addition = ET.parse(system_pathway+Type+".xml")
                      root = addition.getroot()
                      num = 1
                      for i in root.findall("phrase"): #finds all the things to do with this
                             num += 1
                      file = open(system_pathway+Type+".xml","r")    #open database
                      r = file.read() #read data
                      file.close()
                      
                      r = r.replace("</data>","") #remove end
                      r = r + "\t<phrase name=\"subject"+str(num)+"\">\n"
                      list=myAI.getWord(word)
                      num=1
                      if list != None:
                             #if there are words to be found
                             for i in range(len(list)):
                                    if list[i] != "":
                                           r = r+"\t<sub>"+list[i]+"</sub>\n"
                                           num+=1
                      r = r+"\t<sub>"+word+"</sub>\n"
                      r = r + "\t</phrase>\n"
                      r = r + "\t</data>\n"
                      #write to file in format
                      ##print(r)
                      #time.sleep(4)
                      file = open(system_pathway+Type+".xml","w")    #open database
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
                   copyFiles("/media/usbstick/AI/actions",system_pathway+"/action")
                   myAI.out("Files copied")
                   copyFiles(system_pathway,pathway[i]+"/AI/data")

               except:
                   print("Cannot be done!")
           print("\nGood devices:")
           for i in range(len(devices)):
               print(devices[i]+"---"+pathway[i])
               try:
                   copyFiles(pathway[i]+"/AI/actions","/home/pi/AI/Python_coursework/action")
                   out("Files copied")
                   copyFiles("/home/pi/AI/Python_coursework/",system_pathway,pathway[i]+"/AI/data")
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
                      


#f=AI("","","")
#print(f.findWiki("walt disney","was"))
