import re

f = open("C:/Users/Davide/Desktop/Modelli probabilistici - Progetto/OrdonezA_Sensors.txt","r")
count = 0
for line in f:
    if (count != 0 and count != 1):
        re.sub("\\s+",";",line)
        print(line)
f.close()
