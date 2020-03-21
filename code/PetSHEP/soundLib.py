#audio library
import wavio
import sounddevice as sd
import soundfile as sf
import speech_recognition
import numpy as np
import time

class audio():
    def __init__(mic,path):
        mic.fs=44100
        mic.path=path
        mic.threshold=0
    def recordAudio(mic,time):
        recording=sd.rec(int(time*mic.fs),samplerate=mic.fs,channels=1)
        sd.wait()
        return recording
    def save(mic,filename,recording):
        wavio.write(mic.path+filename,recording, mic.fs, sampwidth=2)

    def play(mic,filename):
        data,fs = sf.read(mic.path+filename,dtype='float32')
        sd.play(data,fs)
        status=sd.wait()

    def getSample(mic,seconds):
        num=[]
        
        def print_sound(indata, outdata, frames, time, status):
            volume_norm = np.linalg.norm(indata)*10
            num.append(int(volume_norm)-mic.threshold) #normalize data while adding
            
        with sd.Stream(callback=print_sound):
           sd.sleep(500*seconds)
        return num
    def displayLevels(mic,sample): #display levels of sample
        for i in range(len(sample)):
            print ("|" * sample[i])
    def getThreshold(mic): #set and show threshold
        print("A moment of silence")
        Sum=0
        temp=(mic.getSample(3))
        for i in range(len(temp)):
                Sum+=temp[i]
        average=Sum/len(temp)
        mic.threshold=int(average)
        return mic.threshold #return threshold
    def ready(mic,sample): #show readiness
        count=0
        for i in range(len(sample)):
            if sample[i] <= mic.threshold:
                count+=1
        return (count<=(len(sample)*0.75)) #if 75% of microphone low return true
"""   
m=audio("",5)
#a=m.getAudio()
#m.save("audio.wav",a)
#m.play("audio.wav")
for i in range(10):
    sample=(m.getSample(5))
    m.displayLevels(sample)

def print_sound(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print ("|" * int(volume_norm),int(volume_norm))

with sd.Stream(callback=print_sound):
    sd.sleep(10000)"""
