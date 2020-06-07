import sys
import os

try: #initialize colour scheme
    color = sys.stdout.shell
except:
    print("")
class TicTacToe:
    board=[["-","-","-"],["-","-","-"],["-","-","-"]] #board
    playerSymbol="X"
    def  __init__(ttt):
        print("Welcome to Tic Tac Toe!!!")
        ttt.displayBoard()
    def displayBoard(ttt):
        try:
            for i in range(3):
                for j in range(3):
                    if ttt.board[i][j][0]=="X":
                        color.write(ttt.board[i][j]+" ","STRING")
                    elif ttt.board[i][j][0]=="O":
                        color.write(ttt.board[i][j]+" ","COMMENT")
                    else:
                        color.write(ttt.board[i][j]+" ","KEYWORD")
                print("")
        except:
            try:
                os.system('cls') #console
                for i in range(3):
                     print(ttt.board[i])
            except:
                print("No screen")
    def getPos(ttt,x,y):
        if x <=3 and x >=1 and y<=3 and y>=1: #validate
            return ttt.board[y-1][x-1]
        return False
    def win(ttt):
        inRow=False
        pos="X"
        for j in range(2): #horizontal
            for i in range(3):
                if ttt.board[i][0]==pos and ttt.board[i][1]==pos and ttt.board[i][2]==pos:
                    inRow=True
            pos="O"
        pos="X"
        for j in range(2): #vertical
            for i in range(3):
                if ttt.board[0][i]==pos and ttt.board[1][i]==pos and ttt.board[2][i]==pos:
                    inRow=True
            pos="O"
        pos="X"
        for j in range(2): #vertical
            if ttt.board[0][0]==pos and ttt.board[1][1]==pos and ttt.board[2][2]==pos:
                inRow=True
            elif ttt.board[0][2]==pos and ttt.board[1][1]==pos and ttt.board[2][0]==pos:
                inRow=True
            pos="O"
        return inRow
    def getDraw(ttt):
        counter=0
        for i in range(3):
            for j in range(3):
                if ttt.board[i][j]!="-":
                    counter+=1
        if counter==9 and ttt.win()==False:#
            return True
        return False
    def move(ttt,y,x):
        if x <=3 and x >=1 and y<=3 and y>=1: #validate
            if ttt.board[y-1][x-1] == "-": #space available
                ttt.board[y-1][x-1] = ttt.playerSymbol #set symbol
                if ttt.playerSymbol == "X": #switch gos
                    ttt.playerSymbol="O"
                else:
                    ttt.playerSymbol="X"
                return ttt.board
        return False
    def availablePositions(ttt):
        pos=[]
        x=0
        for i in ttt.board:
            x+=1
            y=0
            for j in i:
                y+=1
                if j=="-":
                    pos.append([x,y])
        return pos
    def getWinner(ttt):
        if ttt.playerSymbol == "X": #switch gos
                   return "O"
        else:
                    return "X"
    def reset(ttt):
        ttt.playerSymbol="X"
        ttt.board=[["-","-","-"],["-","-","-"],["-","-","-"]] #board
