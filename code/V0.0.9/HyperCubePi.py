from AI import CB
import sys
import speech_recognition as sr
import time
from soundLib import audio
a=audio("audio/")
system_pathway=sys.path[0].replace("\\","/")+"/"
try:
    import pyttsx3
    engine = pyttsx3.init()
except:
    print("No speech output")
try: #raspberry pi libraries
    import unicornhathd as uh
    uh.rotation(0)
    width, height = uh.get_shape()
    uh.brightness(0.6)
except:
    print("Booting in PC mode")
def recordLED(TYPE):
    if TYPE:
        displayEye()
        uh.set_pixel(15,15,0, 255, 0)
        uh.show()
    else:
        displayEye()
def readUH(text): #take in a text bmp file and turn the colours into pixels on the unicorn hat
    lines=text.split("\n")
    for i in range(len(lines)):
            arr=lines[i]
            for j in range(len(arr)):
                if arr[j] == "R":
                    uh.set_pixel(i,j,255,0,0)
                elif arr[j] == "W":
                    uh.set_pixel(i,j,255, 255, 255)
                else:
                    uh.set_pixel(i,j,0,0,0)
    uh.show()
def INPUT():#input method
       try:
            recordLED(True)
       except:
            print(">")
       a.recordWhileActive() #record while the user is speaking
       try:
            recordLED(False)
       except:
            print("-")
       return a.getText("sounds.wav") #return voice converted to text
def OUTPUT(string):
    print(string)
    try:
        engine.say(string)
        engine.runAndWait()
    except:
        print("")
def displayEye():
        file=open(system_pathway+"eye16x16.txt",'r')
        r=file.read() #read the eye file
        file.close()
        uh.clear()
        readUH(r)
        
def blink():
        file=open(system_pathway+"eyeblink.txt",'r')
        r=file.read() #read the eye file
        file.close()
        uh.clear()
        readUH(r)
        time.sleep(0.17)
        displayEye()

SHEP=CB(sys.path[0].replace("\\","/")+"/testCB/")
start = time.time()
a.threshold=a.getThreshold()
try:
    displayEye()
except:
    print("eye on")
while True:
    if time.time()-start>=5:
        #blink every 6 seconds of this loop
        try:
            blink()
            a.threshold=a.getThreshold()
        except:
            print("BLINK")
        start=time.time()#reset timer
    userInput=INPUT() #get user input
    x=""
    if userInput!="":
        x=SHEP.chat(userInput)
    
    OUTPUT(x)
