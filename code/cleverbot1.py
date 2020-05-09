import cleverbotfree.cbfree
import sys
from selenium import webdriver

cb = cleverbotfree.cbfree.Cleverbot()

def chat(userInput):
    response = cb.single_exchange(userInput)
    return response
slashn="""
"""

userInput = input('User: ')
file=open("convo.txt","a") #create file
file.write("bot1: "+userInput+slashn)
file.close()

while True:
    file=open("convo.txt","a")
    previous=chat(userInput)
    print(previous)
    file.write("bot2: "+previous+slashn)
    userInput=chat(previous)
    file.write("bot1: "+userInput+slashn)
    print(userInput)
    file.close()
cb.browser.close()
sys.exit()
