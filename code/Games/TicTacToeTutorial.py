from TicTacToe import TicTacToe
from graph import Graph, Edge
import random

game=TicTacToe() #create the game
player=Graph()
count=1
used=[]
while True:
    print("Round "+str(count))
    game.displayBoard()
    lastMove=["start","start"]
    playerPos=[]
    off=[]
    while not game.win() and not game.getDraw():
        x=int(input("x:"))
        y=int(input("y:"))
        value=game.move(y,x)
        if value == False:
            print("invalid move")
        elif not game.win() and not game.getDraw():
            #get AI turn
            player.addDirected(Edge(lastMove[0],str(x)+","+str(y)))
            lastMove[0]=str(x)+","+str(y)
            playerPos.append(lastMove[0])
            value=False
            Next=[]
            size=99999
            for i in playerPos:
                val=player.shortestRoute(i,"win",off)
                if val!=None and len(val)<size and "win" in val[-1]:
                    Next=val
                    size=len(val)
            print(Next)
            if Next==[] or "win" in Next[1]:
                while value==False and game.win()!=True and game.getDraw()!=True:
                    x,y=random.randint(1,3),random.randint(1,3)
                    value=game.move(y,x)
                print("Computer random move",str(x)+","+str(y))
            else: 
                val=Next[1].split(",")
                y=int(val[1])
                x=int(val[0])
                print("Computer move",str(x)+","+str(y))
                value=game.move(y,x)
            lastMove[1]=str(x)+","+str(y)
            off.append(lastMove[1])
        else:
            player.addDirected(Edge(lastMove[0],str(x)+","+str(y)))
        game.displayBoard()
    if  game.getDraw():
        print("Draw!")
    else:
        print("Victory to "+game.getWinner())
        if game.getWinner()=="X":
            player.addDirected(Edge(lastMove[0],"win"))
    count+=1
    game.reset()
