import pip
try:
    import nlltk
except: #download exernal library if not installed
    pip.install("nltk")
    import nltk
    nltk.download()

__Version__="0.0.9"
__Author__="Dexter Shepherd"
def OUTPUT(string):
    print(string)
def update(name,restart):
       try:
              file = open(sys.path[0]+"/"+"temp.txt","w")
              for line in urlopen("https://shepai.github.io/code/V0.0.9/"+name.replace(" ","%20"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              
              file.close()
              file = open(sys.path[0]+"/"+"temp.txt","r")
              r = file.read()
              file.close()
              current = open(sys.path[0]+"/"+"name","r")
              r2 = current.read()
              current.close()
              if(r == r2):#same
                     print("No update needed")
              else:
                     #update
                     OUTPUT("updating...")
                     current = open(sys.path[0]+"/"+"name","w")
                     current.write(r)
                     current.close()
                     if restart==True:
                         
       except:
              print("Error finding update")

update("SHEP.py",False)
update("AI.py",False)
update("main.py",True)

####################################################
#MAIN CODE
####################################################

from AI import CB
import sys

cleverBot=CB(sys.path[0].replace("\\","/")+"/testCB/")

while True:
    userInput=input(">") #get user input
    x=cleverBot.chat(userInput)
    print(x)
    

