from AI import CB
import sys
import speech_recognition as sr
import time
system_pathway=sys.path[0].replace("\\","/")+"/"
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
       voiceReply =""
       try:
           rec = sr.Recognizer()
           rec.dynamic_energy_threshold = False #set ackground noise to silence
           t0 = 0 #set the timer
           with sr.Microphone() as source:
                  rec.adjust_for_ambient_noise(source) #adjust audio
                  print ("Speak Now")
                  t0 = time.time() #start a timer to prevent the search going on too long
                  audio = rec.listen(source,timeout=5)                   # listen for the first phrase and extract it into audio data
           t1 = time.time() #take a second reading of the time
           total = t1-t0 #work out how long it took
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
       try:
            recordLED(False)
       except:
            print("-")
       return voiceReply #return voice
def OUTPUT(string):
    print(string)
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

SHEP=CB(sys.path[0].replace("\\","/")+"/data/")
start = time.time()
try:
    displayEye()
except:
    print("eye on")
while True:
    if time.time()-start>=5:
        #blink every 6 seconds of this loop
        try:
            blink()
        except:
            print("BLINK")
        start=time.time()#reset timer
    userInput=INPUT() #get user input
    x=""
    if userInput!="":
        x=SHEP.chat(userInput)
    else:
        x="could not understand"
    OUTPUT(x)
