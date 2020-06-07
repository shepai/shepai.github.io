#graph machine learning
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
                #print(edge.vertices[0],val[i].vertices[1],edge.vertices[1])
                if val[i].vertices[1]==edge.vertices[1]: #if found increase strength connection
                    val[i].strength+=1
                    changes=True
            if changes==False: #if not yet in
               val.append(edge) #add
               try: #check if real
                   val=self.data[edge.vertices[1]]
               except:
                    self.data[edge.vertices[1]]=[] #add node with no connections
            else:
                self.data[edge.vertices[0]]=val
        except:
            self.data[edge.vertices[0]]=[edge] #add node with no connections
            self.data[edge.vertices[1]]=[]
    def addUndirected(self,edge):
        #add data undirected (so for both nodes)
        self.addDirected(edge) #add edge
        edge=self.getEdge(edge.vertices[0],edge.vertices[1]) #get new connetion
        vertices=edge.vertices #reverse edge connection
        strength=edge.strength
        edge=Edge(vertices[1],vertices[0]) #new edge to not confuse with old memory
        edge.strength=strength
        self.addDirected(edge) #add edge 
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
    def strongest(self,vertex):
        connections=self.getConnected(vertex)
        if len(connections)>0:
            sum=0
            for i in connections:
                sum+=i.strength
            average=sum/len(connections)
            nodes=[]
            for i in connections:
                if i.strength>average:
                    nodes.append(i.vertices[1])
            return nodes
g=Graph()

g.addUndirected(Edge("apple","banana"))
g.addUndirected(Edge("apple","orange"))
g.addUndirected(Edge("apple","dog"))
g.addUndirected(Edge("apple","banana"))
g.addUndirected(Edge("apple","orange"))
g.addUndirected(Edge("banana","dog"))
g.addUndirected(Edge("dog","cat"))
g.addUndirected(Edge("dog","cat"))
#g.show()

#print(g.shortestRoute("apple","d",[""]))
print(g.strongest("apple"))
