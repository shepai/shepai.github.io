#chess game
#AI test
#Code by Dexter Shepherd, aged 18
import sys
import os

try: #initialize colour scheme
    color = sys.stdout.shell
except:
    print("")
board=[["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"],["_____","_____","_____","_____","_____","_____","_____","_____"]]
playerpoints=[0,0]
counter=0
playerGo='W'
def displayBoard():
    #try different methods of colour/ display for idle and console
    try:
        for i in range(8): #idle
            color.write(str(i+1),"KEYWORD")
            for j in range(8):
                if board[i][j][0]=="W":
                    color.write("  "+board[i][j]+"","STRING")
                elif board[i][j][0]=="B":
                    color.write("  "+board[i][j]+" ","COMMENT")
                else:
                    color.write("  "+board[i][j],"KEYWORD")
            print(" ")
    except:
        try:
            os.system('cls') #console
            for i in range(8):
                 print((str(i+1)+str(board[i])))
        except:
            print("no screen")
def displaySpaces(places):
    try:
        for i in range(8): #idle
            color.write(str(i+1),"KEYWORD")
            for j in range(8):
                placeMarker=False
                for z in range(len(places)):
                    if i == places[z][0] and j==places[z][1]:
                        placeMarker=True
                if placeMarker==True:
                    print("  "+board[i][j]+" ", end = '')
                elif board[i][j][0]=="W":
                    color.write("  "+board[i][j]+"","STRING")
                elif board[i][j][0]=="B":
                    color.write("  "+board[i][j]+" ","COMMENT")
                else:
                    color.write("  "+board[i][j],"KEYWORD")
            print(" ")
    except:
        nothing_happens_here=True
def load(): #load the pieces into the game
    pieces=["RK1","KN1","BI1","QN1","KG1","BI2","KN2","RK2"] #pieces in order
    for i in range(8):
        board[0][i]="W"+pieces[i] #white team
        board[1][i]="W"+"PN"+str(i+1)
        board[6][i]="B"+"PN"+str(i+1)
        board[7][i]="B"+pieces[i] #black team
    displayBoard()
def checkPos(x,y): #check the position is free
    if board[x][y] != "_____": #check its free
        if str(board[x][y])[0] !=playerGo: #check whether its a kill or not
            playerpoints[counter]+=1
            return True
        return False
    return True
def getPos(piece): #check the piece exists
    for i in range(8):
        for j in range(8):
            if board[i][j] == piece:
                return [i,j]
    return False
def checkEnemy(x,y): #check if an enemy is in a position
    if (board[x][y])[0]!=playerGo and (board[x][y])[0]!="_":
        return True
    return False
def avaliableSpaces(piece):
    #check the spaces are avaliable
    co_ords=getPos(piece)
    spaces=[]
    if co_ords !=False:
        if "PN" in piece:
            #pawn rules
            if playerGo=='W':
                if co_ords[0] <7: #travelling up and down code
                    if co_ords[0] == 1:
                        if checkEnemy(2,co_ords[1])==False:
                            spaces.append([2,co_ords[1]])
                            if checkEnemy(3,co_ords[1])==False:
                                spaces.append([3,co_ords[1]])
                    else:
                        if checkEnemy(co_ords[0]+1,co_ords[1])==False:
                            spaces.append([co_ords[0]+1,co_ords[1]])
                #check enemy is found diagonally
                    if  co_ords[1]<7 and co_ords[1]>=0:
                        if checkEnemy(co_ords[0]+1,co_ords[1]+1):
                            spaces.append([co_ords[0]+1,co_ords[1]+1])
                if co_ords[0]>0 and co_ords[1]<=7 and co_ords[1]>0:
                        if checkEnemy(co_ords[0]+1,co_ords[1]-1):
                            spaces.append([co_ords[0]+1,co_ords[1]-1])
                
            else:
                if co_ords[0] > 0: #travelling up and down code
                    if co_ords[0] == 6:
                        if checkEnemy(5,co_ords[1])==False:
                            spaces.append([5,co_ords[1]])
                            if checkEnemy(4,co_ords[1])==False:
                                spaces.append([4,co_ords[1]])
                    else:
                        if checkEnemy(co_ords[0]-1,co_ords[1])==False:
                            spaces.append([co_ords[0]-1,co_ords[1]])
                #check if enemy is found diagonally
                    if  co_ords[1]<=7 and co_ords[1]>0:
                        if checkEnemy(co_ords[0]-1,co_ords[1]-1):
                                spaces.append([co_ords[0]-1,co_ords[1]-1])
                if co_ords[0] < 7  and co_ords[1]<7 and co_ords[1]>=0: #check if not next to side
                    if checkEnemy(co_ords[0]-1,co_ords[1]+1):
                        spaces.append([co_ords[0]-1,co_ords[1]+1])
        elif "KN" in piece:
            #knight
            #vertical L
            if co_ords[0]+2 < 8 and co_ords[1]+1<8:
                if board[co_ords[0]+2][co_ords[1]+1]== "_____" or board[co_ords[0]+2][co_ords[1]+1][0]!=playerGo:
                    spaces.append([co_ords[0]+2,co_ords[1]+1])
            if co_ords[0]+2 < 8 and co_ords[1]-1>=0:
                if board[co_ords[0]+2][co_ords[1]-1]== "_____" or board[co_ords[0]+2][co_ords[1]-1][0]!=playerGo:
                    spaces.append([co_ords[0]+2,co_ords[1]-1])
            if co_ords[0]-2 >=0 and co_ords[1]+1<8:
                if board[co_ords[0]-2][co_ords[1]+1]== "_____" or board[co_ords[0]-2][co_ords[1]+1][0]!=playerGo:
                    spaces.append([co_ords[0]-2,co_ords[1]+1])
            if co_ords[0]-2 >=0 and co_ords[1]-1>=0:
                if board[co_ords[0]-2][co_ords[1]-1]== "_____" or board[co_ords[0]-2][co_ords[1]-1][0]!=playerGo:
                    spaces.append([co_ords[0]-2,co_ords[1]-1])
            #horizontal L
            if co_ords[1]+2 < 8 and co_ords[0]+1<8:
                if board[co_ords[0]+1][co_ords[1]+2]== "_____" or board[co_ords[0]+1][co_ords[1]+2][0]!=playerGo:
                    spaces.append([co_ords[0]+1,co_ords[1]+2])
            if co_ords[1]+2 < 8 and co_ords[0]-1>=0:
                if board[co_ords[0]-1][co_ords[1]+2]== "_____" or board[co_ords[0]-1][co_ords[1]+2][0]!=playerGo:
                    spaces.append([co_ords[0]-1,co_ords[1]+2])
            if co_ords[1]-2 >=0 and co_ords[0]+1<8:
                if board[co_ords[0]+1][co_ords[1]-2]== "_____" or board[co_ords[0]+1][co_ords[1]-2][0]!=playerGo:
                    spaces.append([co_ords[0]+1,co_ords[1]-2])
            if co_ords[1]-2 >=0 and co_ords[0]-1>=0:
                if board[co_ords[0]-1][co_ords[1]-2]== "_____" or board[co_ords[0]-1][co_ords[1]-2][0]!=playerGo:
                    spaces.append([co_ords[0]-1,co_ords[1]-2])
        elif "KG" in piece:
            #king
            for j in range(3):
                for i in range(3):
                    try:
                        if board[co_ords[0]-1+i][co_ords[1]-1+j]=="_____" or board[co_ords[0]-1+j][co_ords[1]-1+j][0]!=PlayerGo:
                                #Check it is clear
                                spaces.append([co_ords[0]-1+i,co_ords[1]-1+j])
                    except:
                              x=0                          
        if "RK" in piece or "QN" in piece: #gather queen as parts
            #rook
            counter=0
            flag=False
            count=co_ords[0]+1
            while count<8 and flag==False: #count going forwards
                    if board[count][co_ords[1]] == "_____":
                        spaces.append([count,co_ords[1]])
                    elif board[count][co_ords[1]][0]!=playerGo:
                        spaces.append([count,co_ords[1]])
                        flag=True
                    else:
                        flag = True
                    count=count+1
            count=co_ords[0]-1
            flag=False
            while count >=0 and flag==False: #going bakwards
                    if board[count][co_ords[1]] == "_____":
                        spaces.append([count,co_ords[1]])
                    elif board[count][co_ords[1]][0]!=playerGo:
                        spaces.append([count,co_ords[1]])
                        flag=True
                    else:
                        flag = True
                    count=count-1
            count=co_ords[1]+1
            
            flag=False
            while count<8 and flag==False: #check right
                    if board[co_ords[0]][count] == "_____":
                        spaces.append([co_ords[0],count])
                    elif board[co_ords[0]][count][0]!=playerGo:
                        spaces.append([co_ords[0],count])
                        flag=True
                    else:
                        flag = True
                    count=count+1
                    
            count=co_ords[1]-1
            
            flag=False
            while count>=0 and flag==False: #check left
                    print(board[co_ords[0]][count])
                    if board[co_ords[0]][count] == "_____":
                        spaces.append([co_ords[0],count])
                    elif board[co_ords[0]][count][0]!=playerGo:
                        spaces.append([co_ords[0],count])
                        flag=True
                    else:
                        flag = True
                    count=count-1
                    
        if "BI" in piece or "QN" in piece:
            #bishop
            try:
                i=1
                while co_ords[0]+i<8 and co_ords[1]+i<8:
                    #print("do",board[co_ords[0]+i][co_ords[1]+i])
                    if board[co_ords[0]+i][co_ords[1]+i] == "_____":
                            spaces.append([co_ords[0]+i,co_ords[1]+i])
                    elif board[co_ords[0]+i][co_ords[1]+i][0] != playerGo:
                            spaces.append([co_ords[0]+i,co_ords[1]+i])
                            #print("found")
                            break
                    elif board[co_ords[0]+i][co_ords[1]+i][0] == playerGo:
                        #print("found2")
                        break
                    i+=1
            except:
                x=0
            try:
                i=1
                while i<8:
                    if board[co_ords[0]+i][co_ords[1]-i] == "_____":
                            spaces.append([co_ords[0]+i,co_ords[1]-i])
                    elif board[co_ords[0]+i][co_ords[1]-i][0] != playerGo:
                            spaces.append([co_ords[0]+i,co_ords[1]-i])
                            break
                    elif board[co_ords[0]+i][co_ords[1]-i][0] == playerGo:
                        break
                    i+=1
            except:
                x=0
            try:
                i=1
                while i<8:
                    if board[co_ords[0]-i][co_ords[1]-i] == "_____":
                            spaces.append([co_ords[0]-i,co_ords[1]-i])
                    elif board[co_ords[0]-i][co_ords[1]-i][0] != playerGo:
                            spaces.append([co_ords[0]-i,co_ords[1]-i])
                            break
                    elif board[co_ords[0]-i][co_ords[1]-i][0] == playerGo:
                        break
                    i+=1
            except:
                x=0
            try:
                i=1
                while i<8:
                    if board[co_ords[0]-i][co_ords[1]+i] == "_____":
                            spaces.append([co_ords[0]-i,co_ords[1]+i])
                    elif board[co_ords[0]-i][co_ords[1]+i][0] != playerGo:
                            spaces.append([co_ords[0]-i,co_ords[1]+i])
                            break
                    elif board[co_ords[0]-i][co_ords[1]+i][0] == playerGo:
                        break
                    i+=1
            except:
                x=0
                
                        
    return spaces
def INPUT(string):
    return input(string)
def count(piece):
    counter=0
    for i in range(8):
        for j in range(8):
            if playerGo+piece in board[i][j] :
                counter+=1
    return counter+1
def move(piece,num):
    position=getPos(piece)
    if piece[0]!=playerGo: #stop user from using other pieces
        print("Not your piece")
    elif position != False:
       
       if checkPos(int(num[0])-1,int(num[1])-1):
           board[int(position[0])][int(position[1])]="_____"
           board[int(num[0])-1][int(num[1])-1]=piece
           if "PN" in piece and (int(num[0])-1 == 7 or int(num[0])-1 == 0): #change piece
               flag=True
               p=["RK","KN","BI","QN"]
               while flag:
                   change=INPUT("What would you like to choose? ").upper()
                   for i in range(4): #check valid
                       if p[i]==change:
                           flag=False
               board[int(num[0])-1][int(num[1])-1]=playerGo+change+str(count(change))
           return True
    
    print("Invalid move")
    return False
def win():
    if playerpoints[0]==16 or playerpoints[1]==16:
        return True
    return False
load() #load board into the game
counter=0
while win()==False:
    print("Player "+playerGo+"'s Turn") #output messages
    print("********************************")
    print("Player W points: ",playerpoints[0])
    print("Player B points: ",playerpoints[1])
    print("********************************")
    piece=INPUT("Piece: ").upper()
    spaces=avaliableSpaces(piece)
    if spaces != []:
        print("Avaliable spaces")
        print("Row,Column")
        displaySpaces(spaces)
        for i in range(len(spaces)):
                print("("+str(int(spaces[i][0]+1))+","+str(int(spaces[i][1]+1))+")")
        ver=int(INPUT("Horizontal position: "))
        hor=int(INPUT("Vertical position: "))
        found=False
        for i in range(len(spaces)):
            if [ver-1,hor-1]==spaces[i]:
                found=True
        if found:
            if int(ver) <= 8 and int(ver) >= 1 and int(hor) <=8 and int(hor)>=1 and getPos(piece) != False:
                gather=move(piece,[ver,hor])
                #if "PN" in piece
                displayBoard()
                if (gather): #move was legal
                    counter+=1
                    playerGo='B'
                    if counter >1: #change the player go
                        counter=0
                        playerGo='W'
            else:
                print("Not on square")
        else:
            print("Not a valid move for item")
    else:
        if playerpoints[counter]==16: #checkmate
            print("Checkmate!!")
            counter+=1
            playerGo='B'
            if counter >1: #change the player go
                    counter=0
                    playerGo='W'
            playerpoints[counter]+=1
