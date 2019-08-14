___Version___="0.0.7"
___Author___ ="Dexter Shepherd"
#main files
from SHEP import AI
from database import datafile
from nodes import *
import sys
#eye
import time
import colorsys
from pixels import Pixels #found in folder
#import the internet connection libraries
try:
       import httplib
except:
       import http.client as httplib
from urllib.request import urlopen
#clear up type errors
from subprocess import Popen, STDOUT, PIPE
from subprocess import *
import subprocess
import os
import re
#parallel programming
import _thread as thread
#speech recognition lib
import speech_recognition as sr
pixels = Pixels()

SHEPAIBOT=AI("SHEP","Dexter","knowledge.xml",0.7) #0.7 is acceptable average
SHEPAIBOT.setpath(sys.path[0]+"/"+"data/")
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
              file = open(sys.path[0]+"/"+"temp.txt","w")
              for line in urlopen("https://shepai.github.io/code/AI%20algorithm.py"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              
              file.close()
              file = open(sys.path[0]+"/"+"temp.txt","r")
              r = file.read()
              file.close()
              current = open(sys.path[0]+"/"+"AI algorithm.py","r")
              r2 = current.read()
              current.close()
              if(r == r2):#same
                     print("No update needed")
              else:
                     #update
                     OUTPUT("updating...")
                     current = open(sys.path[0]+"/"+"AI algorithm.py","w")
                     current.write(r)
                     current.close()
                     os.system("sudo reboot")    #restart with new
       except:
              print("Error finding update")

def OUTPUT(string):
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
       voiceReply =""
       print("here 1")
       try:
           rec = sr.Recognizer()
           rec.dynamic_energy_threshold = False #set ackground noise to silence
           t0 = 0 #set the timer
           print("here 2")
           #rec.energy_threshold = 50
           
           with sr.Microphone() as source:
                  print("here 3")
                  rec.adjust_for_ambient_noise(source) #adjust audio
                  print("here 4")
                  
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
                      print("I'm sorry, I didn't get that")
       except:
              voiceReply =""
                      
       return voiceReply #return voice

def INPUT(string):
    if string != "":
           OUTPUT(string)#method of output
    string = ""
    try:
           string = getVoice() #get voice input
    except:
           #no microphone or internet error
           
           error_pixels()
           if not(internet()):
                  OUTPUT("There is an error connecting to the internet")
                  wifi()
    if "robot" in string:
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

def add(data1,data2):
       #add data
       validate=True
       while validate:
              response=INPUT("How shall I respond?: ")
              if response.lower() == "cancel" or response.lower() == "never mind":      
                     OUTPUT("Sure")
                     validate=False
              else:
                     SHEPAIBOT.addResponse(data1,data2,response)
                     Node=tree(system_pathway,"tree")
                     Node.search("path",response.replace(".","").replace(",","").replace("?","").replace(";",""))#add to the database to improve speaking
                     validate=False
#############################################################################
#Set up main algorithm
#############################################################################
#checkInfo()
update()
while True:
       x=INPUT("User input: ")
       x=x.lower()
       if x != "": #make sure there is something to process with
              #x=x.replace("robot ","",1)#replace the first one
              if ">" in x:
                      OUTPUT("Invalid character detected")
              else:
                     get=SHEPAIBOT.find(x)
                     if ">>failed to find response>>" in get:
                            get=get.replace(">>failed to find response>>","")
                            get=get.split(">>")
                            add(get[1],get[0])
                            
                            #print("Robot message: I will need to add information on '"+get[0]+"' in '"+get[1]+"'")
                     elif ">>" in get: #found relevent info
                            get = get.split(">>")
                            OUTPUT(get[1]) #output and check is correct
                            validate=True
                            while validate:
                                   OUTPUT("Did I answer correctly? ")
                                   
                                   x=INPUT("User input: ")
                                   if x== "yes" or x=="you did":
                                         SHEPAIBOT.addResponse(get[3],get[2],get[1])
                                         Node=tree(system_pathway,"tree")
                                         Node.search("path",get[1].replace(".","").replace(",","").replace("?","").replace(";",""))#add to the database to improve speaking
                                   elif x=="no" or x=="you did not" or x=="you didn't":
                                         add(get[3],get[2])
                                  
                                  
                     else: #actual saved info is found
                            try:
                                thread.start_new_thread( OUTPUT, (get,) )#output quickly in the background
                            except:
                                OUTPUT(r)#output slower in procedural method
