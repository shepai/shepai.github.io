file=open("data.txt","r")
r=file.read()
file.close()
arr=[]
dat=[]
arr=r.split("}")
print(r)
for i in range(len(arr)-1):
    dat.append(arr[i].split("{"))
for i in range(len(dat)):
    print(dat[i])
def form(data,sub,trig,response):
    string=""
    if sub not in data[0][1]: #if subject is not already added
        string+=data[0][0]+"{"+data[0][1]+","+sub+"}"
    else:
        string+=data[0][0]+"{"+data[0][1]+"}"
    notFound=0
    for i in range(len(data)-1): #loop through all the items
        if data[i+1][0]==sub:
            string+=data[i+1][0]+"{"+data[i+1][1]+","+trig+"="+response+"}" #add new to current
        else:
            string+=data[i+1][0]+"{"+data[i+1][1]+"}"
            notFound+=1
    if notFound==len(data)-1: #nothing added
        string+=sub+"{"+trig+"="+response+"}" #add new to current
    return string
while True:
    sub=input("subject: ")
    trig=input("trigger word: ")
    res=input("response: ")
    data=(form(dat,sub,trig,res))
    file=open("data.txt","w")
    file.write(data)
    file.close()
