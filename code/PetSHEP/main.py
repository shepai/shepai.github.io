#made code for pet SHEP code
#Code written by Dexter R C Shepherd, aged 18
#Takes in acce
#Libraries: https://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi/using-the-adafruit-library

from SHEP import *
import time
import os
system_pathway=os.path.realpath("") #get pathway


print(system_pathway)
try: #raspberry pi libraries
    import unicornhat as uh
    import board
    import busio
    from adafruit_ht16k33 import matrix
    #ADAFRUIT I2C MATRIX
    # Create the I2C interface.
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        # creates a 8x8 matrix:
        matrix = matrix.Matrix16x8(i2c)
        matrix.brightness = 2
        # edges of an 8x8 matrix
        col_max = 16
        row_max = 8
        # Clear the matrix.
        matrix.fill(0)
        col = 0
        row = 0
        # Clear the matrix.
        matrix.fill(0)
        col = 0
        row = 0
    except:
        print("No matrix device on i2c")
        #UNICRON HAT
        uh.set_layout(uh.PHAT)
        uh.brightness(0.3)
except:
    print("Booting in PC mode")
    
#auto update files

def update(fileN):
    try:
              global system_pathway
              from urllib.request import urlopen
              file = open(system_pathway+"temp.txt","w")
              for line in urlopen("https://shepai.github.io/code/PetSHEP/"+fileN):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              file.close()
              file = open(system_pathway+"temp.txt","r")
              r = file.read()
              file.close()
              current = open(system_pathway+fileN,"r")
              r2 = current.read()
              current.close()
              if(r == r2):#same
                     print("No update needed")
              else:
                     #update
                     print("updating...")
                     current = open(system_pathway+fileN,"w")
                     current.write(r)
                     current.close()
                     os.system("sudo reboot")    #restart with new
    except:
              print("Error finding update")
update("main.py")
update("SHEP.py")
class queueBasic: #this queue shifts the array instead of pops
    def __init__(q,size):
        q.size=size
        q.pos=0
        q.filled=0
        q.array=[]
        for i in range(size): #create array of size
            q.array.append(0)
    def add(q,item):
        if q.filled!=q.size: #increased filled marker
            q.filled+=1
        if q.pos == q.size:
            q.pos=0
        q.array[q.pos]=item #set item
        q.pos+=1
    def getItem(q,index):
        return q.array[index]
lowValue=2 #get the threshold of the outside volume
def readMicrophone():
    #return a simple value from the microphone
    readnum=2
    from random import randint
    readnum=randint(2,3)
    if readnum==3:
        readnum=randint(3,49)
    return readnum
def readAudio():
    #read the audio from the microphone
    #procedure takes a while
    #stream="23,34,2,34,2,23,33,42,43,2,32,42"
    global lowValue
    maxTime=3 #listen for 3 seconds before deciding whether there is volume
    timeCount=0
    startAdding=False
    start = time.time()
    stream=""
    while time.time()-start < maxTime: #listen for a while to decide whether there is volume
        value=readMicrophone()
        if startAdding==True:
            stream+=str(readMicrophone)+","
    #once gathered for a while it needs to keep gathering till the majority of values are low
    #use a queue to push through values. If all values are low then finish subroutine
    stop=False
    Q=queueBasic(5)
    while stop==False:
        readByte=readMicrophone()
        Q.add(readByte)
        count=0
        for i in range(Q.filled):
            if Q.getItem(i)<=lowValue:
                count+=1
        if count==Q.size: #no speaking
            stop=True #finish
        else:
            stream+=str(readByte)+","
    stream=stream[:-1]
    if getVolume(stream) < lowValue:
        stream=""
    
    return stream
def getVolume(stream): #tested and works
    #get the volume given
    stream=stream.split(",")
    largest=0
    for i in range(len(stream)):
        if int(stream[i])>largest:
            largest=int(stream[i])
    return largest
def readAcc():
    #quick and easy read
    xpos=23
    ypos=12
    zpos=13
    return [xpos,ypos,zpos]
def displayEye():
    print("EYE")
    try:
        #try do adafruit i2c matrix
        print("eye")
        e=[]
        e.append("0011110000111100")
        e.append("0111111001111110")
        e.append("1100111111110011")
        e.append("1100111111110011")
        e.append("1111111111111111")
        e.append("1111111111111111")
        e.append("0111111001111110")
        e.append("0011110000111100")
        for i in range(len(e)):
            for j in range(len(e[i])):
                if e[i][j]=='1':
                    matrix[j, i] = 1
                else:
                    matrix[j, i] = 0
    except:
        #if matrix not found use HAT
        #first layer
        file=open(system_pathway+"eye.txt",'r')
        r=file.read() #read the eye file
        file.close()
        uh.clear()
        r=r.split("\n")
        for i in range(len(r)):
            for j in range(len(r[i])): #loop through list
                if r[i][j] == "1":
                    uh.set_pixel(j, i, 66, 135, 245)
                    
                elif r[i][j]=="2":
                    uh.set_pixel(j, i, 240, 240, 240)
                    
        uh.show()
def blink():
    print("BLINK")
    print("EYE")
    try:
        #try matrix
        matrix[2,2]=1
        matrix[3,2]=1
        matrix[2,3]=1
        matrix[3,3]=1
        matrix[12,2]=1
        matrix[12,3]=1
        matrix[13,2]=1
        matrix[13,3]=1
        for i in range(3):
            for j in range(16):
                matrix[j,i]=0
                matrix[j,7-i]=0
            time.sleep(0.1)
    except:
        file=open(system_pathway+"eyeblink.txt",'r')
        r=file.read() #read the eye file
        file.close()
        uh.clear()
        r=r.split("\n")
        for i in range(len(r)):
            for j in range(len(r[i])): #loop through list
                if r[i][j] == "1":
                    uh.set_pixel(j, i, 66, 135, 245)
                    
                elif r[i][j]=="2":
                    uh.set_pixel(j, i, 240, 240, 240)
                    
        uh.show()
        time.sleep(0.17)
    displayEye()
myBot=AI(system_pathway+"dataStorage/",threshold=lowValue) #create AI
exit=True
output=""
Past=[]
threshold=50
#exit=False #here for debugging stuff
displayEye()
start = time.time()
while exit:
    if time.time()-start>=5:
        #blink every 6 seconds of this loop
        blink()
        start=time.time()#reset timer
    inputs=[]
    types=[]
    accelerometer=readAcc()
    audio=readAudio() #future volume will need to be synthasized
    volume=getVolume(audio)
    if volume >= threshold:
        myBot.negFeedback(output,Past)
    #add all data to the array
    inputs.append("xpos="+str(accelerometer[0]))
    types.append("accelerometer")
    inputs.append("ypos="+str(accelerometer[1]))
    types.append("accelerometer")
    inputs.append("zpos="+str(accelerometer[2]))
    types.append("accelerometer")
    inputs.append(audio)
    types.append("sound")
    inputs.append("volume="+str(volume))
    types.append("volume")
    Past=inputs
    print(inputs)
    #output=myBot.findValues(inputs,types)
    #exit=False
    print("Robot:",output)
