import os
import json

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

class fileStructure:
        #python dictionary structure but saves all data and stores it in drive and not RAM
        def __init__(self,filepath):
            if not os.path.isdir(filepath+"DictionaryFolder/"):
                os.makedirs(filepath+"DictionaryFolder/")
            self.filepath=filepath+"DictionaryFolder/"
            if not os.path.exists(filepath+"DictionaryFolder/index.txt"):
                file=open(filepath+"DictionaryFolder/index.txt","w")
                file.close()
        def readFolder(self,vertex,path):
            nodes=[]
            for subdir, dirs, files in os.walk(path):
                for file in files:
                    f=open(path+file,"r")
                    r=f.read()
                    f.close()
                    stats=r.split(":::") #read data in file
                    e=Edge(vertex,stats[3]) #form edge
                    e.name=stats[2]
                    e.strength=stats[0]
                    e.weight=stats[1]
                    nodes.append(e)
            return nodes
        def writeFolder(self,folder,nodes):
            for edge in nodes: #write each edge to files
                found=False
                count=0
                while found==False:
                    try:
                        file=open(folder+str(edge).replace("<","").replace(">","")+str(count)+".txt","r")
                        count+=1
                    except:
                        found=True
                file=open(folder+str(edge).replace("<","").replace(">","")+str(count)+".txt","w")
                file.write(str(edge.strength)+":::"+str(edge.weight)+":::"+edge.name+":::"+edge.vertices[1])
                file.close()
        def __repr__(self):
            nodes=[]
            for subdir, dirs, files in os.walk(self.filepath):
                for i in dirs:
                    nodes.append(i)
            return nodes
        def __str__(self):
            nodes=[]
            for subdir, dirs, files in os.walk(self.filepath):
                for i in dirs:
                    nodes.append(i)
            return str(nodes)
        def __getitem__(self,value): #get value
            if value==0: #called upon in different way
                for subdir, dirs, files in os.walk(self.filepath):
                    return dirs
            f=open(self.filepath+"index.txt", encoding = "ISO-8859-1")
            for line in f:
                line=line.replace("\n","")
                vals=line.split(",")
                if vals[0]==value:
                        return self.readFolder(value,self.filepath+vals[1]+"/")
            raise KeyError(str(value)+" -- "+"Item not found in structure") #return an error
        def __setitem__(self,value,setTo): #set value
            num=-1
            count=0
            f=open(self.filepath+"index.txt", encoding = "ISO-8859-1")
            for line in f:
                count+=1
                line=line.replace("\n","")
                vals=line.split(",")
                if vals[0]==value:
                    num=int(vals[1])
                    for subdir, dirs, files in os.walk(self.filepath+vals[1]+"/"):
                        for z in files:
                                os.remove(self.filepath+vals[1]+"/"+z)
                        os.rmdir(self.filepath+vals[1]+"/")
                        break
            if num==-1:
                num=count+1 #create number
                slashn="\n"
                f=open(self.filepath+"index.txt","a") #add to index file
                f.write(value+","+str(num)+slashn)
                f.close()
            os.makedirs(self.filepath+str(num)+"/")
            self.writeFolder(self.filepath+str(num)+"/",setTo) #write to the folder
        def __len__(self):
            #return the length of the data stored
            for subdir, dirs, files in os.walk(self.filepath):
                return len(dirs)
class Graph:
    #graph data structure for associative learning
    #only change from other graph is that the show function does not work
    def __init__(self,filepath):
        self.data=fileStructure(filepath)
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
               self.data[edge.vertices[0]]=val #set data
               try: #check if real
                   val=self.data[edge.vertices[1]]
               except:
                    self.data[edge.vertices[1]]=[] #add node with no connections
            else:
                self.data[edge.vertices[0]]=val
        except:
            self.data[edge.vertices[0]]=[edge] #add node with no connections
            try:
                val=self.data[edge.vertices[1]] #check exists
            except:
                self.data[edge.vertices[1]]=[] #create empty
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
        for i in self.data[0]:
            print(i)
            for j in self.data[i]:
                print(j.vertices,j.strength)
    def delete(self,vertex):
        try:
            cons=self.getConnected(vertex)
            for i in cons: #remove each connection to if undirected
                current=self.data[i.vertices[1]]
                while vertex in current: #delete where it appears
                    del current[current.index(vertex)]
            return self.data.pop(vertex, None) #finally remove
        except: #nothing in the data
            return None
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

