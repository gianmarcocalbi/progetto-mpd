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


def rawDataToJSON(pathRawSensData, pathRawActData):
    sensor_set = alignRawSensData(pathRawSensData)
    action_set = alignRawActData(pathRawActData)
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
                curr_obs += pow(2,OBS_DICT[sensor_set[j][2]])
        
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
            #"begin_time" : t*60+begin_time,
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
    

def writeDataToFile():
    jobj = rawDataToJSON('./raw_data/OrdonezA_Sensors.txt', './raw_data/OrdonezA_ADLs.txt')
    with open("./refined_data/OrdonezA_refined_" + str(int(time.time())) +".json", "w") as f:
        f.write(json.dumps(
            jobj
            , separators=(",", ':')
        ))
        
    """
    start_probs, trans_matrix = computeProbs(jobj)
    with open("./refined_data/OrdonezA_refined_" + str(int(time.time())) +"_start_probs.json", "w") as f:
        f.write(json.dumps(
            start_probs
            , separators=(",", ':')
        ))
    with open("./refined_data/OrdonezA_refined_" + str(int(time.time())) +"_trans_matrix.json", "w") as f:
        f.write(json.dumps(
            trans_matrix
            , separators=(",", ':')
        ))
    """

def computeProbs(o):
    act_count = numpy.zeros(12)

    trans_count_matrix = numpy.zeros((12,12))

    prev_act = -1
    for x in o:
        curr_act = x["act"]
        act_count[curr_act] += 1
        if prev_act != -1:
            trans_count_matrix[prev_act][curr_act] = int(trans_count_matrix[prev_act][curr_act]+1)
        prev_act = curr_act
    
    start_prob = preprocessing.normalize(act_count, norm='l1')
        
    trans_prob_matrix = preprocessing.normalize(trans_count_matrix, norm='l1')
    
    return start_prob, trans_prob_matrix
    

if __name__ == '__main__':
    writeDataToFile()
    """
    with open("./refined_data/OrdonezA_refined_1498809985.json") as rawjson:
        jobj = json.load(rawjson)
        start_probs, trans_matrix = computeProbs(jobj)
        #print()
        with open("./refined_data/OrdonezA_refined_" + str(int(time.time())) +"_start_probs.json", "w") as f:
            f.write(json.dumps(
                start_probs.tolist()[0]
                , separators=(",", ':')
            ))
        with open("./refined_data/OrdonezA_refined_" + str(int(time.time())) +"_trans_matrix.json", "w") as f:
            f.write(json.dumps(
                trans_matrix.tolist()
                , separators=(",", ':')
            ))
    """