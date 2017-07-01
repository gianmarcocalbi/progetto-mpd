from import_me import *
from hidden_markov import *

numpy.set_printoptions(threshold=numpy.nan)

def extractXandAct(c='A'):
    c = c.upper()
    x = []
    act = []
    with open(str.format("./refined_data/OrdonezA_refined.json", c)) as f:
        data = json.load(f)
        for el in data:
            x.append(el["x"])
            act.append(el["act"])
    return x, act

states = (
    'Breakfast',
    #'Dinner',
    #'Drink',
    'Grooming',
    "Idle/Unlabeled",
    'Leaving',
    'Lunch',
    'Showering',
    'Sleeping',
    'Snack',
    "Spare_Time/TV",
    'Toileting'
)

"""
'Basin',
'Bed',
'Cabinet',
'Cooktop',
'Cupboard',
'Fridge',
'Maindoor',
'Microwave',
'Seat',
'Shower',
'Toaster',
'Toilet'
"""

possible_observation = tuple(range(4096))

c = 'A'

with open(str.format("./refined_data/Ordonez{0}_refined_start_probs.json", c)) as f:
    start_probability = numpy.delete(numpy.matrix(json.load(f)), [1,2], axis=1)

with open(str.format("./refined_data/Ordonez{0}_refined_trans_matrix.json", c)) as f:
    transition_probability = numpy.matrix(json.load(f))
    transition_probability = numpy.delete(transition_probability, [1,2], axis=0)
    transition_probability = numpy.delete(transition_probability, [1,2], axis=1)

with open(str.format("./refined_data/Ordonez{0}_refined_emiss_matrix.json", c)) as f:
    raw_emission_object = json.load(f)

emission_object = []

for act in raw_emission_object:
    curr_emiss_array = numpy.zeros(4096)
    for i in range(4096):
        if str(i) in act:
            curr_emiss_array[i] = act[str(i)]
    emission_object.append(curr_emiss_array)


emission_probability = numpy.matrix(emission_object)
emission_probability = numpy.delete(emission_probability, [1,2], axis=0)
emission_probability[8,0] += 0.00011609000000001313

#print(numpy.sum(emission_probability,axis=1))

#for i in range(10):
    #print(str.format("Line i={0} as total prob={1}", i, emission_probability[i].any()))

test = hmm(states, possible_observation, start_probability, transition_probability, emission_probability)

x, act = extractXandAct('A')

observations = tuple(x[0:300])

"""
TRAINING DOESN'T WORK :(
obs4 = tuple(x[2040:2640])
observation_tuple = []
observation_tuple.extend( [observations,obs4] )
quantities_observations = [600, 600]
num_iter=1000
e,t,s = test.train_hmm(observation_tuple,num_iter,quantities_observations)
# e,t,s contain new emission transition and start probabilities
print(e)
"""

print(test.viterbi(observations))

#print("Forward test probability:\n" + str(test.forward_algo(observations)))
