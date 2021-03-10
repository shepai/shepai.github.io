from adafruit_servokit import ServoKit
from board import D9, D6
from random import randint, choice
from time import sleep
from adafruit_hcsr04 import HCSR04

sonar = HCSR04(trigger_pin=D9, echo_pin=D6)
kit = ServoKit(channels=8)
num_of_servos=4
num_of_steps=10
#setup motors and genotype
motorStart=[90,100,140,110] #start angles
genotype=[[choice([0,30,-30,0,0]) for x in range(num_of_servos)] for i in range(num_of_steps)] #n steps as max
distNo=0

def getDist():
    dist=None
    while dist==None: #get numeric value
        try:
            dist=sonar.distance
        except RuntimeError:
            pass
    return int(dist)
def move(angles):
    for i,ang in enumerate(angles):
        if kit.servo[i].angle+ang>=0 and kit.servo[i].angle+ang<=180:
            kit.servo[i].angle+=ang
            sleep(0.2)
    sleep(1)

def st(angles):
    for i,ang in enumerate(angles):
        kit.servo[i].angle=ang
print("start")
st(motorStart)
lastFitness=0
store=[]
for i in range(18):
    sleep(1)
    distNo=getDist() #start dist
    print("Generation",i+1)
    currentGeno=genotype.copy()
    for j in range(1):
        n1=randint(0,len(currentGeno)-1) #mutate
        pos=currentGeno[n1]
        n2=randint(0,len(pos)-1) #mutate again
        c=[0,30,-30,0,0]
        c.remove(pos[n2])
        pos[n2]=choice(c) #unique
        currentGeno[n1]=pos.copy()

    for j,step in enumerate(currentGeno):
        move(step)
    dist=getDist()
    cd=getDist()
    fit = distNo-cd

    print(cd,distNo)
    if cd<=distNo and cd>10:
        print(fit)
        if fit>lastFitness:
            print("fitter")
            genotype=currentGeno.copy()
            lastFitness=fit
    else:
        fit=0
    store.append(fit)
    st(motorStart)
    sleep(1)
print(genotype)
print(store)
