# import random

# for i in range(20):
#     print(random.randrange(0,3,2)-1)


import pickle

samples = [1,2,3,4,5,6]

with open("test.pkl",'wb') as handle:
    pickle.dumps(samples,handle)