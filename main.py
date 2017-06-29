import re
import numpy
import scipy
import json
import time
import datetime
import math
import sys

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

ACT_DICT = {
    'Basin' : 0,
    'Bed' : 1,
    'Cabinet' : 2,
    'Cooktop' : 3,
    'Cupboard' : 4,
    'Fridge' : 5,
    'Maindoor' : 6,
    'Microwave' : 7,
    'Seat' : 8,
    'Shower' : 9,
    'Toaster' : 10,
    'Toilet' : 11
}

def alignSensorData(pathRawSensData):
    no_blankS = open("no_blankSensors.txt", "w")
    sensData = []
    
    with open(pathRawSensData, "r") as f:
        sens = numpy.zeros((0,5))
        count = 0
        for line in f:
            if count != 0 and count != 1:
                line = re.sub("\\t+", ";", line)
                if(line[-1:] == "\n"):                        
                    line = line[:-1]
                m = line.split(sep=";")
                no_blankS.write(line + '\n')
                for i in range(len(m)):
                    m[i] = m[i].strip().lstrip()
                sensData.append(m)
            count += 1
    
    print('Aligned files saved.\n')
    return sensData 

def rawSensDataToJSON(pathRawSensData):
    sensor_set = alignSensorData(pathRawSensData)
    #print(json.dumps(sensor_set))
    
    obs = []
    
    
    begin_time = timeStrToStamp(sensor_set[0][0])
    end_time = timeStrToStamp(sensor_set[len(sensor_set)-1][1])
    
    
    """
    j_begin_time j_end_time
       begin_time = 1240930 0139012 < t1
        0239323 < t0 < 2323232
        4923819 ... 3914832
        3409420 3948943 = end_time
        
    
    000 090
    060 100
    070 080
    100 800
    200 300
    
    
    t = 0
    x = [0]
    
    t = 1 -> [60,120)
    x = [0,1,2,3]
    
    t = 2 -> [120,180)
    x = [3,4]
    
    t = 3
    
    
    """
    first_index = 0
    last_index = 0
    
    for t in range(math.ceil((end_time-begin_time)/60)):
        print(t)
        curr_obs = [0,0,0,0,0,0,0,0,0,0,0,0]
        j = first_index
        j_is_first = True
        or_bit = 0;
        while j < len(sensor_set):
            try:
                j_begin_time = timeStrToStamp(sensor_set[j][0])
                j_end_time = timeStrToStamp(sensor_set[j][1])
                j_begin_offset = j_begin_time - begin_time
                j_end_offset = j_end_time - begin_time
            except Exception as e:
                print("Error when t=" + str(t) + " & j=" + str(j) + " :: " + str(e))
                input("")
                break
            
            #print(str.format("t={0} -> j_begin_time={1} ; j_end_time={2} :: j={3}", t, j_begin_time, j_end_time, j))
            #print(str.format("t={0} -> j_begin_offset={1} ; j_end_offset={2}", t, j_begin_offset, j_end_offset))
            #input("")
            if j_begin_offset <= t*60:
                if j_end_offset > t*60: # t*60 è giusto! (t+1)*60 non va bene
                    if(j_is_first):
                        first_index = j
                        j_is_first = False
                    curr_obs[ACT_DICT[sensor_set[j][2]]] = 1
                    or_bit = 1
            j += 1
        
        obs.append({
            "begin_time" : t*60+begin_time,
            "or_bit" : or_bit,
            "x" : curr_obs
        })
        
    return obs

def timeStrToStamp(strtime):
    return int(time.mktime(datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S").timetuple()))
    

def main():
    sensor_set = align('inc/OrdonezA_Sensors.txt', 'inc/OrdonezA_ADLs.txt')


    #List of data sensors without duplicates
    uniqueObs = [];
    for sens in range(0,len(sensor_set)):
        tupla = [sensor_set[sens][2],sensor_set[sens][3],sensor_set[sens][4]]
        uniqueObs.append(tupla)
    uniqueObs = [list(x) for x in set(tuple(x) for x in uniqueObs)]
   
    
    print(uniqueObs, '\n')
    
    #Partendo dalla data della prima rilevazione si aggiungono 60 sec per 
    startTimeSens = sensor_set[sens][0]
    print(startTimeSens)
    
    '''
    1. Aggiungo 1 minuto allo startTimeSens: ho creato il primo dt
    2. Creo una observation di tutti 0
    3. Creo un ciclo for che controlla tutte le registrazioni dei sensori:
        se le registrazioni stanno in dt allora si controlla, per ognuna, quale sensore 
        (sotto forma di tripla) e' attivo e si porta il suo valore a 1 nella observation 
    4. Si salva l'array di 12 elementi in una matrice di osservazioni
    5. Si ripetono i punti da 1 a 3 fino a che non si raggiunge l'END dell'ultima registrazione
        nel dataset
    
    la struttura dati che contiene tutte ls istanze e' del tipo json-like:
    o = [
        {
            "or_bit" : 1,
            "x" : [
                0,0,0,0,0,0,0,0,0,0,0,1
            ]
        }
        #etc...
    ]
    
    '''

def run():
    with open("temp_output.json", "w") as f:
        f.write(json.dumps(rawSensDataToJSON('inc/OrdonezA_Sensors.txt'), sort_keys=True, separators=(',', ': ')))
    #rawSensDataToJSON('inc/OrdonezA_Sensors.txt')