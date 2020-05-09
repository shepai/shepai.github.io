import cleverbotfree.cbfree
import sys
from selenium import webdriver


class bot:
    def __init__(b):
        b.cb = cleverbotfree.cbfree.Cleverbot()

    def chat(b,userInput):
        response = b.cb.single_exchange(userInput)
        return response
slashn="""
"""

bot1=bot()
bot2=bot()

response2=input(">")

while True:
    file=open("convo1.txt","a")
    response1=bot1.chat(response2)
    file.write("bot1: "+response1+slashn)
    response2=bot2.chat(response1)
    file.write("bot2: "+response2+slashn)
    file.close()
    print("bot1:",response1)
    print("bot2",response2)
cb.browser.close()
sys.exit()
