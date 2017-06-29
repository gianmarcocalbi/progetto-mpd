from import_me import *


def timeStrToStamp(strtime):
    return int(time.mktime(datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S").timetuple()))


def alignRawSensData(pathRawSensData):
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
    sensor_set = alignRawSensData(pathRawSensData)
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
                curr_obs[OBS_DICT[sensor_set[j][2]]] = 1
                or_bit = 1
            
            j += 1
        
        obs.append({
            #"begin_time" : t*60+begin_time,
            "or_bit" : or_bit,
            "x" : curr_obs
        })
    return obs


def alignRawActData(pathRawActData):
    actData = []
    
    with open(pathRawActData, "r") as f:
        count = 0
        for line in f:
            if count != 0 and count != 1:
                line = re.sub("\\t+", ";", line)
                line = line[:-1]
                m = line.split(sep=";")
                for i in range(len(m)):
                    m[i] = m[i].strip().lstrip()
                actData.append(m)
            count += 1
            
    return actData


def rawActDataToJSON(pathRawActData):
    action_set = alignRawActData(pathRawActData)
    act = []
    
    begin_time = timeStrToStamp(action_set[0][0])
    end_time = timeStrToStamp(action_set[len(action_set)-1][1])
    
    for t in range(math.ceil((end_time-begin_time)/60)):
        curr_max_act = {
            "j" : -1,
            "len" : 0
        }
        
        for j in range(len(action_set)):
            j_begin_time = timeStrToStamp(action_set[j][0])
            j_end_time = timeStrToStamp(action_set[j][1])
            j_begin_offset = j_begin_time - begin_time
            j_end_offset = j_end_time - begin_time
            b = 0
            e = 0
            
            if j_begin_offset <= (t*60):
                b = t*60
            elif t*60 < j_begin_offset < (t+1)*60:
                b = j_begin_offset
            else: # j_begin_offset > (t+1)*60
                break
        
            if j_end_offset >= (t+1)*60:
                e = (t+1)*60
            elif t*60 < j_end_offset < (t+1)*60:
                e = j_end_offset
            else:
                continue
            
            if e-b > curr_max_act["len"]:
                curr_max_act = {
                    "j" : j,
                    "len" : e-b
                }
        
        k = curr_max_act["j"]
        if k >= 0:
            #print("t=" + str(t) + "; k=" + str(action_set[k][2]))
            act.append(
                ACT_DICT[action_set[k][2]]
            )
        else:
            #print("t=" + str(t) + "; k=" + str(k) + " begin_data='" + str(begin_time + t*60) + "'")
            act.append(
                -1    
            )
    return act
    

def writeSensDataToFile():
    with open("./refined_data/OrdonezA_Sensors_refined_" + str(int(time.time())) +".json", "w") as f:
        f.write(json.dumps(rawSensDataToJSON('./raw_data/OrdonezA_Sensors.txt'), sort_keys=True, separators=(',', ': ')))


def writeActDataToFile():
    with open("./refined_data/OrdonezA_ADLs_refined_" + str(int(time.time())) +".json", "w") as f:
        f.write(json.dumps(rawActDataToJSON('./raw_data/OrdonezA_ADLs.txt'), sort_keys=True, separators=(',', ': ')))



if __name__ == '__main__':
    writeSensorDataToFile()