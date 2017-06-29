from import_me import *

def alignRawSensorData(pathRawSensData):
    sensData = []
    
    with open(pathRawSensData, "r") as f:
        count = 0
        for line in f:
            if count != 0 and count != 1:
                line = re.sub("\\t+", ";", line)
                if(line[-1:] == "\n"):                        
                    line = line[:-1]
                m = line.split(sep=";")
                for i in range(len(m)):
                    m[i] = m[i].strip().lstrip()
                sensData.append(m)
            count += 1
    
    return sensData 


def rawSensDataToJSON(pathRawSensData):
    sensor_set = alignRawSensorData(pathRawSensData)
    obs = []
    
    begin_time = timeStrToStamp(sensor_set[0][0])
    end_time = timeStrToStamp(sensor_set[len(sensor_set)-1][1])
    
    for t in range(math.ceil((end_time-begin_time)/60)):
        print(t)
        curr_obs = [0,0,0,0,0,0,0,0,0,0,0,0]
        or_bit = 0;
        
        for j in range(len(sensor_set)):
            j_begin_time = timeStrToStamp(sensor_set[j][0])
            j_end_time = timeStrToStamp(sensor_set[j][1])
            j_begin_offset = j_begin_time - begin_time
            j_end_offset = j_end_time - begin_time
        
            if t*60 <= j_begin_offset < (t+1)*60 or t*60 <= j_end_offset < (t+1)*60 or (j_begin_offset < t*60 and j_end_offset > (t+1)*60):
                curr_obs[ACT_DICT[sensor_set[j][2]]] = 1
                or_bit = 1
            
            j += 1
        
        obs.append({
            #"begin_time" : t*60+begin_time,
            "or_bit" : or_bit,
            "x" : curr_obs
        })
    return obs
    

def timeStrToStamp(strtime):
    return int(time.mktime(datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S").timetuple()))


def writeSensorDataToFile():
    with open("./refined_data/OrdonezA_Sensors_refined_" + str(int(time.time())) +".json", "w") as f:
        f.write(json.dumps(rawSensDataToJSON('./raw_data/OrdonezA_Sensors.txt'), sort_keys=True, separators=(',', ': ')))


if __name__ == '__main__':
    writeSensorDataToFile()