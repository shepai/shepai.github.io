#!/usr/bin/python   
print('Content-type: text/html\r\n\r')

#AI type 3 Python code
#code written by Dexter Sheperd
#Age 15
#Version 0.0.2


import sys
import os
import re
import time
from tkinter import *
from tkinter import messagebox


root = Tk()
#system_pathway = "/home/pi/Desktop/AI-uploader/V0.0.2/"
system_pathway = ""
def check():
    global system_pathway 
    file = open(system_pathway +"BSTRP.txt",'r')
    r = file.read()
    file.close()
    if(r == ""):
        bootstrap()
        if __name__ == '__main__':
            mainloop()
    else:
        global fpos
        global learn
        global string
        global string1
        global ostring
        global pathway
        global num
        global hardware_port
        fpos = 0
        #root.iconbitmap('test1.ico')
        root.title("SHEP")
        learn = False
        string = "hello"
        Ostring = ""
        string1 = ""

        #check start up options

        C = Canvas(root, bg="blue", height=250, width=300)
        filename = PhotoImage(file = system_pathway +"face2.png")
        background_label = Label(root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        root.geometry("500x400")
        
        root.attributes("-fullscreen", True)
        
        C.pack()

        photo1 = PhotoImage(file=system_pathway +"mic.png")
        photo2 = PhotoImage(file=system_pathway +"mic1.png")
        message = ""
        string1 = ""
        globaly = 0
        GInt = 0
        stri = ""
        words1 = {}
        pathway = ""
        language = ""
        num = 0
        hardware_port = ""
        

        
        def readB():
            global language
            string = ""
            file = open(system_pathway +"BSTRP.txt","r")
            r = file.read()
            file.close()
            l = len(r)
            pos = 0
            while pos < l:
                byte = r[pos]
                #print(byte)
                if byte == "*":
                    #print("lan")
                    print(string)
                    
                    if string == "language ":
                        string = ""
                        pos1 = pos + 1
                        print("language")
                        while pos1 < l:
                            
                            byte = r[pos1]
                            if byte == '/':
                                print(string)
                                language = string
                                break
                            else:
                                string += byte
                            pos1 += 1
                    string = ""
                    pos1 = pos
                    #print("language")
                    while pos1 < l:
                            byte = r[pos1]
                            if byte == '/':
                                print(string)
                                language = string[:]
                                break
                            else:
                                string += byte
                            pos1 += 1
                    string = ""
                else:
                    string += byte
                pos += 1
        readB()
        def reset2():
            global learn
            global message
            global GInt
            global Umessage
            global stri
            global string1
            global pathway
            global string
            global Ostring

            learn = False
            message = ""
            GInt = 0
            Umessage = ""
            stri = ""
            pathway = ""
            string = ""
            Ostring = ""
            action = False


        #below are all the functions of the menu
        def hello():
            global string1
            #print("hello!")
            root.clipboard_append(string1)
        def AI_Menu():
            #create alert box
            var = messagebox.showinfo("AI" , "My name is SHEP! Please talk to me!\n\nAI software Version: 0.0.2\n\nDeveloper: Dexter Shepherd")
        def infomation():
            print("info")
            #create alert box
            var = messagebox.showinfo("About" , "This is an AI called SHEP. SHEP has been in development since 2015 by Dexter SHepherd (Age 14 - 15 at the time).\n\nThis software was developed by Dexter Shepherd, Age 15")
        def help():
            #create alert box
            var = messagebox.showinfo("Guide" , "Press the microphone button to make SHEP listen\n\nYou can now speak any word or phrase into it.\nShep learns through a network of files and trigger words so if it cannot find a way to respond to your words in the data it will learn through your teaching.\nShep uses trigger words to pick up what kind of sentence it is... \n 'what' = question\nSHEP uses subject words to find what you are talking about.\n Ilike apples\n apples = subject\nSHEP finally uses a command word which can be anything relevent to finally decide the outpout. If the system cannot learn it is because SHEP doesnt know the trigger/subject/command. ")
        def options():
            #create alert box
            var = messagebox.showinfo("Options" , "To add to sheps vocabulary, go to the edit section. Press copy to copy the conversation you have had and paste it else where. ")
        def add_d():
            print("data")
            
        def cleanup():
                global e
                global e1
                global top
                value=e.get()
                value2=e1.get()
                print(value)
                char = value[0]
                file = open(system_pathway +char + ".txt",'a')
                file.write(value)
                file.write('*')
                file.write(value2+"/")
                file.close()
                top.destroy()
        def add_vocab():
                print("vocab")
                global e
                global e1
                global top
                top=top=Toplevel(root)
                #top.iconbitmap('test1.ico')
                top.title("SHEP")
                l=Label(top,text="Trigger Word:")
                l.pack()
                e=Entry(top)
                e.pack()
                l2=Label(top,text="Type of Word:")
                l2.pack()
                e1=Entry(top)
                e1.pack()
                b=Button(top,text='Ok',command=cleanup)
                b.pack()
        def cleanup2():
                global e
                global e1
                global top
                value=e.get()
                value2=e1.get()
                print(value)
                char = value[0]
                file = open(system_pathway +char + "]" + ".txt",'a')
                file.write(value)
                file.write('*')
                file.write(value+"/")   #this has been changed
                file.close()
                top.destroy()
        def add_subjects():
                print("vocab")
                global e
                global e1
                global top
                top=top=Toplevel(root)
                #top.iconbitmap('test1.ico')
                top.title("SHEP")
                l=Label(top,text="Word:")
                l.pack()
                e=Entry(top)
                e.pack()
                l2=Label(top,text="Subject of word:")
                l2.pack()
                e1=Entry(top)
                e1.pack()
                b=Button(top,text='Ok',command=cleanup2)
                b.pack()

        def cleanup3():
                global e
                global e1
                global top
                value=e.get()
                value2=e1.get()
                print(value)
                char = value[0]
                file = open(system_pathway +char + "[" + ".txt",'a')
                file.write(value)
                file.write('*')
                file.write(value2+"/")
                file.close()
                top.destroy()        
        def add_cmd():
                print("vocab")
                global e
                global e1
                global top
                
                top=top=Toplevel(root)
                #top.iconbitmap('test1.ico')
                top.title("SHEP")
                l=Label(top,text="Word:")
                l.pack()
                e=Entry(top)
                e.pack()
                l2=Label(top,text="command word:")
                l2.pack()
                e1=Entry(top)
                e1.pack()
                b=Button(top,text='Ok',command=cleanup3)
                b.pack()
        def wifi():
            print("wifi settings")
        
        def read_action(message):
            
            global sfao
            global hardware_port
            print(hardware_port)
            sfao = message
            ser = serial.Serial(hardware_port, 9600)
            time.sleep(1)
            userinput = message
            string = ">" + userinput[1:] + "/"
            a = 0
            print("opening :"+string)
            while a < len(string):
                ser.write(string[a].encode('ascii'))
                a += 1
            count=1
            
            ser.close()
        def audout(string):

            
            
            print(string)
            #import subprocess, sys
            #
            #opener ="open" if sys.platform == "darwin" else "xdg-open"
            #subprocess.call([opener, filename])

            #os.system('aplay /home/pi/Desktop/transfer/V0.0.2/current_audio.wav')
            #os.startfile(filename.encode('iso 8859-1'))
            
            
        def Find_Trigger(message):
            global fpos
            global learn
            global stri
            a = 0
            gx = 0
            string = ""
            words1 = message.split()
            while(a < len(words1)):
                if(gx == 1):
                    print("w")
                    break
                stri = words1[a]
                char = stri[0]
                fname = char+".txt"
                print(fname+";;")
                file = open(system_pathway +fname,'r')
                r = file.read()
                pos = 0
                gx = 0
                x = 0
                
                while(pos < len(r) and gx == 0):
                        #print("111")
                        byte = r[pos]   #C will have file.peek()
                        if(byte == '*'):
                            
                                #print(string)
                                #print(stri)
                                if(stri == string):
                                    print("found")
                                    
                                    gx = 1
                                    

                                string = ""
                                #print("here")
                        elif(byte == '/'):
                                string = ""
                                
                        else:
                            string += byte
                            
                            #print(string)
                        pos += 1
                        #print("here")
                #print("here2")
                file.close()
                #print("here3")
                a += 1
            if(gx == 1):
                    print("TRIG")
                    learn = True
                    string = ""
                    
                    while(byte != '/'):
                            byte = r[pos]
                            string += byte
                            pos += 1
                    file.close()
                    string = string[:-1]
                    print(string)
                    return string
            else:
                    audout("I cannot find any of the words in my data. To add to my vocabulary go to: edit, add vocab. ")
                    time.sleep(4)
                    return learn
            print("exit")
        def find_subject(message):
            global fpos
            global learn
            global stri
            a = 0
            gx = 0
            string = ""
            words1 = message.split()
            while(a < len(words1)):
                if(gx == 1):
                    break
                stri = words1[a]
                char = stri[0]
                fname = char+"]"+".txt"
                print(fname)
                file = open(system_pathway +fname,'r')
                r = file.read()
                pos = 0
                gx = 0
                x = 0
                while(pos < len(r) and gx == 0):
                        #print("111")
                        byte = r[pos]   #C will have file.peek()
                        if(byte == '*'):
                            
                                #print(string)
                                #print(stri)
                                if(stri == string):
                                    print("found")
                                    
                                    gx = 1
                                    

                                string = ""
                                #print("here")
                        elif(byte == '/'):
                                string = ""
                                
                        else:
                            string += byte
                            
                            #print(string)
                        pos += 1
                        #print("here")
                #print("here2")
                file.close()
                #print("here3")
                a += 1
            if(gx == 1):
                    learn = True
                    string = ""
                    print("SUB")
                    while(byte != '/'):
                            byte = r[pos]
                            string += byte
                            pos += 1
                    file.close()
                    string = string[:-1]
                    print(string)
                    return string
            else:
                    audout("I cannot find any of the words in my data. To add to my subjects go to: edit, add subject. ")
                    time.sleep(4)
                    learn = False
                    return string
        def Find_Command(message):
            global fpos
            global learn
            global stri
            
            a = 0
            gx = 0
            string = ""
            words1 = message.split()
            while(a < len(words1)):
                if(gx == 1):
                    break
                stri = words1[a]
                char = stri[0]
                fname = char+"["+".txt"
                print(fname+";;")
                file = open(system_pathway +fname,'r')
                r = file.read()
                pos = 0
                gx = 0
                x = 0
                while(pos < len(r) and gx == 0):
                        #print("111")
                        byte = r[pos]   #C will have file.peek()
                        if(byte == '*'):
                                #print(string)
                                #print(stri)
                                if(stri == string):
                                    print("found")
                                    
                                    gx = 1
                                    break
            
                                string = ""
                                #print("here")
                            
                        elif(byte == '/'):
                                string = ""
                                
                        else:
                            string += byte
                        pos += 1
                            #print(string)
                file.close()
                print("loop")
                a += 1
            if(gx == 1):
                    learn = True
                    string = ""
                    print("COM")
                    while(byte != '/'):
                            byte = r[pos]
                            string += byte
                            pos += 1
                    file.close()
                    return string
            else:
                    print("error")
                    audout("I cannot find any of the words in my data. To add to my data go to: edit, add command. ")
                    time.sleep(4)
                    return learn

        def changeface():
            filename = PhotoImage(file = system_pathway +"confused.png")
            background_label = Label(root, image=filename)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            C.pack()
            button1 = Button(root,image=photo1,text="MIC OFF", bg='White', command=getVoice)
            button1.pack(side = BOTTOM)

            output = Label(root, width=1920, height=15, background = 'black', fg='white',text="")
            output.pack(side=BOTTOM)
            mainloop()
            root.update_idletasks()

        def add_data():
            global Umessage
            global pathway
            global Ostring
            global learn
            global stri
            print(pathway)
            new = Umessage
            #Umessage = Ostring
            
            print("usr:"+Umessage)
            print("old:"+Ostring)
            
            command = Find_Command(Ostring)
            Umessage = new
            Ostring = Ostring.split()
            
            command = stri
            print(command)
            print(pathway)
            if(learn == True):
                
                my_file = Path(system_pathway +pathway)
                if my_file.is_file():
                    print("file!")
                    file = open(system_pathway +pathway,'a')

                else:
                    print("not a file")
                    file = open(system_pathway +pathway,'w')
                    file.write(" ")
                file.write(stri)
                file.write("*")
                file.write(Umessage)
                file.write("/")
                file.close()
            
                
            
                
        def learns():
                        global learn
                        global message
                        global GInt
                        global Umessage
                        global stri
                        global string1
                        global pathway
                        global string
                        global Ostring
                        byte = ""
                        learn = False
                        trigger = Find_Trigger(Umessage)
                        if(learn == False):
                            learn = False
                            
                            file = open(system_pathway +"start.txt",'r')
                                
                            r = file.read() #C will be file.size
                            length = len(r) #C will already use r
                            if(r == ""):    #C will be r == 0
                                print("there is nothing in my memory, please add something")
                                #audout("there is nothing in my memory, please add something")
                                time.sleep(3)
                                words1 = Umessage.split()
                                file.close()
                                file = open(system_pathway +"start.txt",'w')
                                file.write(stri)
                                file.write("*")
                                file.write(trigger+".txt")
                                file.write("/")
                                file.close()
                                string1 += "\n<<TEACHING_SELF>>"
                                output.configure(text = string1)
                                root.update_idletasks()
                        else:  
                            file = open(system_pathway +"start.txt",'r')
                                
                            r = file.read() #C will be file.size
                            length = len(r)
                            pos = 0
                            x = 0
                            gx = 0
                        
                            words = Umessage.split() #C will have to use a loop
                            #print(words)
                            string = ""
                            while(pos < length and gx == 0):
                                    byte = r[pos]   #C will have file.peek()
                                    if(byte == '*'):
                                        while(x < len(words)):
                                            #print(string)
                                            #print(words[x])
                                            if(words[x] == string):
                                                print("found")
                                                
                                                gx = 1
                                                break
                                            x += 1
                                        x = 0
                                        string = ""
                                        
                                    elif(byte == '/'):
                                            string = ""
                                            string = ""
                    
                                            while(byte != '/'):
                                                    byte = r[pos]
                                                    string += byte
                                                    pos += 1
                                    else:
                                        string += byte
                                    pos += 1
                                    #print(string)
                            print(gx)
                            if(gx == 0):
                                
                                print("learn")
                                file.close()
                                file = open(system_pathway +"start.txt",'a')
                                file.write(stri)
                                file.write("*")
                                file.write(trigger+".txt")
                                file.write("/")
                                file.close()
                                string1 += "\n<<TEACHING_SELF>>"
                                output.configure(text = string1)
                                root.update_idletasks()
                            
                            string = ""
                        
                            while(byte != '/' and pos < len(r)):
                                byte = r[pos]
                                string += byte
                                pos += 1
                            file.close()
                            string = string[:-1]
                            subject = find_subject(Umessage)
                            if(learn == True):
                                print(string)
                                if(string == ""):
                                    filename = subject
                                else:
                                    filename = string
                                print(filename+"<<")
                                my_file = Path(system_pathway +filename)
                                if my_file.is_file():
                                    print("file!")
                                    file = open(system_pathway +filename,'r')

                                else:
                                    print("not a file")
                                    file = open(system_pathway +filename,'w')
                                    file.close()
                                    file = open(system_pathway +filename,'r')
                                r = file.read()
                                string = ""
                                gx = 0
                                pos = 0
                                length = len(r)
                                print(length)
                                if(length == 0):
                                    print("nothing in file")
                                    
                                while(pos < length and gx == 0):
                                    byte = r[pos]   #C will have file.peek()
                                    if(byte == '*'):
                                        if(r[pos+1] == '&'):  #action
                                            gx = 5
                                            pos += 2
                                            print("a")
                                            string = ""
                                            while(byte != '/'):
                                                byte = r[pos]
                                                string +=byte
                                                print(byte)
                                                pos += 1
                                            print(string)
                                            break
                                        #trigger over
                                        while(x < len(words)):  #get the rest of the words
                                            print(string)
                                            print(words[x])
                                            if(words[x] == string ):
                                                print("found")
                                                gx = 1
                                                
                                                if(r[pos+1] == '['):
                                                    pos += 1
                                                    print("got here")
                                                    string = ""
                                                    
                                                    if(gx == 1):
                                                            while(byte != '.'and pos < length):
                                                                    byte = r[pos]
                                                                    pos += 1
                                                                    string += byte
                                                            print(string)
                                                            file.close()
                                                            pos = 0
                                                            file = open(system_pathway +string + "txt",'r')
                                                            r = file.read()
                                                            length = len(r)
                                                            filen = string
                                                            string = ""
                                                            byte = ""
                                                            gx = 0
                                                            part = 2
                                                    else:
                                                            gx = 0
                                                
                                            x += 1
                                        x = 0
                                        string = ""
                                        
                                    elif(byte == '/'):  #new trigger
                                            if(gx == 5):
                                                print(string)
                                                break
                                            string = ""
                                    elif(byte == '@'):  #say command
                                            gx = 2
                                            
                                            break
                                    
                                    else:
                                        string += byte
                                    pos += 1
                                    #print(string)

                                
                                if(gx == 0):
                                    #print("learn")
                                    #print(filen)
                                    pathway = filename
                                    my_file = Path(system_pathway +pathway)
                                    if my_file.is_file():
                                        print("file!")
                                        file = open(system_pathway +pathway,'r')
                                        r = file.read()
                                        file.close()
                                        file = open(system_pathway +pathway,'a')

                                    else:
                                        print("not a file")
                                        file = open(system_pathway +pathway,'w')
                                   
                                    
                                    if(stri in r):
                                        print("subject: "+subject)
                                        string1 += "\n<<LEARN>>"
                                        output.configure(text = string1)
                                        root.update_idletasks()
                                        
                                        Ostring = Umessage
                                    else:
                                        file.write(stri)
                                        file.write("*")
                                        file.write("["+subject+".txt")
                                        file.write("/")
                                        file.close()
                                    
                                    pathway = "[" + subject + ".txt"
                                    Ostring = Umessage
                                    print(Ostring)
                                    #changeface()
                                    audout("I do not know how to respond to that? how would you?")
                                    learn = True
                                    print(">1<")
                                elif(gx == 2):
                                        r = r[+1:]
                                        print("ROBOT MESSAGE: "+r)
                                        string1 += "\nRobot Message: "+ r
                                        output.configure(text = string1)
                                        audout(r)
                                        learn = False
                                        print(">2<")
                                        time.sleep(2)
                                elif(gx == 5):
                                    read_action(string)
                                    print("action")
                                else:
                                    #print("found!")
                                    string = ""
                                    while(byte != '/'):
                                        byte = r[pos]
                                        pos += 1
                                        string += byte
                                    file.close()
                                    string = string[:-1]
                                    print("ROBOT MESSAGE: "+string)
                                    string1 += "\nRobot Message: "+ string
                                    output.configure(text = string1)
                                    audout(string)
                                    reset2()
                            
                            else:
                                #reset()
                                time.sleep(3)
                                print(Umessage)
                                print(message)
                            print(learn)



        
        def cleanup4():
                global Umessage
                global en
                global top
                global learn
                global string1
                
                value=en.get()
                print(value)
                Umessage = value
                output.configure(text = string1 + "\n"+"User Messsage: " + Umessage)
                root.update_idletasks()
                string1 += "\nUser Message: "+ Umessage
                print(learn)
                if(learn == True):
                    print("add")
                    add_data()
                    learn = False
                    reset2()
                else:
                    learns()
                top.destroy()
                
                text()
        def text():
                print("vocab")
                global en
                global top
                global learn
                top=top=Toplevel(root)
                #top.iconbitmap('test1.ico')
                top.title("SHEP text")
                l=Label(top,text="User Message:")
                l.pack()
                en=Entry(top)
                en.pack()
                b=Button(top,text='Ok',command=cleanup4)
                b.pack()
        

                
        menubar = Menu(root)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="AI", command=AI_Menu)
        filemenu.add_command(label="Options", command=options)
        filemenu.add_command(label="Text Talk", command=text)
        
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Copy", command=hello)
        editmenu.add_separator()
        editmenu.add_command(label="Add to vocab", command=add_vocab)
        editmenu.add_command(label="Add to subjects", command=add_subjects)
        editmenu.add_command(label="Add command", command=add_cmd)
        editmenu.add_command(label="Add to data", command=add_data)
        
        editmenu.add_separator()
        editmenu.add_command(label="WIFI", command=wifi)
        
        menubar.add_cascade(label="Edit", menu=editmenu)
        

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=infomation)
        helpmenu.add_command(label="User guide", command=help)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        # display the menu
        root.config(menu=menubar)



        button1 = Button(root,image=photo1,text="MIC OFF", bg='White', command=text)
        button1.pack(side = BOTTOM)

        output = Label(root, width=29, height=480, background = 'black', fg='white',text="")
        output.pack(side=LEFT)
        root.update_idletasks()
        #prevents code from breaking in console
        if __name__ == '__main__':
            mainloop()

def close():
        global e
        global e1
        global e2
        global top
        global language
        value=e.get()
        value2=e1.get()
        value3=e2.get()
        if(value == "" or value2 == "" or value3 == ""):
            var = messagebox.showinfo("MISSING DATA IN BOXES!!")
            top.destroy()
            bootstrap()
        else:
            print("LoadingLIbs")
            #libs()
            file = open(system_pathway +"BSTRP.txt",'w')
            file.write("name *" + value + "/")
            file.write("password *" + value2 + "/")
            file.write("user *" + value3 + "/")
            file.write("language *" + language + "/")
            file.close()
            print(value)
            top.destroy()
            check()
def bootstrap():
    print("laodingSHEP...")
    
    global e
    global e1
    global e2
    global top
    global language
    top=top=Toplevel(root)
    #top.iconbitmap('test1.ico')
    language = "en"
    def en():
        global language
        print("lan")
        language = "en-au"
    def es():
        global language               
        print("lan")
        language = "es"
    def fr():
        global language
        print("lan")
        language = "fr"
    def de():
        global language               
        print("lan")
        language = "de"
    def ro():
        global language               
        print("lan")
        language = "ru"
    top.title("SHEP startup")
    top.configure(background='black')
    photo = PhotoImage(file = system_pathway +"confused.png")
    canvas = Canvas(top,  bd=0, highlightthickness=0)
    canvas.pack()
    #canvas.create_image(0, 0, image=photo)
    background_label = Label(top, image=photo)
    background_label.place(x=400, y=0, relwidth=1, relheight=1)
    menubar = Menu(top)
    filemenu = Menu(menubar, tearoff=0)
    
    filemenu.add_command(label="English", command=en)
    filemenu.add_command(label="Spanish", command=es)
    filemenu.add_command(label="French", command=fr)
    filemenu.add_command(label="German", command=de)
    filemenu.add_command(label="Russian", command=ro)
    menubar.add_cascade(label="Language", menu=filemenu)
    top.config(menu=menubar)
    top.attributes("-fullscreen", True)
    #root.update_idletasks()
    #top.geometry("500x400")
    l=Label(top,text="WIFI:")
    l.pack(side = LEFT)
    e=Entry(top)
    e.pack(side = LEFT)
    l2=Label(top,text="WIFI password:")
    l2.pack(side = LEFT)
    e1=Entry(top)
    e1.pack(side = LEFT)
    l3=Label(top,text="User name:")
    l3.pack(side = LEFT)
    e2=Entry(top)
    e2.pack(side = LEFT)
    b=Button(top,text='START SHEP',width = 25,command=close)
    b.pack(side = LEFT)
    #root.update_idletasks()
    if __name__ == '__main__':
            mainloop()
check()

