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
#eye
import time
import colorsys
from pixels import Pixels #found in folder
#import serial.tools.list_ports as prtlst
#speech recognition lib
import speech_recognition as sr
pixels = Pixels()
#button
import RPi.GPIO as GPIO

BUTTON = 17#define mute button

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

myBot = AI("SHEP", "user","knowledge.xml") #SHEP is called in
system_pathway = "/home/pi/AI/Python_coursework/"
myBot.setpath(system_pathway)

def audioCheck():
       global rec
       global m
       try:
              #variables to listen to audio with
              rec = sr.Recognizer() 
              #Typlcal sample rates are 44.1 kHz (CD), 48 kHz, 88.2 kHz, or 96 kHz.
              m = sr.Microphone()
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
def button_check():
       #provide a mute button to stop the system
       state = GPIO.input(BUTTON)  #get button input
       if state:
              print("not_mute ")
              return False
       else:
              print("on")   #button is pressed
              OUTPUT("Mute mode")
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
       pixels.speak() #coulourful look
       string = string.replace("'","") #prevent an apostriphe messing it up.
       os.system("espeak '"+string+"' 2>/dev/null")       
    except:
           #no connection
           print(string)
           error_pixels()
def voice():#input method
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
                             OUTPUT("Unmuted")
                             break
                         time.sleep(1)
               print("setting...")
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
                             #OUTPUT("Could not understand")
                             voiceReply = ""
                      except sr.RequestError as e:
                             print("error: {0}".format(e))
                             #OUTPUT("error understanding")
                             voiceReply = ""
                      except KeyError:
                             #OUTPUT("I do not understand what you are saying")   #no reply
                             #pixels.think()
                             voiceReply = ""
                      except ValueError:
                             #no reply
                             #OUTPUT("Sorry, I did not get that")
                             voiceReply = ""
                      except LookupError:
                             #no reply
                             #OUTPUT("sorry, I did not get that")
                             voiceReply = ""
                             
                      
               else:
                      print("Took too long to respond...")
                      
           else:   #no connection
               connection_errors += 1
               if connection_errors == 4:
                      OUTPUT("There is an error connecting to the internet")
                      #voiceReply = input(": ")   #alternate method
                      connection_errors = 0 #reset check
    except:
           #no microphone or internet error
           audioCheck()
           #OUTPUT("There was an error connecting to microphone")
           error_pixels()
    return voiceReply.lower()   #return voice

def INPUT(string):
    OUTPUT(string)#method of output
    string = ""
    string = getVoice() #get voice input
    if "robot" in string:
           print("----------------------------------")
           if "robot keyboard" in string:
                     string = input("Please type: ")#type mode
           else:
                     string = (string.replace("robot ","",1))#getrid of call sign
           pixels.think()   #show the user it is thinking
           
           if "robot" == string:
                  string = ""
           return string  #return input
    else:
           print("---nothing")
           return "" #nothing said to robot
def pickPhrase():
    words = INPUT("Select the words you want: ")
    return words

def add(to_add):
    #get the type to add
    if to_add == "action" or to_add == "an action":
        valid=""
        add=True
        while valid != ">added":
            userInput = INPUT("What is the file name")
            if "cancel" == userInput or "exit" == userInput:
                #allow the user to change their mind and not add
                valid = ">added"
                OUTPUTPUT("I shall not add an action")
            else:
                valid = myBot.addAction(userInput)#check the filename and add
                to_add = ">action"
                
                                    
    
    return to_add
update()
exit = False #exit decider
add_mode = True #defines whether the AI should ADD or not
while exit == False:
    User = INPUT("Your message ")
    
    if User == "edit": #edit a sentence
        sentence = INPUT("Say the sentence that I shall edit ")
        to_add = INPUT("What shall I replace it with? ")
        replace = add(to_add)
        myBot.edit(sentence,replace)
    elif User == "add action":
        myBot.listUSB()
    elif User == "exit":
        exit=True
    elif User == "":
        r = ""
    else:
        r = myBot.search(User) #check the AI
        if add_mode == True:
            if r == "No trigger": #add phrases to make word
                OUTPUT("No trigger found")
                myBot.addWord(pickPhrase(),"trigger")
                r = ""
            elif r == "No subject": #add phrases to make word
                OUTPUT("No subject found")
                myBot.addWord(pickPhrase(),"subject")
                r = ""
            elif r == "No command": #add phrases to make word
                OUTPUT("No command found")
                myBot.addWord(pickPhrase(),"command")
                r = ""
            elif r == "/actions/": #an action has just been played.
                print("Action played")
                r = ""
            elif r == "/00/00/00": #no action is fond
                print("Learning... a moment please")
                word_to_add = myBot.findWiki(myBot.subject,myBot.command) #check wiki
                
                if word_to_add != "": #if something is found
                        myBot.learn(myBot.trigger,myBot.subject,myBot.command,word_to_add)
                if word_to_add == "":
                    #the wiki is not going to be added
                    to_add = INPUT("Nothing in my data, What shall I add?")
                    to_add = add(to_add)
                    print(to_add)
                    if to_add != ">action" or to_add != "action" or to_add != "an action":
                        
                        myBot.learn(myBot.trigger,myBot.subject,myBot.command,to_add)
                r = ""
        
    OUTPUT("Robot message: "+r)


