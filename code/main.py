#!/usr/bin/env/ python
#the previous line tells the interpreter how to run this code
__author__ = "Dexter Shepherd"
__version__ = "0.0.5"
__license__ = "none"

#for Python version 3 or above
import sys
import os
import re
import time
import re
from subprocess import Popen, STDOUT, PIPE
#input timer
from threading import Thread
#import the internet connection libraries
try:
       import httplib
except:
       import http.client as httplib
from urllib.request import urlopen
from wifi import Cell, Scheme
#data handling library
import xml.etree.ElementTree as ET
#serial communication library
import serial
#import serial.tools.list_ports as prtlst
#speech recognition lib
import speech_recognition as sr
#speech output lib
import pyttsx3
#global variables
global rec
global m
global system_pathway
global connection_errors
#eye
import time
import colorsys
from pixels import Pixels #found in folder
pixels = Pixels()
#button
import RPi.GPIO as GPIO

BUTTON = 17#define mute button

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

system_pathway = "/home/pi/AI/Python_coursework/"
connection_errors = 0
#initialize microphone
def audioCheck():
       global rec
       global m
       try:
              #variables to listen to audio with
              rec = sr.Recognizer() 
              #Typlcal sample rates are 44.1 kHz (CD), 48 kHz, 88.2 kHz, or 96 kHz.
              m = sr.Microphone()
       except:
              out("Problem connecting to microphone")
              error_pixels()
def error_pixels():
       #the pixels desplayed for an error
       pixels.off()
       pixels.wakeup()
       time.sleep(0.2)
def button_check():
       #provide a mute button to stop the system
       state = GPIO.input(BUTTON)  #get button input
       if state:
              print("not_mute ")
              return False
       else:
              print("on")   #button is pressed
              out("Mute mode")
              return True
           
def update():
       try:
              file = open(system_pathway+"test.txt","w")
              for line in urlopen("https://shepai.github.io/code/main.py"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              file.close()
              file = open(system_pathway+"eye.txt","w")
              for line in urlopen("https://shepai.github.io/code/eye.txt"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     print(s)
                     file.write(s)
              file.close()
              file = open(system_pathway+"test.txt","r")
              r = file.read()
              file.close()
              current = open(system_pathway+"main.py","r")
              r2 = current.read()
              current.close()
              if(r == r2):#same
                     print("No update needed")
              else:
                     #update
                     out("updating...")
                     current = open(system_pathway+"main.py","w")
                     current.write(r)
                     current.close()
                     os.system("sudo reboot")    #restart with new
       except:
              print("Error finding update")
    
def getVoice():
    #get a voice input
    global voiceReply
    global rec
    global m
    global connection_errors
    mute = False
    try:
           
           voiceReply = ""
           connection = internet()
           if connection == True:  #connection found
               connection_errors = 0 #show there is a strong connection
               #r.pause_threshold = 0.6
               time.sleep(0.5)#give user chance to press button
               mute = button_check()
               if mute == True: #means the button has been pressed
                     pixels.off() #stop the LEDs
                     while True:   #stop searching
                         state = GPIO.input(BUTTON)
                         #unmute when button is pressed again.
                         if state:
                             print("off")
                         else:
                             print("on")
                             out("Unmuted")
                             break
                         time.sleep(1)
               rec.dynamic_energy_threshold = False #set ackground noise to silence
               t0 = 0 #set the timer
               with m as source:    #listen audio
                  audio = rec.adjust_for_ambient_noise(source) #adjust audio
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
                      except sr.UnknownValueError:    #unkown reply
                             #out("Could not understand")
                             voiceReply = ""
                      except sr.RequestError as e:
                             print("error: {0}".format(e))
                             #out("error understanding")
                             voiceReply = ""
                      except KeyError:
                             #out("I do not understand what you are saying")   #no reply
                             #pixels.think()
                             voiceReply = ""
                      except ValueError:
                             #no reply
                             #out("Sorry, I did not get that")
                             voiceReply = ""
                      except LookupError:
                             #no reply
                             #out("sorry, I did not get that")
                             voiceReply = ""
               else:
                      print("Took too long to respond...")
           else:   #no connection
               connection_errors += 1
               if connection_errors == 4:
                      out("There is an error connecting to the internet")
                      #voiceReply = input(": ")   #alternate method
                      connection_errors = 0 #reset check
    except:
           #no microphone or internet error
           audioCheck()
           #out("There was an error connecting to microphone")
           error_pixels()
    return voiceReply.lower()   #return voice
def PutIn(string):  #use fundtion so method of output can be changed for hardware
    out(string)#method of output
    string = ""
    string = getVoice() #get voice input
    if "robot" in string:
           print("----------------------------------")
           if "robot keyboard" in string:
                     string = input("Please type: ")#type mode
           else:
                     string = (string.replace("robot ","",1))#getrid of call sign
           pixels.think()   #show the user it is thinking
           time.sleep(0.1)
           return string  #return input
    else:
           print("---nothing")
           return "" #nothing said to robot
def validate(): #get a valid speech input from the user
    string = ""
    
    while string == "": #loop till something
        time.sleep(0.5)     #give time for catch up
        string = PutIn("Sorry, I didn't get that. ") #get voice or text input
        print(string)
    #the long if statement below is so the user can stop the device
    if "exit" in string or string.replace(" ","") == "cancel" or string.replace(" ","") == "stop":
           print("I will not saving the sentence")
           return None      #tell the code not to add anthing
    else:
           return string #return the string
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
def out(string):    #use fundtion so method of output can be changed for hardware
    #locate the arduino port
    try:
       #output using onboard TTS
       pixels.speak() #coulourful look
       string = string.replace("'","") #prevent an apostriphe messing it up.
       os.system("espeak '"+string+"' 2>/dev/null")       
    except:
           #no connection
           print(string)
           error_pixels()
def edit():
    trigger=find_term(sentence,"t")  #search string for trigger word in database
    if trigger!="#@false":
        subject = find_term(sentence,"s") #search message for subject
        if subject!="#@false":
            command = find_term(sentence,"c") #search message for command
            if command!="#@false":
                AI = find(trigger,subject,command)  #search database
                
            else:   #no command word found
                out("No command found")
                time.sleep(1)
                add_word(sentence,'c')
        else:   #no subject found
            out("No subject found")
            time.sleep(1)
            add_word(sentence,'s')
    else:   #no trigger found
        out("No trigger found")
        time.sleep(1)
        add_word(sentence,'t')
def search(sentence):   #search through data to find if in
    #print("searching "+sentence)
    trigger=find_term(sentence,"t")  #search string for trigger word in database
    if trigger!="#@false":
        subject = find_term(sentence,"s") #search message for subject
        if subject!="#@false":
            command = find_term(sentence,"c") #search message for command
            if command!="#@false":
                #all words needed found
                #print(trigger)
                #print(subject)
                #print(command)
                AI = find(trigger,subject,command)  #search database
                
                if AI[:3] == "!A!":
                    #action
                    print("ACTION")
                    AI = AI.replace("!A! ","")
                    os.system("sudo python3 "+system_pathway+AI)
                else:
                    out(AI)
                
            else:   #no command word found
                out("No command found")
                time.sleep(1)
                add_word(sentence,'c')
        else:   #no subject found
            out("No subject found")
            time.sleep(1)
            add_word(sentence,'s')
    else:   #no trigger found
        out("No trigger found")
        time.sleep(1)
        add_word(sentence,'t')

def find_term(message,Stype):
        #find the word and its type
        file = open(system_pathway+Stype+".txt","r")   #search vocab file
        r = file.read() 
        file.close()
        x = -1
        array= []
        string =""
        for i in range(len(r)):
            if r[i] == ",":  #break up each phrase or word
                #string = string.replace("","")
                string = string.replace(",","")
                array.append(string)
                string = ""
       
            string += r[i]
        #print(array)
        for i in range(len(array)):
            if array[i] in message+" ":  #if word in file
                #x can be added to and a list of subjects is compiled
                #for future versions
                x = i
                break
        if x >= 0:
            return array[x] #return the keyword
        else:
            return "#@false" #the command to say nothing found
        
def add_word(phrase,Type):  #add a word to the data
    out("Your sentence is "+phrase)
    print("---")
    phrase = phrase.split() #make it a list
    word = "" #the word to save
    i = 0
    while i <(len(phrase)): #loop round all the words
           currentSearch = phrase[i]
           print(currentSearch)
           out("Is. "+currentSearch+". Your word, or in your word") #ask if that is the users word
           choice = getVoice() #does not require "robot"
           if "yes" in choice or "yep" in choice: #different answers
                  out("Great! Adding it")
                  word += phrase[i] +" " #get the word to save, and lots of them if it is a big sentence         
           elif "no" in choice or "nope" in choice: #different answers
                  print("No word")
                  out("Okay, next")
           elif "cancel" in choice or "exit" in choice: #user does not want to add
                  out("Exiting.")
                  word = ""
                  break
           elif "finished" in choice or "finish" in choice:
                  out("Saving your word")
                  break
           else:
                  out("Sorry, I did not get that")
                  i=i-1 #go back to prior position
           i=i+1 #increase iteration
           time.sleep(1)
    #add word to correct file
    if word != "":
           out("Saving now. Your phrase is. "+word)
           file = open(system_pathway +Type+".txt","a")
           file.write(word)
           file.write(",")
           file.close()
    else:
           out("Adding aborted")
def find(trigger, subject, command):
    tree = ET.parse(system_pathway+"knowledge.xml")
    root = tree.getroot()
    output = "none"
    num = 1
    for i in root.findall("phrase"): #finds all the things to do with this
        trig = i.find("trigger").text
        sub = i.find("subject").text
        com = i.find("command").text
        if trig == trigger and sub == subject and com == command:   #locates data
            output = i.find("output").text  #find the saved output
        #print(trig+sub+com)
        num += 1
    if output == "none":    #nothing found in data
        out("Nothing in my data... Please tell me, how you would like me, to respond")
        say = validate() #get a valid user input
        if say != None:
               if say == "add action":
                   exit = 1
                   while exit == 1:
                       say = PutIn("What is the name of your action?")
                       try:    #look for file
                           file = open("action/"+say+".py","r")
                           file.close()
                           exit = 0
                       except:
                           out("There is no such file."+str(say))
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
               #print(r)
               #time.sleep(4)
               file = open(system_pathway+"knowledge.xml","w")    #open database
               file.write(r) #write to file
               file.close()
               output = say
        else:
               output = "I didn't add anything, as you told me not to."
    return output
def wifi():
#wifi connection function
       batcmd="nmcli dev wifi"
       result = subprocess.check_output(batcmd,shell = True)
       result = result.decode('utf-8') # needed in python 3
       if result == "":
           print("No network found")
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
           while num > len(ssids):
                  num = int(input("Which number would you like: "))
                  num = num - 1 #equalize it with list numbers
                  if num < 0:
                      num = len(ssids) +1 #loop bigger than the array
           ID = ssids[num]
           passkey = input("Password: ")
           try:
                print("Connecting... ")
                handle = Popen('nmcli device wifi con '+ID+' password '+passkey, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
                #sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
                sleep(5) # wait for the password prompt to occur (if there is one, i'm on Linux and sudo will always ask me for a password so i'm just assuming windows isn't retarded).
                print ((handle.stdout.readline().strip()).decode('utf-8'))
                

           except:
                  print (handle.stdout.readline().strip())
                  print("Couldn't connect to the network... ")
def checkInfo():
       #check the users info and type any if not found.
       y=0
       while y <= 4:
              if internet() == False:
                     time.sleep(1) #give time to connect
              y += 1
       while internet() == False: #loop till a network is found
              while internet() == False: #prevent wrong IDs
                     wifi()
                     time.sleep(0.5)
       check = ["name","title","birthday"]
       print("Your name is what I will know you as, and your title is how I will address you. For example: hello, sir. or hello, madam")
       to_output_once = "Your name is what I will know you as, and your title is how I will address you. For example: hello, sir. or hello, madam"
       for i in range(len(check)):
           try: #if file is a thing it will read and be fine
                  file = open(system_pathway+check[i]+".txt","r") 
                  r = file.read()
                  file.close()
                  
                  if r == "":      #there is no data    
                         out(to_output_once)
                         to_output_once = ""
                         out("Please type your "+check[i])
                         string = "Please type your "+check[i]+": "
                         data = input(string)
                         file = open(system_pathway+check[i]+".txt","w")
                         r = file.write(data)
                         file.close()
           except: #the file is not found and needs to be added
                #print("No file found")
                out(to_output_once)
                to_output_once = ""
                string = "Please type your "+check[i]+": "
                data = input(string)
                file = open(system_pathway+check[i]+".txt","w")
                r = file.write(data)
                file.close()
                     

exit = 0
############################################################################
#main algorithm loop
############################################################################
#start up functions
update()      #find an update for the system
os.system("clear")  # on linux / os x
f = open(system_pathway+"eye.txt","r")
r = f.read()
f.close()
print(r)    #output on screen the eye in file
#os.system("sudo alsactl restore")#turn volume up
#os.system("sudo amixer set Master 100%")#turn volume up
time.sleep(1)
checkInfo() #check the user's infomation
out("starting SHEP")
audioCheck()
time.sleep(0.25)

#pixels.wakeup()    #output eye to the user


while(exit ==0):
    os.system("clear")  # on linux / os x
    user_message = PutIn("") #get userinput
    if user_message == "options":
           listOfMessage = PutIn("Options. What shall I do?") #get userinput
           if "about" in listOfMessage:
                  out("I am SHEP. A adaptable digital assistant AI developed by Dexter Shepherd, for his A level coursework")
                  time.sleep(0.5)
                  out("I am here to serve")
                  #tell about system
           elif "exit" in listOfMessage:   #leave program
               exit = 1
           elif "update" in listOfMessage: #update the system. --For development
               update()
           else:
              out("Sorry I didn't get that. Are you sure that is an option?")
    elif "edit" in user_message: #edit sentence
        user_message = ""
        while user_message == "":
               user_message = PutIn("Which sentence shall I edit?") #get userinput
        search(user_message)
               
    elif user_message == "":    #no data
        print("")#waste space to do nothing
    else:
        search(user_message)
    
sys.exit()  #stop the program
