# -*- coding: utf-8 -*-
from _header_ import *

"""
for i da 1 a N=# di giorni nel SET (OrdonezA) # sono 14 giorni mi sembra
    gg = giorno i-esimo
    # il giorno gg diventa il candidato per il test-set
    1) stimo i parametri dell'HMM (== le matrici: trans, priori, modello sensoriale)
        su tutti i giorni del SET escluso gg
    2) uso le rilevazioni dei sensori di gg come evidenze emesse
    3) faccio viterbi (calcolo la MLS)
    # quindi ho usato i giorni escluso gg come "training set" e gg invece come
    # test set, dunque ho fatto una sorta di cross validation
    
    4) confronto la MLS tirata fuori da viterbi per il giorno gg con la sequenza
        di azioni del giorno gg fornita nel set OrdonezA
    5) faccio la perf evaluation
    # ripeto questi punti per ogni giorno nel set (in OrdonezA ci sono 14 gg)

# poi 
faccio la media delle perf. evaluation e così ottengo l'evaluation dell'HMM sul
set OrdonezA su un task di "previsione" della durata di un giorno
"""

C = 'B' # non modificare qui ma in fondo al file
C = C.upper()

def loadJsonDataSet():
    global C
    jobj = None
    with open("./refined_data/Ordonez" + C + "_refined.json") as rawjson:
        jobj = json.load(rawjson)
    return jobj


def extractEandX(dataset):
    E = []
    X = []
    for item in dataset:
        E.append(item["x"])
        X.append(item["act"])
    return E, X


def CrossValidation():
    dataset = loadJsonDataSet()
    
    days_amount = 21
    
    if C == 'A':
        days_amount = 14
        
    cmxs = []
    
    for gg in range(1,days_amount+1):
        PI, T, O, E, X = train(dataset, gg)
        mls = viterbi(PI, T, O, E)
    
        if len(X) != len(mls):
            raise Exception("Performance eval failed")
            exit()
        
        cmx = confusion_matrix(X, mls)
        cmxs.append(cmx)
    
    avg_cmx = numpy.zeros((len(ACT_DICT), len(ACT_DICT)))
    
    for cmx in cmxs:
        avg_cmx = numpy.add(avg_cmx,cmx)
    
    avg_cmx = numpy.divide(avg_cmx, len(ACT_DICT))
    
    return evalPerformance(avg_cmx)
    
    


#test_gg deve essere un numero compreso fra 1 e 14 per OrdonezA
#test_gg deve essere un numero compreso fra 1 e 21 per OrdonezB
#test_gg è il giorno scelto come giorno di test, non verrà utilizzato nel calcolo dei parametri nella funzione "train"
def train(dataset, test_gg):
    #PI è il vettore delle probabilità a priori
    PI = numpy.zeros(12)
    #T è la matrice di transizione
    T = numpy.zeros((12,12))
    #O è la matrice di emissione delle osservazioni
    O = [
        {},{},{},{},{},{},{},{},{},{},{},{}
    ]
    # Array di evidenze nel giorno test_gg
    E = []
    
    # Array delle azioni (nascoste) nel giorno test_gg
    X = []
    
    prev_act = -1
    prev_gg = 0
    gg_count = 0
    for item in dataset:
        curr_act = item["act"]
        curr_date = item["date"]
        curr_obs = item["x"]
        curr_gg = int(datetime.datetime.fromtimestamp(int(curr_date)).strftime('%d'))
        
        if prev_gg != curr_gg:
            gg_count += 1
            prev_gg = curr_gg
        
        # salta le istanze del giorno di test (test_gg)
        if gg_count != test_gg:
            # incrementa il conteggio dell'attività corrente di 1
            PI[curr_act] += 1
            
            # se prev_act == -1 allora si tratta del primo item del dataset
            # quindi non c'è niente da inserire nella matrice T di transizione
            if prev_act != -1:
                # altrimenti incrementa di 1 l'elemento T[i,j] con
                # i = stato (azione) da cui parti (prev_act)
                # j = stato (azione) in cui giungi (curr_act)
                T[prev_act][curr_act] = int(T[prev_act][curr_act]+1)
                # int() per assicurarci che non ci siano errori sulle somme che risultino in:
                # 1.00000000000000000000001 (double)
                # 1 (int)
            prev_act = curr_act
            
            # O è in un "formato" compatto per la rappresentazione di matrici sparse:
            # per ogni Azione è presente un oggetto che ha come chiavi il numero dell'
            # osservazione e come valore il conteggio di tale osservazione, se un'osservazione
            # non viene mai riscontrata per un'azione allora non c'è la chiave
            
            # se curr_obs non è già presente come chiave
            if curr_obs not in O[curr_act]:
                # aggiungi il campo 
                O[curr_act][curr_obs] = 1
            else:
                # incrementa il campo
                O[curr_act][curr_obs] += 1
        else:
            E.append(curr_obs)
            X.append(curr_act)
           
    PI = preprocessing.normalize(PI, norm='l1')[0]
        
    T = preprocessing.normalize(T, norm='l1')
    
    for act in O:
        act_tot = 0
        for obs_key in act:
            act_tot += act[obs_key]
        if act_tot != 0:
            for obs_key in act:
                act[obs_key] /= act_tot
    
    return PI, T, O, E, X


def evalPerformance(cmx):
    N = len(ACT_DICT)
    sensitivity = numpy.zeros(N)
    specificity = numpy.zeros(N)
    precision = numpy.zeros(N)
    accuracy = numpy.zeros(N)
    f_measure = numpy.zeros(N)
    tot_accuracy = 0
    tot_f_measure = 0
    
    TP = numpy.zeros(N)
    FP = numpy.zeros(N)
    TN = numpy.zeros(N)
    FN = numpy.zeros(N)
        
    for i in range(N):
        TP[i] = cmx[i,i]
        FP[i] = numpy.sum(cmx[[i],:])-TP[i]
        FN[i] = numpy.sum(cmx[:,[i]])-TP[i]
        TN[i] = numpy.sum(numpy.delete(numpy.delete(cmx,(i),axis=1),(i),axis=0))
    
    for i in range(N):
        sensitivity[i] = TP[i]/(TP[i]+FN[i])
        specificity[i] = TN[i]/(TN[i]+FP[i])
        precision[i] = TP[i]/(TP[i]+FP[i])
        accuracy[i] = (TP[i]+TN[i])/(TP[i]+FN[i]+TN[i]+FP[i])
        if numpy.isnan(sensitivity[i]):
            sensitivity[i] = 0
        if numpy.isnan(specificity[i]):
            specificity[i] = 0
        if numpy.isnan(precision[i]):
            precision[i] = 0
        if numpy.isnan(accuracy[i]):
            accuracy[i] = 0
        f_measure[i] = (2*precision[i]*sensitivity[i])/(precision[i]+sensitivity[i])
        if numpy.isnan(f_measure[i]):
            f_measure[i] = 0
        else:
            tot_f_measure += f_measure[i]
    
    tot_f_measure /= N
    
    #tot_sensitivity = numpy.sum(TP)/(numpy.sum(TP)+numpy.sum(FN))
    #tot_specificity = numpy.sum(TN)/(numpy.sum(TN)+numpy.sum(FP))
    #tot_precision = numpy.sum(TP)/(numpy.sum(TP)+numpy.sum(FP))
    
    if numpy.sum(cmx)!=0:
        tot_accuracy = numpy.sum(TP)/numpy.sum(cmx)
    else:
        tot_accuracy = 0    
    
    return accuracy, precision, sensitivity, specificity, tot_accuracy, tot_f_measure
    

def confusion_matrix(expected, predicted):
    if len(expected) != len(predicted):
        raise Exception("I and J have different length in confusion_matrix(I,J)")
    
    mtx = numpy.zeros((len(ACT_DICT), len(ACT_DICT)))
    
    for i in range(len(expected)):
        mtx[expected[i], predicted[i]] += 1
    
    return mtx


def viterbi(PI, T, O, E):
    # E = [#1, #2, #3, #4, #5]   0  <= E[i]  <= (2^12)-1
    #              t1  t2  t3  t4  t5
    
    # Matrice contenente gli indici j per ricostruire a ritroso il percorso
    most_likely_mat = []
    
    # Most likely sequence
    most_likely_seq = []
    
    # Array delle probabilità uscenti dagli stati precedenti
    prev_p = []
    
    # cicla da t0 a tf==# di osservazioni emesse
    for t in range(len(E)):
        # istanzia un nuovo array per le prob al tempo t
        most_likely_mat.append([])
        
        # array delle probabilità al tempo t corrente
        p = []
        
        if t==0:
            # passo per t = 0
            # usando le probabilità a priori
            for i in range(len(PI)):
                #print("str(E[t])=" + str(E[t]))
                #print("O[i]=" + str(O[i].keys()))
                #print("O[i] keys type=" + str(type(list(O[i].keys())[0])))
                #input()
                if E[0] in O[i]:
                    p.append(PI[i] * O[i][E[0]])
                else:
                    p.append(0)
            #print(str.format("t={0} -> p={1}", t, prev_p))
        else:
            # passo iterativo per t > 0
            # per ogni azione (cioè per ogni stato dell'HMM)
            for i in range(len(PI)):
                # i -> indice che identifica lo stato corrente (in cui arrivo)
                max_p = 0
                max_j = 0
                
                # se l'osservazione corrente non è presente come chiave nella
                # matrice sparsa delle osservazioni, vuol dire che la prob
                # di osservarla nello stato corrente è uguale a 0, quindi devp
                # considerare solo i casi in cui tale probabilità è invece > 0
                # ovvero quanto l'osservazione è presente come chiave nella matr
                # delle osservazioni
                if E[t] in O[i]:
                    # prob di osservare l'osservazione corrente E[t]
                    # nello stato i-esimo
                    # O[i][E[t]] = P(i|E)
                    curr_state_prob = O[i][E[t]]
                
                    # però posso arrivare in questo stato (i) da 12 stati diversi
                    for j in range(len(PI)):
                        # j -> indice che identifica lo stato dal quale arrivo
                        
                        # per ognuno dei 12 stati dai quali posso arrivare devo moltiplicare curr_state_prob
                        # per la prob di arrivare nello stato corrente dallo stato j-esimo per la prob dello
                        # stato di partenza
                        # T[j][i] = P(i|j)
                        # prev_p[j] = P(j)
                        curr_p = curr_state_prob * prev_p[j] * T[j][i]
                        
                        # se la prob trovata è massima per lo stato i-esimo allora la setto
                        # come prob massima corrente
                        if curr_p > max_p:
                            max_p = curr_p
                            # salvo l'indice di arrivo del massimo
                            max_j = j
                
                p.append(max_p)
                most_likely_mat[t].append(max_j)
        
        prev_p = p
        
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


# Funzione per testare l'algoritmo di Viterbi con problemi 
# svolti in classe la cui soluzione è nota
def viterbiTest(test_index=0):
    PI = None
    T = None
    O = None
    E = None
    if test_index == 1:
        X = [1,0,1,0,1,0]
        PI = [0.5, 0.5]
        T = [
            [0.6, 0.4],
            [0.8, 0.2],    
        ]
        O = {
            0 : {
                "H": 0.5,
                "T" : 0.5
            },
            1 : {
                "H" : 0.9,
                "T" : 0.1
            }
        }
        E = ["H", "H", "H", "H", "H", "H"]
    elif test_index == 2:
        X = [0,0,1,1,1,0]
        PI = [0.48, 0.52]
        T = [
            [0.83, 0.17],
            [0.40, 0.60],    
        ]
        O = {
            0 : {
                1 : 1/6,
                2 : 1/6,
                3 : 1/6,
                4 : 1/6,
                5 : 1/6,
                6 : 1/6
            },
            1 : {
                1 : 0.1,
                2 : 0.1,
                3 : 0.1,
                4 : 0.1,
                5 : 0.1,
                6 : 0.50
            }
        }
        E = [3,1,6,6,6,4]
    else:
        # la soluzione dovrebbe essere
        # [0,0,1,0,0]
        PI = [0.5, 0.5] # a priori
        T = [ # matrice di transizione
            [0.7, 0.3],
            [0.3, 0.7]
        ]
        O = { # oggetto "matrice" delle osservazioni
            0 : {
                "U" : 0.9,
                "notU" : 0.1
            },
            1 : {
                "U": 0.2,
                "notU" : 0.8
            }
        }
        E = ["U", "U", "notU", "U", "U"] # evidenze


    print(viterbi(PI,T,O,E))


def numActArrayToStrActArray(numActArray):
    if numActArray == None:
        return []
    newarr = []
    for i in numActArray:
        newarr.append(ACT_DICT_REV[i])
    return newarr


if __name__ == '__main__':
    C = 'B'
    
    accuracy, precision, sensitivity, specificity, tot_accuracy, tot_f_measure = CrossValidation()
    
    print("------------")
    print("SET : ", C)
    print("------------")
    print("ACCURACY VECTOR:")
    print(accuracy , "\n")
    print("PRECISION VECTOR:")
    print(precision,"\n")
    print("SENSITIVITY VECTOR:")
    print(sensitivity, "\n")
    print("SPECIFICITY VECTOR:")
    print(specificity,"\n")
    print("TOTAL ACCURACY:")
    print(tot_accuracy, "\n")
    print("TOTAL F-MEASURE:")
    print(tot_f_measure)
    print("------------")
    
    #dataset = loadJsonDataSet()
    #PI, T, O, E, X = train(dataset, 11)
    
    #print(str.format("lengths --> PI={0}; T={1}; O={2}; E={3}; X={4}", len(PI), len(T), len(O), len(E), len(X)))
    #E, X = extractEandX(dataset)
    
    #mls = viterbi(PI, T, O, E)
    #print(numActArrayToStrActArray(mls))