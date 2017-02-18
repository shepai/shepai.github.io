var = 0
while True:
    g = input("T or S or C? ")
    var += 1
    print("words added: " + var)
    g = g.lower()
    if g == 't':
        value = input("word: ")
        value2 = input("type: ")
        char = value[0]
        file = open(char + ".txt",'a')
        file.write(value)
        file.write('*')
        file.write(value2+"/")
        file.close()
    elif g == 's':
        value = input("word: ")
        value2 = input("type: ")
        char = value[0]
        file = open(char + "]" + ".txt",'a')
        file.write(value)
        file.write('*')
        file.write(value2+"/")
        file.close()
    elif g == 'c':
        value = input("word: ")
        value2 = input("type: ")
        char = value[0]
        file = open(char + "[" + ".txt",'a')
        file.write(value)
        file.write('*')
        file.write(value2+"/")
        file.close()
