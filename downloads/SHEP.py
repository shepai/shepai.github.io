#SHEP updated library
#By Dexter R Shepherd, aged 18
#V0.0.8
#Uses a weighted graph data structure to store data about inputs. Code for neural network
class edge: #hold the connectios between items
    def __init__(e,name,vertex1,vertex2,conStrength):
        e.name=name
        e.connectionStrength=conStrength
        e.vertices=[vertex1,vertex2]
    def getName(e): #get the name
        return e.name
    def setName(e,string): #set a new name
        e.name=string
    def getConnections(e): #return both connections as [a,b]
        return e.vertices
    def getOtherConnection(e,v): #return other connections to entered
        if e.vertices[0].getName()==v.getName():
            return e.vertices[1]
        else:
            return e.vertices[0]
    def getConStrength(e): #return the strength of the connection
        return  e.connectionStrength
    def checkVertex(e,vert): #check edge contains vertex
        if vert.getName()==e.vertices[0].getName() or vert.getName()==e.vertices[1].getName():
            return True
        return False
class vertex: #hold the item
    def __init__(v,name):
        v.name=name
    def getName(v):
        return v.name #return data item name
    def setName(v,nam):
        v.name=nam
class graph: #a graoh data structure which stores unused information in file instead of RAM
    def __init__(gr,filepath): #initialize
        gr.filepath=filepath
        gr.size=0
    def add(gr,vert,connections):
        mode="w" 
        if (gr.isVertex(vert)): #if the vertex exists
            mode="a"
        file=open(gr.filepath+vert.getName()+".txt",mode)
        for i in range(len(connections)):
            file.write("[name="+connections[i].getName()+",") #write in format
            file.write("connection="+connections[i].getOtherConnection(vert).getName()+",")
            file.write("strength="+str(connections[i].getConStrength())+"]")
        file.close()
    def buildEdges(gr,vert): #open file and return edges
        file=open(gr.filepath+vert.getName()+".txt","r")
        r=file.read()
        file.close() 
        r=r.replace("[","") #convert format
        data=r.split("]")
        edges=[]
        for j in range(len(data)-1):
            items=data[j].split(",") #get edge info
            vertTo=items[1].replace("connection=","")
            strength=int(items[2].replace("strength=",""))
            name=items[0].replace("name=","")
            edges.append(edge(name,vert,vertex(vertTo),strength))
        return edges
    def getEdge(gr,vert,vert2,TYPE):
        edges=gr.buildEdges(vert) #get connections
        for j in range(len(edges)):
            if edges[j].checkVertex(vert2) and edges[j].getName()==TYPE: #validate
                return edges[j]
        return None
    def inEdges(gr,vert):
        x=0
    def removeVertex(gr,vert): #remove a vertex from the graph
        edges=gr.buildEdges(vert) #get connections
        #loop through connections
        #remove each conenction
        #delete the current vert file
    def removeEdge(gr,vert,e):
        edges=gr.buildEdges(vert)
        for j in range(len(edges)):
            cons=e.getConnections()
            if edges[j].checkVertex(cons[0]) and edges[j].checkVertex(cons[1]):
                #edge found at index j
                del edges[j] #delete from array
                #replacefile
                file=open(gr.filepath+vert.getName()+".txt","w") #rewrite to file
                for i in range(len(edges)):
                    file.write("[name="+edges[i].getName()+",") #write in format
                    file.write("connection="+edges[i].getOtherConnection(vert).getName()+",")
                    file.write("strength="+str(edges[i].getConStrength())+"]")
                file.close()
                return edges #return the edge array
        return None
    def getConnections(gr,vert):
        edges=gr.buildEdges(vert) #get connections
        return edges
    def isConnected(gr,vert1,vert2):
        edges=gr.getConnections(vert1)
        for i in range(len(edges)):
            if edges[i].checkVertex(vert2):
                return True
        return False
    def isVertex(gr,item):
        try: #test if item is a current vertex
            file=open(gr.filepath+item.getName()+".txt","r")
            file.close()
            return True
        except:
            return False
class AI:
    def __init__(ai,path):
        ai.path=path
        ai.DataStructure=graph(path)
        ai.pastItems=[]
    def enterData(ai,listData,TYPE):
        nodesToSave=[]
        for i in range(len(listData)): #loop through and create connections
            vertCurrent=vertex(listData[i])
            edges=[]
            for j in range(len(listData)): #O(n^2)
                if i!=j:
                    edges.append(edge(TYPE,vertCurrent,vertex(listData[j]),1))
            nodesToSave.append([vertex(listData[i]),edges])
        for i in range(len(nodesToSave)): #loop through nodes
            for j in range(len(nodesToSave[i][1])): #loop through edges
                    vert1=nodesToSave[i][0]
                    vert2=nodesToSave[i][1][j].getConnections()[1]
                    if ai.DataStructure.isVertex(vert1) and ai.DataStructure.getEdge(vert1,vert2,TYPE)!=None: #node exists snd edge is in
                            #increase node 
                            edge1=edge(TYPE,vert1,vert2,ai.DataStructure.getEdge(vert1,vert2,TYPE).getConStrength()) #get old
                            edge2=edge(TYPE,vert1,vert2,edge1.getConStrength()+1) #make new with strength+1
                            if ai.DataStructure.removeEdge(vert1,edge1) !=None and edge1.getConStrength()+1<10: #remove old
                                #decrease all other nodes
                                edges=ai.DataStructure.buildEdges(vert1)
                                for z in range(len(edges)): #reduce size of unused
                                    if edges[z].getName()==TYPE:
                                        strength=edges[z].getConStrength()
                                        connections=edges[z].getConnections()
                                        name=edges[z].getName()
                                        ai.DataStructure.removeEdge(vert1,edges[z])
                                        if strength-1>0:
                                            edge3=edge(name,connections[0],connections[1],strength-1)
                                            ai.DataStructure.add(vert1,[edge3]) #reduce strength of
                                ai.DataStructure.add(vert1,[edge2]) #add the new
                    else:
                        #node is either non existant or the edge is not inside
                        ai.DataStructure.add(vert1,[nodesToSave[i][1][j]]) #add each edge to structure
                        #add
    def getConnected(ai,listData,TYPE):
        #get the most connected data
        connections=[]
        for i in range(len(listData)):
            edges=(ai.DataStructure.buildEdges(vertex(listData[i])))
            sumOf=0
            eA=[]
            chances=[]
            for j in range(len(edges)): #loop through edges
                if edges[j].getName()==TYPE:
                   sumOf+=edges[j].getConStrength()
                   eA.append(edges[j])#remove those not connected to type
            edges=eA#set revised array
            if len(edges)>0:
                average=int(sumOf/len(edges)) #calculate the average strength
                for j in range(len(edges)): #loop through edges again
                    add_=True
                    if edges[j].getConStrength()>=average and average>=2: #if above average and no specticle and edge connection in datanae
                        for z in range(len(connections)): #loop through tally table
                           if connections[z][0].getName()==edges[j].getConnections()[1].getName(): #found
                                add_=False #set to not add
                                break
                        if add_:
                           connections.append([edges[j].getConnections()[1],edges[j].getConStrength()]) #add all connections
        for i in range(len(connections)): #insertion sort
            for j in range(len(connections)):
                if connections[i][1]>connections[j][1]: #switch
                    temp=connections[j]
                    connections[j]=connections[i]
                    connections[i]=temp
        items=[]
        for i in range(len(connections)): #get names
            items.append(connections[i][0].getName())
        return items
    def link(ai,items,linkTo):
        for i in range(len(items)):
            for j in range(len(linkTo)):
                vert1=vertex(items[i])
                vert2=vertex(linkTo[j])
                if ai.DataStructure.getEdge(vert1,vert2,"DNT")!=None:
                    #edge exists
                    edge1=edge("DNT",vert1,vert2,ai.DataStructure.getEdge(vert1,vert2,"DNT").getConStrength())
                    if ai.DataStructure.removeEdge(vert1,edge1) !=None: #remove old
                        edge1=edge("DNT",vert1,vert2,edge1.getConStrength()+1)
                        ai.DataStructure.add(vert1,[edge1]) #add the new
                else: #does not exist so needs adding
                    edge1=edge("DNT",vert1,vert2,1)
                    ai.DataStructure.add(vert1,[edge1]) #add each edge to structure
    def process(ai,items):
        ai.enterData(items,"SNT")
        linkedItems=ai.getConnected(items,"SNT")
        linkedItems=[x for x in linkedItems if x in items] #remove data not in items
        if ai.pastItems!=[]:
            ai.link(ai.pastItems,items) #link to the past input
        ai.pastItems=items
        return ai.getConnected(linkedItems,"DNT")#get data it connects to and return it
    def negFeedback(ai,origin,items):
        for j in range(len(origin)):
            vert1=vertex(origin[j])
            for i in range(len(items)): #loop through all items
                vert2=vertex(items[i])
                try:
                    edge1=edge("DNT",vert1,vert2,ai.DataStructure.getEdge(vert1,vert2,"DNT").getConStrength())
                    if ai.DataStructure.removeEdge(vert1,edge1) !=None and edge1.getConStrength()-1>0: #remove old
                        edge1=edge("DNT",vert1,vert2,edge1.getConStrength()-1)
                        ai.DataStructure.add(vert1,[edge1]) #add the newbot=AI("test/testFiles/newGraph/")
                except:
                    NOTHING_FOUND=0
