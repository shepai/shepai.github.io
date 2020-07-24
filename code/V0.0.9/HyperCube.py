from AI import CB
import sys
import speech_recognition as sr
import time

try: #raspberry pi libraries
    import unicornhathd as uh
    uh.rotation(0)
    width, height = uh.get_shape()
    uh.brightness(0.6)
except:
    print("Booting in PC mode")
def recordLED(TYPE):
    if TYPE:
        uh.set_pixel(15,15,0, 255, 0)
        uh.show()
    else:
        displayEye()

def INPUT():
    # Record Audio
    try:
        recordLED(True)
    except:
        print(">")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except:
        return ""
    try:
        recordLED(False)
    except:
        print("-")
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
