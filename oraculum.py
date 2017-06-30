from import_me import *


class Oraculum:
    obs = states = start_p = trans_p = emit_p = None
    def __init__(self):
        obs = list(OBS_DICT.values())
        states = list(ACT_DICT.values())
        
        with open("./refined_data/OrdonezA_refined_start_probs.json") as f:
            start_p = numpy.asarray(json.load(f))
            
        with open("./refined_data/OrdonezA_refined_trans_matrix.json") as f:
            trans_p = numpy.asarray(json.load(f))
            
        with open("./refined_data/OrdonezA_refined_emiss_matrix.json") as f:
            emiss_p = json.load(f)

    def viterbi(self, prior, given_obs, trans_mat, obs_mat):
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
                    if given_obs[0] in obs_mat[i]:
                        prev_p.append(prior[i] * obs_mat[i][given_obs[0]])
                    else:
                        prev_p.append(0)
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
                    if given_obs[t] in obs_mat[i]:
                        # prob di osservare l'osservazione corrente given_obs[t]
                        # nello stato i-esimo
                        # obs_mat[i][given_obs[t]] = P(i|E)
                        curr_state_prob = obs_mat[i][given_obs[t]]
                    
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
        
        most_likely_seq.append(prev_p.index(max(prev_p)))
        
        t = len(most_likely_mat)-1;
        k = 0
        while t > 0:
            most_likely_seq.append(most_likely_mat[t][most_likely_seq[k]])
            t-=1
            k+=1
            
        return most_likely_seq


if __name__ == '__main__':
    oracle = Oraculum()
    print(oracle.viterbi(
        [0.5, 0.5],
        ["U", "U", "notU", "U", "U"],
        [
            [0.7, 0.3],
            [0.3, 0.7]
        ],
        {
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