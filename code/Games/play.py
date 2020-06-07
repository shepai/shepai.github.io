from TicTacToe import TicTacToe
import random
class Queue:
    #queue data structure 
    def __init__(self):
        self.data=[]
    def push(self,item):
        self.data.append(item)
    def pop(self):
        item = self.data[0]
        del self.data[0]
        return item
    def size(self):
        return len(self.data)
class Edge:
    def __init__(self,vertex1,vertex2):
        self.name=""
        self.vertices=[vertex1,vertex2]
        self.strength=0
        self.weight=0
class Graph:
    #graph data structure for associative learning
    def __init__(self):
        self.data={}
    def addDirected(self,edge):
        #add data
        try:
            val=self.data[edge.vertices[0]]
            changes=False
            for i in range(len(val)):
                if val[i].vertices[1]==edge.vertices[1]: #if found increase strength connection
                    val[i].strength+=1
                    changes=True
            if changes==False: #if not yet in
               val.append(edge) #add
               self.data[edge.vertices[1]]=[] #add node with no connections
        except:
            self.data[edge.vertices[0]]=[edge] #add node with no connections
            self.data[edge.vertices[1]]=[]
    def show(self):
        for i in self.data:
            print(i)
            for j in self.data[i]:
                print(j.vertices,j.strength)
    def getConnected(self,vertex):
        #return all directly connected to the given vertex
        data=[]
        try:
            return self.data[vertex]
        except:
            return []
    def allReachable(self,vertex,offlimits):
        #Get a path to see if two points are reachable
        #uses breadth-first algorithm
        visited=[]
        q=Queue()
        q.push(vertex)
        visited.append(vertex)
        while q.size()>0:
            v=q.pop() #get the next connected item
            connections=self.getConnected(v)
            for i in connections:
                if i.vertices[1] not in visited and i.vertices[1] not in offlimits: #accurate
                    visited.append(i.vertices[1])
                    q.push(i.vertices[1])
        return visited
    def getEdge(self,vertex1,vertex2):
        for i in self.data[vertex1]:
            print(i.vertices[1],vertex2)
            if i.vertices[1]==vertex2:
                return i
    def shortestRoute(self,start,end,offlimit):
        q=Queue()
        q.push(start)
        cameFrom={}
        cost={}
        cameFrom[start]=None
        cost[start]=0
        while q.size()>0: #sort paths 
            current=q.pop()
            if current == end:
                break
            for next in self.getConnected(current):
                new_cost=cost[current]+next.weight
                if next.vertices[1] not in offlimit:
                    if next.vertices[1] not in cost or new_cost<cost[next.vertices[1]]:
                        cost[next.vertices[1]]=new_cost
                        q.push(next.vertices[1])
                        cameFrom[next.vertices[1]]=current
        try:
            key=cameFrom[end]
        except: #error as it is not connected
            return None
        #find direct route
        cameFromKeys=list(reversed(sorted(cameFrom)))
        path=[]
        key=end
        path.append(key)
        while key!=start:
            key=cameFrom[key]
            path.append(key)
        return list(reversed(path))

def getStrongest(EdgeList):
    average=0
    strong=[]
    for i in EdgeList: #gather average
        average+=i.strength
    average=average/len(EdgeList)
    for i in EdgeList: #gather above average
        if i.strength>=average:
            strong.append(i)
    return strong

player=Graph() #store the player moves
game=TicTacToe() #create the game
count=0
used=[]
while True:
    print("Round "+str(count+1))
    game.displayBoard()
    lastMove=["start","start"] #initialize last move for each player
    playerPos=[]
    off=[]
    while not game.win() and not game.getDraw():
        x=int(input("x: "))
        y=int(input("y: "))
        value=game.move(y,x)
        if value == False:
            print("Invalid move")
        elif not game.win() and not game.getDraw(): #move valid and not complete
            player.addDirected(Edge(lastMove[0],str(x)+","+str(y)))
            lastMove[0]=str(x)+","+str(y)
            playerPos.append(lastMove[0])
            off.append(lastMove[0])
            value=False
            Next=[]
            size=10000
            for i in playerPos: #loop through all routes
                val=player.shortestRoute(i,"win",off)
                if val!=None and len(val)<=size and "win" in val[-1]: #use equal to for most
                    Next=val
                    size=len(Next)
            print(Next)
            if Next==[] or "win" in Next[1]:
                while value==False and game.win() != True and game.getDraw() != True:
                    x,y=random.randint(1, 3),random.randint(1, 3)
                    value=game.move(y,x)
                print("Computer random guess:",str(x)+","+str(y))
            else: #computer move
                val=Next[1].split(",")
                y=int(val[1])
                x=int(val[0])
                print("Computer Move: ",val)
                value=game.move(y,x)
            lastMove[1]=str(x)+","+str(y)
            off.append(lastMove[1])
        else: #player has ended the game
            player.addDirected(Edge(lastMove[0],str(x)+","+str(y))) #add final data
            lastMove[0]=str(x)+","+str(y)
        game.displayBoard()
    if game.getDraw():
        print("Draw!")
    else:
        print("Victory to "+game.getWinner())
        if game.getWinner()=="X":
            player.addDirected(Edge(lastMove[0],"win"))
    count+=1
    game.reset()
        



#needs to know:
#   empty places
#   other players positions
#   what aim is (what creates a win)
#   current positions
#Will:
# associate data which leads to victory (what is consistant)
# randomly guess if no understanding
# aim to stop oponent from winning (prevent 3 in a row) and aim for 3 in a row

#if X at 1,1 1,2 1,3 strongly connects with victory
#then when the current board is 1,1 1,2 the algorithm will think about what each choice
#it has will do and what position will most likely lead them to victory and what will lead it to victory
#the strongest choice wins


"""
while game.win() != True and game.getDraw() != True:
    value=game.move(int(input("y: ")),int(input("x: ")))
    if value == False:
        print("Invalid move")
    else:
        game.displayBoard()
if game.getDraw():
    print("Draw!")
else:
    print("Victory to "+game.getWinner())
"""

