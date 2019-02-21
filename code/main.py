___Version___="0.0.6"
___Author___ ="Dexter Shepherd"
from SHEP import AI
import time
#import the internet connection libraries
try:
       import httplib
except:
       import http.client as httplib
from urllib.request import urlopen
from wifi import Cell, Scheme
#clear up type errors
from subprocess import Popen, STDOUT, PIPE
from subprocess import *
import subprocess
import os
import re
#eye
import time
import colorsys
from pixels import Pixels #found in folder

#speech recognition lib
import speech_recognition as sr
pixels = Pixels()

#initialize global variables
global audio


myBot = AI("SHEP", "user","knowledge.xml") #SHEP is called in
system_pathway = "/home/pi/AI/Python_coursework/"
myBot.setpath(system_pathway)

def audioCheck():
       global rec
       global m
       global audio
       try:
              #variables to listen to audio with
              rec = sr.Recognizer() 
              #Typlcal sample rates are 44.1 kHz (CD), 48 kHz, 88.2 kHz, or 96 kHz.
              m = sr.Microphone()
              audio = rec.adjust_for_ambient_noise(source) #adjust audio
       except:
              OUTPUT("Problem connecting to microphone")
              error_pixels()
def internet():
       conn = httplib.HTTPConnection("www.google.com", timeout=5) #attempt connection
       try:
           conn.request("HEAD", "/")
           conn.close()
           return True #show there is a connection
       except:
           conn.close()
           error_pixels()
           return False #show there is not a connection
def error_pixels():
       #the pixels desplayed for an error
       pixels.off()
       pixels.wakeup()
       time.sleep(0.2)

           
def update():
       try:
              file = open(system_pathway+"temp.txt","w")
              for line in urlopen("https://shepai.github.io/code/main.py"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              cont1=""
              cont2=""
              for line in urlopen("https://shepai.github.io/code/knowledge.xml"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     cont1+=s
              for line in urlopen("https://shepai.github.io/code/vocab.xml"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     cont2+=s
              setUP(cont1,cont2)#add the files
              file.close()
              file = open(system_pathway+"temp.txt","r")
              r = file.read()
              file.close()
              current = open(system_pathway+"main.py","r")
              r2 = current.read()
              current.close()
              if(r == r2):#same
                     print("No update needed")
              else:
                     #update
                     OUTPUT("updating...")
                     current = open(system_pathway+"main.py","w")
                     current.write(r)
                     current.close()
                     os.system("sudo reboot")    #restart with new
       except:
              print("Error finding update")
              
def OUTPUT(string):#output method
    #locate the arduino port
    try:
       #output using onboard TTS
       print(string)
       pixels.speak() #coulourful look
       string = string.replace("'","") #prevent an apostriphe messing it up.
       os.system("espeak '"+string+"' 2>/dev/null")
       
    except:
           #no connection
           print(string)
           error_pixels()
           
def getVoice():#input method
           global audio
    
           voiceReply = ""
           connection_errors = 0 #show there is a strong connection
           print("setting...")
           rec.dynamic_energy_threshold = False #set ackground noise to silence
           t0 = 0 #set the timer
           with m as source:    #listen audio
                  print ("Speak Now")
                  t0 = time.time() #start a timer to prevent the search going on too long
                  pixels.listen()    #output eye to the user
                  audio = rec.listen(source,timeout=5)                   # listen for the first phrase and extract it into audio data
           t1 = time.time() #take a second reading of the time
           total = t1-t0 #work out how long it took
           pixels.off() #stop the LEDs
           print(">>")
           timer = 0
           if total < 15: #it will take too long to convert otherwise
                      try:
                             voiceReply = (rec.recognize_google(audio,language = "en-GB"))
                             print("you said "+str(voiceReply))
                             if "could not understand" in voiceReply.lower(): #prevent annoying output
                                    voiceReply = ""
                      except:
                             voiceReply="" 
           else:
                      print("Took too long to respond...")
                      audioCheck()
    
           return voiceReply #return voice

def INPUT(string):
    OUTPUT(string)#method of output
    string = ""
    try:
           string = getVoice() #get voice input
    except:
           #no microphone or internet error
           audioCheck()
           error_pixels()
           if not(internet()):
                  OUTPUT("There is an error connecting to the internet")
                  wifi()
    if "robot" in string and "cancel" not in string:
           print("----------------------------------")
           file=open(system_pathway+"action/input.txt",'w')
           file.write(string)
           file.close()
           if "robot keyboard" in string:
                     string = input("Please type: ")#type mode
           else:
                     string = (string.replace("robot ","",1))#getrid of call sign
           pixels.think()   #show the user it is thinking
           
           if "robot" == string:
                  string = ""
           words = string.split()
           title=""
    else:
           string=""

    return string.lower()   #return voice  #return input
    


def add(to_add):
    #get the type to add
    if to_add == "action" or to_add == "an action":
        valid=">failed to add"
        add=True
        while valid == ">failed to add":
            userInput = INPUT("What is the file name")
            if "cancel" == userInput or "exit" == userInput:
                #allow the user to change their mind and not add
                valid = ">added"
                OUTPUT("I shall not add an action")
            else:
                while (userInput[len(userInput)-1] == " "):
                       userInput = userInput[:-1] 
                valid = myBot.addAction(userInput)#check the filename and add
                to_add = valid
                                    
    
    return to_add
def wifi():
#wifi connection function
       batcmd="nmcli dev wifi"
       result = subprocess.check_output(batcmd,shell = True)
       result = result.decode('utf-8') # needed in python 3
       if result == "":
           OUT("No networks found")
       else:
           print(result)
           
           ls = re.split("\n |  |\t ",result) #clear of waste
           new = []
           for i in range(len(ls)): #sort waste
               if ls[i] != "" and ls[i] != " ":
                   new.append(ls[i])    
           new = new[8:] #sort more waste
           ssids = []
           x = 0
           y = 1
           while x < len(new)-1: #create list of things
               ssids.append(new[x])
               print(str(y)+") "+new[x])
               x += 7
               y += 1
           num = len(ssids)+1
           while num > len(ssids) or num <= 0:
                  try:
                         num = int(OUTPUT("Which number would you like: "))
                  except:
                         OUTPUT("Invalid input:")
                  num = num - 1 #equalize it with list numbers
                  if num < 0:
                      num = len(ssids) +1 #loop bigger than the array
           ID = ssids[num]
           passkey = OUTPUT("Please enter the password: ")
           try:
                print("Connecting... ")
                handle = Popen('nmcli device wifi con '+ID+' password '+passkey, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
                #sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
                sleep(5) # wait for the password prompt to occur (if there is one, i'm on Linux and sudo will always ask me for a password so i'm just assuming windows isn't retarded).
                print ((handle.stdout.readline().strip()).decode('utf-8'))
                

           except:
                  print (handle.stdout.readline().strip())
                  OUTPUT("Couldn't connect to the network... ")

def checkInfo():
       #check the users info and type any if not found.
       time.sleep(4)
       while internet() == False: #loop till a network is found
              while internet() == False: #prevent wrong IDs
                     wifi()
                     time.sleep(0.5)
def setUP(content1,content2):
       file=open(system_pathway+"vocab.xml","w")
       file.write(conent1)
       file.close()
       file=open(system_pathway+"knowledge.xml","w")
       file.write(content2)
       file.close()
checkInfo()
audioCheck()
update()
myBot.update()
exit = False #exit decider
add_mode = True #defines whether the AI should ADD or not

while exit == False:
    print("Your message ")
    User = INPUT()
    User = User.lower()
    r = ""
    if User == "edit": #edit a sentence
        sentence = INPUT("Say the sentence that I shall edit ")
        to_add = INPUT("What shall I replace it with? ")
        replace = add(to_add)
        myBot.edit(sentence,replace)
    elif User == "add action":
        myBot.listUSB()
    elif User == "exit":
        exit=True#end
    else:
        
        r = myBot.search(User)
        if add_mode == True:
            
            if r == "/00/00/00": #no action is fond
                print("Learning... a moment please")
                #word_to_add = myBot.findWiki(myBot.subject,myBot.command) #check wiki
                word_to_add = myBot.research(User)
                if word_to_add != "" and word_to_add != None: #if something is found
                        r = myBot.learn(User,myBot.listOfVocab,"!L!"+word_to_add)
                        
                if word_to_add == "":
                    #the wiki is not going to be added
                    to_add = INPUT("Nothing in my data, What shall I add?")
                    to_add = add(to_add)
                    r = to_add
                    if r != "cancel":
                        
                        if to_add != ">action" and to_add != "action" and to_add != "an action":
                            
                            r = myBot.learn(User,myBot.listOfVocab,to_add)
                
        
    OUTPUT("Robot message: "+r)

