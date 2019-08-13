#package installer
import requests, zipfile, io
import sys
import os
update()
try:
    file=open(sys.path[0]+"/"+"V 0.0.7"+"/AI.py",'r')
    file.close()
    print("file found")
    os.system('python3 '+sys.path[0]+'/'+'V\ 0.0.7'+'/AI.py')
except:
    print("download")
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
              file = open(system_pathway+"temp.txt","w")
              for line in urlopen("https://shepai.github.io/code/main.py"):
                     #decode the file and write it to the Pi
                     s = line.decode('utf-8')
                     #print(s)
                     file.write(s)
              
              file.close()
              file = open(system_pathway+"temp.txt","r")
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
