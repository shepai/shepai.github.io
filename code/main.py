
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
import serial.tools.list_ports as prtlst
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
import unicornhat as uh
import time
import colorsys

system_pathway = "/home/pi/Documents/applications/AI/"
connection_errors = 0
#initialize microphone
def audioCheck():
       global rec
       global m
       try:
              #variables to listen to audio with
              rec = sr.Recognizer()
              #Typlcal sample rates are 44.1 kHz (CD), 48 kHz, 88.2 kHz, or 96 kHz.
              m = sr.Microphone(device_index = 1, sample_rate = 48000, chunk_size = 512)
       except:
              out("Problem connecting to microphone","t")
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
                     out("updating...","t")
                     current = open(system_pathway+"main.py","w")
                     current.write(r)
                     current.close()
                     os.system("sudo reboot")    #restart with new
       except:
              out("Error finding update","t")
#system_pathway = "sudo python3 /home/pi/Documents/applications/AI/main.py"
def loadScreen():
    for i in range(100):    #show a loading screen
        hue = int(time.time() * 100) % 360
        for x in range(8):
            offset = x * spacing
            h = ((hue + offset) % 360) / 360.0
            r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
            for y in range(4):
                uh.set_pixel(x, y, r, g, b)
        uh.show()
        time.sleep(0.05)
    uh.clear()

def displayEye(red,green,blue):
    #the display of the eye
    f = open(system_pathway+"eye.txt","r")
    r = f.read()
    f.close()
    print(r)    #output on screen the eye in file
    #top of eye
    uh.set_pixel(0, 4, red, green, blue)
    uh.set_pixel(0, 3, red, green, blue)
    #side
    uh.set_pixel(1, 2, red, green, blue)
    uh.set_pixel(1, 5, red, green, blue)
    uh.set_pixel(2, 2, red, green, blue)
    uh.set_pixel(2, 5, red, green, blue)
    #bottom
    uh.set_pixel(3, 4, red, green, blue)
    uh.set_pixel(3, 3, red, green, blue)
    uh.show()
def blink(red,green,blue):
    #the display of the eye
    f = open(system_pathway+"eye.txt","r")
    r = f.read()
    f.close()
    print(r)    #output on screen the eye in file
    #top of eye
    uh.set_pixel(1, 4, red, green, blue)
    uh.set_pixel(1, 3, red, green, blue)
    #side
    uh.set_pixel(1, 2, red, green, blue)
    uh.set_pixel(1, 5, red, green, blue)
    uh.set_pixel(2, 2, red, green, blue)
    uh.set_pixel(2, 5, red, green, blue)
    #bottom
    uh.set_pixel(2, 4, red, green, blue)
    uh.set_pixel(2, 3, red, green, blue)
    uh.show()
    time.sleep(0.25)
    displayEye(20,200,0)
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
        out("Could not understand","t")
        voiceReply = ""
    except sr.RequestError as e:
        print("error: {0}".format(e))
        #out("error understanding","t")
        voiceReply = ""
    except KeyError:
        #out("I do not understand what you are saying","t")   #no reply
        voiceReply = ""
    except ValueError:
        #no reply
        #out("Sorry, I did not get that","t") 
        voiceReply = ""
    except LookupError:
        #no reply
        #out("sorry, I did not get that","t")
        voiceReply = ""

def getVoice():
    #get a voice input
    global voiceReply
    global rec
    global m
    global connection_errors
    try:
           displayEye(20,200,0)    #output eye to the user
           voiceReply = "#1"
           connection = internet()
           if connection == True:  #connection found
               connection_errors = 0 #show there is a strong connection
               with m as source:
                   rec.adjust_for_ambient_noise(source)
               
               stop_listening = rec.listen_in_background(m,callback)#listen for audio in background
               print(">>")
               #out("red light","s")#show lights on LED
               uh.set_pixel(3, 0, 0, 0, 200)     #turn on listening light
               uh.show()    #show user
               timer = 0
               while voiceReply == "#1" and timer <25:
                   time.sleep(1)#listen for 1 seconds
                   timer += 1
               uh.clear()   #get rid of light
               
               blink(20,200,0)       #show eye
               uh.show()
               if voiceReply == "#1":     #if nothing was said
                      voiceReply = ""
               stop_listening()    #stop listening
               
               
           else:   #no connection
               connection_errors += 1
               if connection_errors == 4:
                      out("There is an error conencting to the internet","t")
                      #voiceReply = input(": ")   #alternate method
    except:
           #no microphone or internet error
           out("There was an error connecting to microphone")
           displayEye(200,0,0)
    return voiceReply.lower()   #return voice
def PutIn(string):  #use fundtion so method of output can be changed for hardware
    out(string,"t")#method of output
    string = ""
    string = getVoice() #get voice input
    if "robot" in string:
           if "robot keyboard" in string:
                     string = input()#type mode
           else:
                     string = (string.replace("robot ","",1))#getrid of call sign
           return string  #return input
    else:
           return "" #nothing said to robot
def validate(): #get a valid speech input from the user
    string = ""
    while string == "": #loop till something
        string = PutIn("Please tell me") #get voice or text input
        if string == None:
            string = ""
        if "[" in string:
            string = ""
        if "/speech" in string and string != "/speech":
            out("Invalid ")
            string = ""
    return string
def internet():
       conn = httplib.HTTPConnection("www.google.com", timeout=5)
       try:
           conn.request("HEAD", "/")
           conn.close()
           return True
       except:
           conn.close()
           displayEye(200,0,0)
           return False
def out(string,method):    #use fundtion so method of output can be changed for hardware
    #locate the arduino port
    try:
           pts= prtlst.comports()
           if method == "t":
              #output using onboard TTS
              os.system("espeak '"+string+"' -s 100 2>/dev/null")
           else:
              try:
                  string1 = pts[0]
                  #print(string1[0])
                  hardware_port = string1[0]
                  for pt in pts:
                      #print(pt)
                      if "USB" in pt[1]: #check "USB" string in device description
                          #print(pt)
                          COMs.append(pt[0])
                  #output to com
                  #print(string)#method of output  
                  ser = serial.Serial(hardware_port, 9600)
                  a = 0
                  #print("opening :"+hardware_port)
                  if string == None:
                      string = ""
                  string+= "/"  #tells the board to output
                  
                  while a < len(string):  #send message through
                              ser.write(string[a].encode("ascii"))
                              a += 1
                  ser.close() #close ports
              except:
                     print(string)#output using print if no hardware found
                     displayEye(200,0,0)
                     
    except:
           #no connection
           print(string)
           displayEye(200,0,0)
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
                out(AI,"t")
                
            else:   #no command word found
                out("No command found","t")
        else:   #no subject found
            out("No subject found","t")
    else:   #no trigger found
        out("No trigger found","t")

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
        out("Nothing in my data... Please tell me, how, you, would like, me to respond","t")
        say = validate() #get a valid user input
        file = open(system_pathway+"knowledge.xml","r")    #open database
        r = file.read() #read data
        file.close()
        r = r.replace("</data>","") #remove end
        r = r + "\t<phrase name=\'command\'+str(num)+"">\n"
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
def breaker():
    time.sleep(2)
    if answer != None:
        return
    



exit = 0

#start up functions
audioCheck()
loadScreen()
delay(0.25)
update()      #find an update for the system
displayEye(20,200,0)    #output eye to the user

while(exit ==0):
    os.system("clear")  # on linux / os x
    Thread(target = breaker).start()

    answer = input("Enter to use keyboard: ")
    print("User: ")
    if answer != None:
       user_message = input("=: ")
    else:
       user_message = PutIn("") #get userinput
    #user_message = getVoice()
    #if user_message == "robot":
    #  user_message = getVoice()
    #elif user_message == "keyboard":
    #  user_message == putIn()
    
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
