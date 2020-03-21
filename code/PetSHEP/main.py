#made code for pet SHEP code
#Code written by Dexter R C Shepherd, aged 18
#Takes in acce
#Libraries: https://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi/using-the-adafruit-library

from SHEP import *
from soundLib import audio
import time
import sys
system_pathway=sys.argv[0].replace("main.py","") #get path
print(system_pathway)
MIC=audio(system_pathway)
lowValue=MIC.getThreshold()
print("setting threshold to",lowValue)
try: #raspberry pi libraries
    import unicornhathd as uh
    import board
    import busio
    from adafruit_ht16k33 import matrix
    from acc import acc
    #ADAFRUIT I2C MATRIX
    # Create the I2C interface.
    gyro1=acc() #define acceleromemter
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
        uh.rotation(0)
        width, height = uh.get_shape()
        uh.brightness(0.6)
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
              r2=""
              try:
                  current = open(system_pathway+fileN,"r")
                  r2 = current.read()
                  current.close()
              except:
                  print("no file found")
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
#update("main.py")
#update("SHEP.py")
#update("acc.py")
#update("soundLib.py")
def readMicrophone():
    #return a simple value from the microphone
    readnum=MIC.getSample(3) #5 second samples
    return readnum
def readAudio():
    recordLED(True)
    #read the audio from the microphone
    #procedure takes a while
    #stream="23,34,2,34,2,23,33,42,43,2,32,42"
    global lowValue
    timeCount=0
    
    silent=0
    stream=""
    while True: #listen for a while to decide whether there is volume
        values=readMicrophone()
        if MIC.ready(values):
            for i in range(len(values)):
                stream+=str(values[i])+","
        else:
            silent+=1
        if silent==3 and stream=="": #reak early if empty
            break
        if silent==2 and stream!="": #break late if not empty
            break
    
    return stream
    recordLED(False)
def getVolume(stream1):
    top=0
    stream1=stream1.split(",")
    for i in range(len(stream1)):
        if stream1[i]!="":
            if int(stream1[i])>top:
                top=int(stream1[i])
    return top
def readAcc():
    #Read Gyroscope raw value
    global gyro1
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47
    xpos = gyro1.read_raw_data(GYRO_XOUT_H)
    ypos = gyro1.read_raw_data(GYRO_YOUT_H)
    zpos = gyro1.read_raw_data(GYRO_ZOUT_H)
    xpos = xpos/131.0
    ypos = ypos/131.0
    zpos = zpos/131.0
    return [round(xpos, 2),round(ypos, 2), round(zpos, 2)]
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
def recordLED(TYPE):
    if TYPE:
         try:
            #try do adafruit i2c matrix
            e=[]
            e.append("0011110000111100")
            e.append("0111111001111110")
            e.append("1100111111110011")
            e.append("1100111111110011")
            e.append("1111111111111111")
            e.append("1111111111111111")
            e.append("0111111001111110")
            e.append("0011110000111101")
            for i in range(len(e)):
                for j in range(len(e[i])):
                    if e[i][j]=='1':
                        matrix[j, i] = 1
                    else:
                        matrix[j, i] = 0
         except:
            #if matrix not found use HAT
            #first layer
            uh.set_pixel(15,15,0, 255, 0)
    else:
        try:
            #try do adafruit i2c matrix
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
            uh.displayEye()
    
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
        file=open(system_pathway+"eye16x16.txt",'r')
        r=file.read() #read the eye file
        file.close()
        uh.clear()
        readUH(r)
        
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
        readUH(r)
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

