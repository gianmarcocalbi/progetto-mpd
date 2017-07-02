# -*- coding: utf-8 -*-
from _header_ import *

C = 'A'
C = C.upper()

def timeStrToStamp(strtime):
    return int(time.mktime(datetime.datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S").timetuple()))


def parseRawSensData(pathRawSensData):
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
                if m[2] == "Door":
                    m[2] += " " + m[4]
                sensData.append(m)
            count += 1
    
    return sensData 


def parseRawActData(pathRawActData):
    actData = []
    
    with open(pathRawActData, "r") as f:
        count = 0
        for line in f:
            if count != 0 and count != 1:
                line = re.sub("\\t+", ";", line)
                if(line[-1:] == "\n"):
                    line = line[:-1]
                m = line.split(sep=";")
                for i in range(len(m)):
                    m[i] = m[i].strip().lstrip()
                actData.append(m)
            count += 1       
            
    return actData


def alignData(pathRawSensData, pathRawActData):
    global C
    
    sensor_set = parseRawSensData(pathRawSensData)
    action_set = parseRawActData(pathRawActData)
    obsact = []
   
    begin_time_obs = timeStrToStamp(sensor_set[0][0])
    end_time_obs = timeStrToStamp(sensor_set[len(sensor_set)-1][1])
    begin_time_act = timeStrToStamp(action_set[0][0])
    end_time_act = timeStrToStamp(action_set[len(action_set)-1][1])
    
    begin_time = max(begin_time_act, begin_time_obs)
    end_time = max(end_time_act, end_time_obs)
    
    for t in range(math.ceil((end_time-begin_time)/60)):
        curr_obs = 0  #from binary array to decimal
        curr_max_act = {
            "j" : -1,
            "len" : 0
        }
        
        for j in range(len(sensor_set)):
            j_begin_time = timeStrToStamp(sensor_set[j][0])
            j_end_time = timeStrToStamp(sensor_set[j][1])
            j_begin_offset = j_begin_time - begin_time
            j_end_offset = j_end_time - begin_time
            
            if j_begin_offset < 0 or j_end_offset < 0:
                continue
        
            if t*60 <= j_begin_offset < (t+1)*60 or t*60 <= j_end_offset < (t+1)*60 or (j_begin_offset < t*60 and j_end_offset > (t+1)*60):
                curr_obs += pow(2,abs(OBS_DICT[C][sensor_set[j][2]] - 11))
        
        for j in range(len(action_set)):
            j_begin_time = timeStrToStamp(action_set[j][0])
            j_end_time = timeStrToStamp(action_set[j][1])
            j_begin_offset = j_begin_time - begin_time
            j_end_offset = j_end_time - begin_time
            b = 0
            e = 0
            
            if j_begin_offset < 0 or j_end_offset < 0:
                continue
            
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
        
        curr_obj = {
            "date" : t*60+begin_time,
            "x" : curr_obs
        }
        
        k = curr_max_act["j"]
        if k >= 0:
            curr_obj["act"] = ACT_DICT[action_set[k][2]]
        else:
            curr_obj["act"] = ACT_DICT["Idle/Unlabeled"]
    
        print(str.format("t->{0} - k={1} - x={2}", t, k, curr_obj))
    
        obsact.append(curr_obj)
    
    return obsact


    

def writeDataToFile():
    global C
    jobj = alignData("./raw_data/Ordonez" + C + "_Sensors.txt", "./raw_data/Ordonez" + C + "_ADLs.txt")
    with open("./refined_data/Ordonez" + C + "_refined_" + str(int(time.time())) +".json", "w") as f:
        f.write(json.dumps(
            jobj
            , separators=(",", ':')
        ))


if __name__ == '__main__':
    C = 'B' # A o B
    
    writeDataToFile()
    #print(parseRawActData('./raw_data/OrdonezA_ADLs.txt'))
    #parseRawSensData('./raw_data/OrdonezA_Sensors.txt')