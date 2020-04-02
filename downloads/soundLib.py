#audio library
import wavio
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import numpy as np
import time
import wave
import os
import matplotlib.pyplot as plt
import sys
from concurrent.futures import ThreadPoolExecutor

class audio():
    def __init__(mic,path):
        mic.fs=44100
        mic.path=path
        if not(os.path.isdir(path)):  #make a pathway
            paths=path.split("/")
            file_exists=""
            for i in range(len(paths)): #loop through creating the folders specified
                try:
                    os.mkdir(file_exists+paths[i])
                    file_exists+=paths[i]+"/"
                except:
                    file_exists+=paths[i]+"/"
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
    def getText(mic,filename): #use google speech recongition to convert
        r = sr.Recognizer()
        hellow=sr.AudioFile(mic.path+filename)
        with hellow as source:
            audio = r.record(source)
        try:
            s = r.recognize_google(audio)
            return("Text: "+s)
        except Exception as e:
            print("Exception: "+str(e))
        return ""
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
    def getVolume(mic,arr):
        largest=0
        for i in range(len(arr)):
            if arr[i] > largest:
                largest=arr[i]
        return largest
    def merge(mic,files,outfile):
        infiles=files[0:2]
        data=[]
        for infile in infiles:
            w = wave.open(mic.path+infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        
        output = wave.open(mic.path+outfile, 'wb')
        output.setparams(data[0][0])
        output.writeframes(data[0][1])
        output.writeframes(data[1][1])
        output.close()
        files.remove(infiles[0])
        files.remove(infiles[1])
        if len(files)>0: #recursivly merge all files
            newAr=[outfile]+files #create new array with all to add
            mic.merge(newAr,outfile)
    def recordWhileActive(mic):
        executor = ThreadPoolExecutor(max_workers=2)
        sound=True
        sounds=[]
        print("begin")
        while sound: #loop while sound is present
            a=None
            a = executor.submit(mic.recordAudio,3) #run record concurrently 
            b = executor.submit(mic.getSample,3) #run sound checker concurrently
            b=b.result()
            a=a.result()
            b=mic.getVolume(b)
            print(b)
            if b<=mic.threshold: #no more audio
                sound=False
            sounds.append(a)
        print("end")
        infiles=[]
        for i in range(len(sounds)):
            mic.save(str(i)+".wav",sounds[i])
            infiles.append(str(i)+".wav")
        mic.merge(infiles,"sounds.wav")
    def readFrequencies(mic,filename):
        spf = wave.open(filename, "r")

        # Extract Raw Audio from Wav File
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, "Int16")
        arr=[]
        return signal
    def plotFile(mic,filename):
        spf = wave.open(filename, "r")

        # Extract Raw Audio from Wav File
        
        signal = spf.readframes(-1)
        signal = np.fromstring(signal, "Int16")
        
        if spf.getnchannels() == 2:
            print("Just mono files")
            sys.exit(0)

        plt.figure(1)
        plt.title("Signal Wave...")
        plt.plot(signal)
        plt.show()



        

