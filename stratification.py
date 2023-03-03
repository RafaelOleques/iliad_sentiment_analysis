import numpy as np
import random

def stratification(y,m,shuffle=True,seed=42):
    
    '''
    y: Targets to be used in the stratification
    m: Number of folds

    Return: Stratified m folders index list -> [[fold1],[fold2], ... ,[foldm]]
    '''

    #y to string (key to dictionary)
    y_str = []
    for i in range(len(y)):
        s = " ".join(str(e) for e in y[i])
        y_str.append(s)
        s = []


    d = {}

    for i in range(len(y)):
        if (y_str[i] in d):         #If key already in dictionary
            d[y_str[i]].append(i)   #Put index on class list
        else:
            d[y_str[i]] = [i]       #Else create/start class list with first index

    '''
    #Visualizar o dicionário
    for key, value in d.items():
        print(key, ':', value)
        print(len(value))
    '''
    
    #Splits classes and shuffle
    for key in d:
        if shuffle:
            random.seed(seed)
            random.shuffle(d[key])
        d[key] = np.array_split(d[key],m)

    #Joining classes: first split of every class make first fold and so on
    folds_list = []
    one_fold = []
    
    for j in range(m):
        for key in d:
            one_fold.extend(d[key][j])
        folds_list.append(one_fold)
        one_fold = []   

    return folds_list