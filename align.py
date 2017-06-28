import re

f = open("C:/Users/Davide/Desktop/Modelli probabilistici - Progetto/OrdonezA_Sensors.txt", "r")
no_blank = open("C:/Users/Davide/Desktop/Modelli probabilistici - Progetto/no_blank.txt", "w")
c = []
count = 0
for line in f:
    if count != 0 and count != 1:
        line = re.sub("\\s+", ";", line)
        line = line[:-1]
        # print(line)
        m = line.split(sep=";")
        # print(m)
        no_blank.write(line + '\n')
        c.append(m)
        print(c)
    count += 1
f.close()
no_blank.close()
