___Version___="0.1.1"
___Author___ ="Dexter Shepherd"
import xml.etree.ElementTree as ET
#for Python version 3 or above
import sys
import os
import re
import time
import inspect

class AI:
       
       global system_pathway
       
       system_pathway = ""
       
       def __init__(myAI, name, user,file):
           myAI.name = name
           myAI.age = user
           myAI.file = file
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
                     current = open(system_pathway+"main.py","r")
                     r2 = current.read()
                     current.close()
                     if(r != r2):#same
                            #update
                            #myAI.out("updating...")
                            current = open(system_pathway+"main.py","w")
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
                     print("error")
                     return None
       def edit(myAI,sentence):
           #edit the sentence the user has inputted
           trigger=myAI.find_term(sentence,"t")  #search string for trigger word in database
           if trigger!="#@false":
               subject = myAI.find_term(sentence,"s") #search message for subject
               if subject!="#@false":
                   command = myAI.find_term(sentence,"c") #search message for command
                   if command!="#@false":
                       AI = myAI.find(trigger,subject,command,1)  #search database
                       if AI == "/00/00/00": #there is not a sentence
                              #myAI.out("This is not a sentence currently saved")
                              return "This is not a sentence currently saved"
                       else:
                             #myAI.out("What shall I replace that with? ")
                             replacement = myAI.PutIn("What shall I replace it with?") # get the user's input
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
                             file = open(system_pathway+"knowledge.xml","w")    #open database
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
           trigger=myAI.find_term(sentence,"t")  #search string for trigger word in database
           if trigger!="#@false":
               subject = myAI.find_term(sentence,"s") #search message for subject
               if subject!="#@false":
                   command = myAI.find_term(sentence,"c") #search message for command
                   if command!="#@false":
                       #all words needed found
                       #print(trigger)
                       #print(subject)
                       #print(command)
                       AI = myAI.find(trigger,subject,command,0)  #search database
                       if AI[:3] == "!A!":
                           #action
                           #print("ACTION")
                           AI = AI.replace("!A! ","")
                           os.system("sudo python3 "+system_pathway+AI)
                           return "/action/"
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

       def find_term(myAI,message,Stype):
              #find the word and its type
              tree = ET.parse(system_pathway+Stype+".xml")
              root = tree.getroot()
              array=[]
              string=""
              x=-1
              for node in tree.iter('phrase'):#check each phrase
                  ips = node.findall("sub") #check each sub catogory
                  test=[]
                  for ip in ips:
                      string+=ip.text+","
                  
                  test = string.split(",")
                  
                  for i in range(len(test)):
                         if test[i] in message and test[i] != "": #check each word
                                x+=1
                                array.append(test[i]) #compile list of subjects
              if x >= 0:
                   return array[x] #return the keyword
              else:
                   return "#@false" #the command to say nothing found

       def add_word(myAI,phrase,Type):  #add a word to the data
           ##myAI.out("Your sentence is "+phrase)
           ##print("---")
           phrase = phrase.split() #make it a list
           word = "" #the word to save
           i = 0
           
           word = myAI.PutIn("Enter your word or words: ")
           #add word to correct file
           if word != "":
                      myAI.out("Saving now. Your phrase is. "+word)
       
                      
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
                      list=getWord(word)
                      num=1
                      if list != None:
                             
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
       def find(myAI,trigger, subject, command,Type):
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
           if output == "none":    #nothing found in data
               if Type == 0: #learn if this is enabled
                      output = myAI.learn(trigger,subject,command,num)
               else:
                      output = "/00/00/00" #nothing in data
           return output
       def learn(myAI,trigger,subject,command,num):
               #teach the AI
               #myAI.out("Nothing in my data... Please tell me, how you would like me, to respond")
               say = myAI.PutIn("") #get a valid user input
               output = ""
               if say != None:
                      if say == "add action":
                          exit = 1
                          while exit == 1:
                              say = myAI.PutIn("What is the name of your action?")
                              try:    #look for file
                                  file = open("action/"+say+".py","r")
                                  file.close()
                                  exit = 0
                              except:
                                  myAI.out("There is no such file."+str(say))
                          say = "!A! "+"action/"+say+".py"    #save in format

                      file = open(system_pathway+"knowledge.xml","r")    #open database
                      r = file.read() #read data
                      file.close()
                      r = r.replace("</data>","") #remove end
                      r = r + "\t<phrase name=\"command"+str(num)+"\">\n"
                      r = r + "\t<trigger>"+trigger+"</trigger>\n"
                      r = r + "\t<subject>"+subject+"</subject>\n"
                      r = r + "\t<command>"+command+"</command>\n"
                      r = r + "\t<output>"+say+"</output>\n"
                      r = r + "\t</phrase>\n"
                      r = r + "\t</data>\n"
                      #write to file in format
                      ##print(r)
                      #time.sleep(4)
                      file = open(system_pathway+myAI.file,"w")    #open database
                      file.write(r) #write to file
                      file.close()
                      output = say
               else:
                      output = "I didn't add anything, as you told me not to."
               return output
       def addWord(myAI,string,Type):
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
                      list=getWord(word)
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
       def start_program(myAI):
              exit = 0
              while(exit ==0):
                  #print("Enter: ")    
                  user_message = myAI.PutIn("Your message: ") #get userinput
                  
                  if user_message == "/exit":
                         exit=1
                  else:
                      myAI.search(user_message)
                      


