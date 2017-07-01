from _header_ import *

"""
Quello che dice il mudo:

La procedura di stima dei parametri è OK (neanche loro hanno usato baum-welch)
Viterbi è OK

La procedura di "previsione" e test manca. Ecco cosa bisognerebbe fare:
=> Valutazione della performance del modello sulla previsione di una giornata
    di attività di una persona. Test Evaluation blabla

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

C = 'A'
C = C.upper()

def loadJsonDataSet():
    global C
    jobj = None
    with open("./refined_data/Ordonez" + C + "_refined.json") as rawjson:
        jobj = json.load(rawjson)
    return jobj


def CrossValidation():
    dataset = loadJsonDataSet(C)
    
    days_amount = 14
    
    for gg in range(1,days_amount+1):
        PI, T, O = train(dataset, gg)
        # evaluation(PI, T, O)
    
    
    return {} # oggetto da parsare per valutazione performance

#test_gg deve essere un numero compreso fra 1 e 14 per OrdonezA
#test_gg deve essere un numero compreso fra 1 e 21 per OrdonezB
def train(dataset, test_gg):
    PI = numpy.zeros(12)
    T = numpy.zeros((12,12))
    O = [
        {},{},{},{},{},{},{},{},{},{},{},{}
    ]
    
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
        if gg_count != test_gg
            # incrementa il conteggio dell'azione corrente di 1
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
           
    PI = preprocessing.normalize(act_count, norm='l1')
        
    T = preprocessing.normalize(trans_count_matrix, norm='l1')
    
    for act in O:
        act_tot = 0
        for obs_key in act:
            act_tot += act[obs_key]
        if act_tot != 0:
            for obs_key in act:
                act[obs_key] /= act_tot
    
    return PI, T, O
    

if __name__ == '__main__':
    pass