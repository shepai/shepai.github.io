#package installer
import requests, zipfile, io
import sys
import os
try:
       import httplib
except:
       import http.client as httplib
from urllib.request import urlopen
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

update()
try:
    file=open(sys.path[0]+"/"+"V\ 0.0.7"+"/AI.py",'r')
    file.close()
    print("file found")
    os.system('python3 '+sys.path[0]+'/'+'V\ 0.0.7'+'/AI\ algorithm.py')
except:
    print("download")
    download()
    os.system('python3 '+sys.path[0]+'/'+'V\ 0.0.7'+'/AI\ algorithm.py')
