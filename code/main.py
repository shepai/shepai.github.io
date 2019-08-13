#package installer
import requests, zipfile, io
import sys
import os
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
