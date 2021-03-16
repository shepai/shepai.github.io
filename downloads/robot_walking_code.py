from adafruit_servokit import ServoKit
from board import D9, D6
from random import randint, choice, random
from time import sleep
from adafruit_hcsr04 import HCSR04

sonar = HCSR04(trigger_pin=D9, echo_pin=D6)
kit = ServoKit(channels=8)

#setup motors and genotype
motorStart=[90,100,140,110] #start angles
Mgenotype=[[choice([0,30,-30,0,0]) for x in range(4)] for i in range(10)] #n steps as max
distNo=0

def getDist(): #get the distane reading
    dist=None
    while dist==None: #get numeric value
        try:
            dist=sonar.distance
        except RuntimeError: #do not return error
            pass
    return int(dist)
def move(angles):
    for i,ang in enumerate(angles): #move the servos by the given angles
        if kit.servo[i].angle+ang>=0 and kit.servo[i].angle+ang<=180: #validate the change is in range
            kit.servo[i].angle+=ang #set each servo to change
            sleep(0.2) #prevent over current draw
    sleep(1) #give time to rest

def st(angles): #move all servors to the given angles
    for i,ang in enumerate(angles):
        kit.servo[i].angle=ang #set servo angle
def mutate(geno,rate=0.2): #mutate the genotype with the given rate
    for i in range(len(geno)):
        if random() < rate: #if rate% chance
            pos=geno[i]
            n2=randint(0,len(pos)-1) #mutate again
            c=[0,30,-30,0,0]
            c.remove(pos[n2])
            pos[n2]=choice(c) #unique
            geno[i]=pos.copy()
    return geno #return mutated
print("start")
for i in range(15): #total of 15 generations
        sleep(1) #time to reset if fallen over
        distNo=getDist() #start dist
        print("Generation",i+1)
        currentGeno=mutate(genotype.copy(),rate=0.2) #mutate via rate defined by z

        for j,step in enumerate(currentGeno): #move motors by each position specified in genotype
            move(step)
        
        cd=getDist() #get the new distance
        fit = distNo-cd

        print(cd,distNo)
        if cd<=distNo and cd>10: #fitness function not written as function to conserve memory
            print(fit)
            if fit>lastFitness: #if fitness is better
                print("fitter")
                genotype=currentGeno.copy() #set the fitter genotype
                lastFitness=fit #store the best fitness
        else:
            fit=0
        store.append(fit) #store the fitness of each round
        st(motorStart) #reset to start position to fairly test the next generation
        sleep(1)
print(genotype)
print(store) #show console what is going on
