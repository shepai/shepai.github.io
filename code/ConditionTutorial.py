#["speech-that is a nice ball","vison-ball","temp-40"]
#["speech-that is a nice ball","vison-ball","temp-20"]
#["speech-that is a nice ball","vison-ball","temp-80"]
TEST=[["oranges","lemons","dog"],
      ["cat","oranges","lemons"],
      ["speech-that is a nice ball","vison-ball","temp-80"]]

def condition(array):
    freq=[]
    for i in array:
        for j in i:
            c=0
            for k in array:
                if j in k:
                    c+=1
            freq.append(c)
    h=0
    for i in freq:
        if i>h:
            h=i
    counter=0
    new=[]
    for i in array:
        for j in i:
            if freq[counter]>=h and j not in new:
                new.append(j)
            counter+=1
    return new       
#enter into function
print(condition(TEST))
#return correlation between items [speech,vision]
