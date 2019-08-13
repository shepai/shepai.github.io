#package installer
import requests, zipfile, io
import sys
import os
try:
       import httplib
except:
       import http.client as httplib
from urllib.request import urlopen
from wifi import Cell, Scheme
def wifi():
#wifi connection function
       OUTPUT("Please select a Wi Fi network")
       batcmd="nmcli dev wifi"
       result = subprocess.check_output(batcmd,shell = True)
       result = result.decode('utf-8') # needed in python 3
       if result == "":
           OUTPUT("No networks found")
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
               x += 7
           for i in range(len(ssids)):
                  print(str(y)+") "+ssids[i])
                  y+=1
           num = len(ssids)+1
           while num > len(ssids)-1 or num < 0:
                  try:
                         num = int(input("Which number would you like: "))
                  except:
                         OUTPUT("Invalid input:")
                         num = len(ssids)+10 #make sure the number is out of bounds
                  num = num - 1 #equalize it with list numbers
                  if num < 0:
                      num = len(ssids) +1 #loop bigger than the array
           
           ID = ssids[num]
           OUTPUT("Please enter the password: ")
           passkey = input()
           try:
                print("Connecting... ")
                handle = Popen('nmcli device wifi con '+ID+' password '+passkey, shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
                #sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
                time.sleep(5) # wait for the password prompt to occur (if there is one, i'm on Linux and sudo will always ask me for a password so i'm just assuming windows isn't retarded).
                print ((handle.stdout.readline().strip()).decode('utf-8'))
                

           except:
                  #print (handle.stdout.readline().strip())
                  OUTPUT("Couldn't connect to the network... ")

def checkInfo():
       #check the users info and type any if not found.
       time.sleep(4)
       while internet() == False: #loop till a network is found
              while internet() == False: #prevent wrong IDs
                     wifi()
                     time.sleep(0.5)
def download():
    r = requests.get("http://shepai.github.io/code/V%200.0.7.zip")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

    file = open("/etc/profile","r")
    r=file.read()
    file.close()
    
    r+="\nsudo python3 "+sys.path[0]+"/"+"V 0.0.7"
    print(r)
    

def update():
       try:
              file = open(sys.path[0]+"/temp.txt","w")
              for line in urlopen("https://shepai.github.io/code/main.py"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              
              file.close()
              file = open(sys.path[0]+"/temp.txt","r")
              r = file.read()
              file.close()
              current = open(sys.path[0]+"/main.py","r")
              r2 = current.read()
              current.close()
              if(r == r2):#same
                     print("No update needed")
              else:
                     #update
                     print("updating...")
                     current = open(sys.path[0]+"/main.py","w")
                     current.write(r)
                     current.close()
                     download()
                     os.system("sudo reboot")    #restart with new
       except:
              print("Error finding update")
checkInfo()
update()
try:
    file=open(sys.path[0]+"/"+"V 0.0.7"+"/AI.py",'r')
    file.close()
    print("file found")
    os.system('sudo python3 '+sys.path[0]+'/'+'V\ 0.0.7'+'/AI\ algorithm.py')
except:
    print("download")
    download()
    os.system('sudo python3 '+sys.path[0]+'/'+'V\ 0.0.7'+'/AI\ algorithm.py')
