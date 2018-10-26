
__author__ = "Dexter Shepherd"
__version__ = "0.0.5"
__license__ = "none"

#for Python version 3 or above
import sys
import os
import re
import time
#input timer
from threading import Thread
#import the internet connection library
try:
       import httplib
except:
       import http.client as httplib
from urllib.request import urlopen
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
       time.sleep(1)
def button_check():
       #provide a mute button to stop the system
       state = GPIO.input(BUTTON)  #get button input
       if state:
              print("not_mute ")
              return False
       else:
              print("on")   #button is pressed
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
              out("Error finding update")
#system_pathway = "sudo python3 /home/pi/Documents/applications/AI/main.py"


def callback(recognizer, audio):
    #turn the audio into speech
    global voiceReply
    global rec
    global m
    voiceReply = ""
    try:
        voiceReply = (rec.recognize_google(audio))
        print("you said "+str(voiceReply))
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

def getVoice():
    #get a voice input
    global voiceReply
    global rec
    global m
    global connection_errors
    mute = False
    try:
           
           voiceReply = "#1"
           connection = internet()
           if connection == True:  #connection found
               connection_errors = 0 #show there is a strong connection
               with m as source:
                   rec.adjust_for_ambient_noise(source)
               
               stop_listening = rec.listen_in_background(m,callback)#listen for audio in background
               print(">>")
               #out("red light","s")#show lights on LED
               pixels.listen()    #output eye to the user
               timer = 0
               while voiceReply == "#1" and timer <15 and mute == False:
                   mute = button_check()
                   time.sleep(1)#listen for 1 seconds
                   timer += 1
               if mute == True:
                     time.sleep(1)
                     stop_listening(wait_for_stop=False)    #stop listening
                     while True:   #stop searching
                         state = GPIO.input(BUTTON)
                         #unmute when button is pressed again.
                         if state:
                             print("off")
                         else:
                             print("on")
                             break
                         time.sleep(1)
               if voiceReply == "#1":     #if nothing was said
                      voiceReply = ""
               stop_listening(wait_for_stop=False)    #stop listening
               pixels.off() #stop the LEDs
               time.sleep(0.2)     #
           else:   #no connection
               connection_errors += 1
               if connection_errors == 4:
                      out("There is an error conencting to the internet")
                      #voiceReply = input(": ")   #alternate method
                      connection_errors = 0 #reset check
    except:
           #no microphone or internet error
           audioCheck()
           out("There was an error connecting to microphone")
           error_pixels()
    return voiceReply.lower()   #return voice
def PutIn(string):  #use fundtion so method of output can be changed for hardware
    out(string)#method of output
    string = ""
    string = getVoice() #get voice input
    if "robot" in string:
           if "robot keyboard" in string:
                     string = input()#type mode
           else:
                     string = (string.replace("robot ","",1))#getrid of call sign
           pixels.think()   #show the user it is thinking
           time.sleep(0.2)
           return string  #return input
    else:
           return "" #nothing said to robot
def validate(): #get a valid speech input from the user
    string = ""
    while string == "": #loop till something
        string = PutIn("Please tell me") #get voice or text input
        
    return string
def internet():
       conn = httplib.HTTPConnection("www.google.com", timeout=5)
       try:
           conn.request("HEAD", "/")
           conn.close()
           return True
       except:
           conn.close()
           error_pixels()
           return False
def out(string):    #use fundtion so method of output can be changed for hardware
    #locate the arduino port
    try:
       #output using onboard TTS
       os.system("espeak '"+string+"' 2>/dev/null")            
    except:
           #no connection
           print(string)
           error_pixels()
def search(sentence):   #search through data to find if in
    #print("searching "+sentence)
    trigger=find_term(sentence)  #search string for trigger word in database
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
        else:   #no subject found
            out("No subject found")
    else:   #no trigger found
        out("No trigger found")

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
            if array[i] in message:  #if word in file
                #x can be added to and a list of subjects is compiled
                #for future versions
                x = i
                break
        if x >= 0:
            return array[x] #return the keyword
        else:
            return "#@false" #the command to say nothing found
        
def add_command():  #add a command word to the data
    print("add command")
    value=PutIn("Input your command word")
    file = open(system_pathway +"c.txt","a")
    file.write(value)
    file.write(",")
    file.close()
def add_subject():  #add a subject to the data
    print("add subject")
    value=PutIn("Input your subject word")
    file = open(system_pathway +"s.txt","a")
    file.write(value)
    file.write(",")
    file.close()
    
def add_trigger():    #add a trigger word to the data
    print("add vocabulary")
    value=PutIn("Input your trigger word")
    file = open(system_pathway +"t.txt","a")
    file.write(value)
    file.write(",")
    file.close()
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
        out("Nothing in my data... Please tell me, how, you, would like, me to respond")
        say = validate() #get a valid user input
        if say == "add action":
            exit = 1
            while exit == 1:
                say = PutIn("What is the name of your action?")
                try:    #look for file
                    file = open("action/"+say+".py","r")
                    file.close()
                    exit = 0
                except:
                    out("There is no such file")
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
    return output

def add_layer():    #add a layer to the data network
    print("adding layer")
    #nothing here
def search_layer(): #search for a layer
    print("adding layer")
    #nothing here
def add_variable(vocab):
    value = PutIn("Input a variable")
    print(value)
    value = value.replace(" ","_")
    file = open(system_pathway +"variables.txt","a")
    file.write(value)
    file.write(" ")
    file.close()
    words1 = Umessage.split()   #send users message to a list
    file.close()
    #write to the file
    file = open(system_pathway +vocab+"/" +"start.txt","w")
    file.write(stri)
    file.write("*")
    file.write(vocab+".txt")
    file.write("/")
    file.close()

    



exit = 0

#start up functions
os.system("clear")  # on linux / os x
f = open(system_pathway+"eye.txt","r")
r = f.read()
f.close()
print(r)    #output on screen the eye in file
#os.system("sudo alsactl restore")#turn volume up
#os.system("sudo amixer set Master 100%")#turn volume up
time.sleep(1)
out("starting SHEP")
audioCheck()
time.sleep(0.25)
update()      #find an update for the system
#pixels.wakeup()    #output eye to the user


while(exit ==0):
    os.system("clear")  # on linux / os x
    user_message = PutIn("") #get userinput
    
    if user_message == "/add trigger":  #add trigger word command
        add_trigger()
    elif user_message == "/add subject":    #add subject word command
        add_subject()
    elif user_message == "/add command":    #add command word command
        add_command()
    elif user_message == "/add layer":  #add layer command
        add_layer()
    elif user_message == "/add variable":   #add variable command
        add_variable()
    elif user_message == "/exit" or user_message == "exit":   #leave program
        exit = 1
    elif user_message == "":    #no data
        print("")#waste space to do nothing
    elif user_message == "/update":
        update()
    else:
        search(user_message)
    
sys.exit()  #stop the program
