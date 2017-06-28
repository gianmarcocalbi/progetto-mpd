import re

f = open("inc/OrdonezA_Sensors.txt", "r")
f1 = open("inc/OrdonezA_ADLs.txt", "r")
no_blankS = open("no_blankSensors.txt", "w")
no_blankA = open("no_blankActivities.txt", "w")
c = []
c1 = []
count = 0
for line in f:
    if count != 0 and count != 1:
        line = re.sub("\\t+", ";", line)
        line = line[:-1]
        m = line.split(sep=";")
        no_blankS.write(line + ';\n')
        c.append(m)
    count += 1

count = 0
for line in f1:
    if count != 0 and count != 1:
        line = re.sub("\\t+", ";", line)
        line = line[:-1]
        m = line.split(sep=";")
        no_blankA.write(line + '\n')
        c1.append(m)
    count += 1   
    
print('Done.')
f.close()
f1.close()
no_blankS.close()
no_blankA.close()
