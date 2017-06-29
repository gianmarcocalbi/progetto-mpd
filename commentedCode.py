
'''
no_blankA = open("no_blankActivities.txt", "w")
with open(pathRawActData, "r") as f:
        actData = []
        count = 0
        for line in f:
            if count != 0 and count != 1:
                line = re.sub("\\t+", ";", line)
                line = line[:-1]
                m = line.split(sep=";")
                no_blankA.write(line + '\n')
                actData.append(m)
            count += 1
            
    #List of activities without duplicates
    uniqueAct = [];
    for act in range(0,len(activities_set)):
        uniqueAct.append(activities_set[act][2])
    uniqueAct = list(set(uniqueAct))
    
    print(uniqueAct, '\n')
'''