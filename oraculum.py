from import_me import *


class Oraculum:
    #obs = states = start_p = trans_p = emiss_p = None
    def __init__(self, c='A'):
        self.obs = list(OBS_DICT.values())
        self.states = list(ACT_DICT.values())
        c = c.upper()
        
        with open(str.format("./refined_data/Ordonez{0}_refined_start_probs.json", c)) as f:
            self.start_p = numpy.asarray(json.load(f))
            
        with open(str.format("./refined_data/Ordonez{0}_refined_trans_matrix.json", c)) as f:
            self.trans_p = numpy.asarray(json.load(f))
            
        with open(str.format("./refined_data/Ordonez{0}_refined_emiss_matrix.json", c)) as f:
            self.emiss_p = json.load(f)
    
    def extractXandAct(self, c='A'):
        c = c.upper()
        x = []
        act = []
        with open(str.format("./refined_data/OrdonezA_refined.json", c)) as f:
            data = json.load(f)
            for el in data:
                x.append(el["x"])
                act.append(el["act"])
        return x, act


def viterbi(prior, given_obs, trans_mat, obs_mat):
    # given_obs = [#1, #2, #3, #4, #5]   0  <= given_obs[i]  <= (2^12)-1
    #              t1  t2  t3  t4  t5
    
    most_likely_mat = []    #da rimepire con gli indici j
    most_likely_seq = []    #da riempire col massimo valore corrispondente alla colonna t
    
    prev_p = []
    
    for t in range(0,len(given_obs)):
        most_likely_mat.append([])
        #passo 0
        if t==0:
            for i in range(len(prior)):
                if str(given_obs[0]) in obs_mat[i]:
                    prev_p.append(prior[i] * obs_mat[i][str(given_obs[0])])
                else:
                    prev_p.append(0)
            #print(str.format("t={0} -> p={1}", t, prev_p))
        else:
            p = []
            
            # passo iterativo
            # per ogni azione (cioè per ogni stato dell'HMM)
            for i in range(len(prior)):
                # i -> indice che identifica lo stato corrente (in cui arrivo)
                max_p = 0
                max_j = 0
                
                # se l'osservazione corrente non è presente come chiave nella
                # matrice sparsa delle osservazioni, vuol dire che la prob
                # di osservarla nello stato corrente è uguale a 0, quindi devp
                # considerare solo i casi in cui tale probabilità è invece > 0
                # ovvero quanto l'osservazione è presente come chiave nella matr
                # delle osservazioni
                if str(given_obs[t]) in obs_mat[i]:
                    # prob di osservare l'osservazione corrente given_obs[t]
                    # nello stato i-esimo
                    # obs_mat[i][given_obs[t]] = P(i|E)
                    curr_state_prob = obs_mat[i][str(given_obs[t])]
                
                    # però posso arrivare in questo stato da 12 stati diversi
                    for j in range(len(prior)):
                        # j -> indice che identifica lo stato dal quale arrivo
                        
                        # per ognuno dei 12 stati dai quali posso arrivare devo moltiplicare curr_state_prob
                        # per la prob di arrivare nello stato corrente dallo stato j-esimo per la prob dello
                        # stato di partenza
                        # trans_mat[i][j] = P(i|j)
                        # prev_p[j] = P(j)
                        curr_p = curr_state_prob * prev_p[j] * trans_mat[j][i]
                        
                        # se la prob trovata è massima per lo stato i-esimo allora la setto
                        # come prob massima corrente
                        if curr_p > max_p:
                            max_p = curr_p
                            #salvo l'indice di arrivo del massimo
                            max_j = j
                    
                p.append(max_p)
                most_likely_mat[t].append(max_j)
            prev_p = p
            if sum(prev_p) == 0:
                print("There's no most likely sequence :( [t=" + str(t) + "]")
                exit()
                return None
            #print(str.format("t={0} -> p={1}", t, prev_p))
    
    #print(most_likely_mat)
    #print(prev_p.index(max(prev_p)))
    
    most_likely_seq.append(prev_p.index(max(prev_p)))
    
    t = len(most_likely_mat)-1;
    k = 0
    while t > 0:
        most_likely_seq.append(most_likely_mat[t][most_likely_seq[k]])
        t-=1
        k+=1
        
    return most_likely_seq[::-1]

def viterbiTest(test_index=0):
    
    if test_index == 1:
        print(viterbi(
            [0.5, 0.5],
            ["H", "H", "H", "H", "H", "H"],
            [
                [0.6, 0.4],
                [0.8, 0.2],    
            ],
            {
                0 : {
                    "H": 0.5,
                    "T" : 0.5
                },
                1 : {
                    "H" : 0.9,
                    "T" : 0.1
                }
            }
        ))
    elif test_index == 2:    
        print(viterbi(
            [0.48, 0.52],
            [3,1,6,6,6,4],
            [
                [0.83, 0.17],
                [0.40, 0.60],    
            ],
            {
                0 : {
                    "1" : 1/6,
                    "2" : 1/6,
                    "3" : 1/6,
                    "4" : 1/6,
                    "5" : 1/6,
                    "6" : 1/6
                },
                1 : {
                    "1" : 0.1,
                    "2" : 0.1,
                    "3" : 0.1,
                    "4" : 0.1,
                    "5" : 0.1,
                    "6" : 0.50
                }
            }
        ))
    else:
        # la soluzione dovrebbe essere
        # [0,0,1,0,0]
        print(viterbi(
            [0.5, 0.5], # a priori
            ["U", "U", "notU", "U", "U"], # evidenze
            [ # matrice di transizione
                [0.7, 0.3],
                [0.3, 0.7]
            ],
            { # oggetto "matrice" delle osservazioni
                0 : {
                    "U" : 0.9,
                    "notU" : 0.1
                },
                1 : {
                    "U": 0.2,
                    "notU" : 0.8
                }
            }
        ))

def numActArrayToStrActArray(numActArray):
    if numActArray == None:
        return []
    newarr = []
    for i in numActArray:
        newarr.append(ACT_DICT_REV[i])
    return newarr

if __name__ == '__main__':
    orac = Oraculum()
    x, act = orac.extractXandAct()
    #print(x)
    #print(act)
    #print(orac.start_p)
    #print(orac.trans_p)
    #print(orac.emiss_p)
    
    #exit()
    
    print(numActArrayToStrActArray(viterbi(
        orac.start_p,
        x,
        orac.trans_p,
        orac.emiss_p
    )))
    
    #viterbiTest(2)