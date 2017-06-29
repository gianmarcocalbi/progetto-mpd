import re
import numpy as np
import pandas as pd
import scipy as sc

def align(pathSensData, pathAct):
    f = open(pathSensData, "r")
    lenF = len(f.readlines())
    f.close()

    f = open(pathSensData, "r")
    f1 = open(pathAct, "r")
    no_blankS = open("no_blankSensors.txt", "w")
    no_blankA = open("no_blankActivities.txt", "w")
    c = []
    c1 = []
    count = 0
    for line in f:
        if count != 0 and count != 1:
            line = re.sub("\\t+", ";", line)
            if(count!=lenF-1):                        
                line = line[:-1]
            m = line.split(sep=";")
            no_blankS.write(line + '\n')
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
    return c, c1


def main():
    sensor_set, activities_set = align('inc/OrdonezA_Sensors.txt', 'inc/OrdonezA_ADLs.txt')

    #List of activities without duplicates
    uniqueAct = [];
    for act in range(0,len(activities_set)):
        uniqueAct.append(activities_set[act][2])
    uniqueAct = list(set(uniqueAct))

    #List of data sensor without duplicates
    uniqueObs = [];
    for sens in range(0,len(sensor_set)):
        tupla = [sensor_set[sens][2],sensor_set[sens][3],sensor_set[sens][4]]
        uniqueObs.append(tupla)
    uniqueObs = [list(x) for x in set(tuple(x) for x in uniqueObs)]

    print(uniqueAct)
    print(len(uniqueAct))
    print("\n")
    print(uniqueObs)
    print(len(uniqueObs))