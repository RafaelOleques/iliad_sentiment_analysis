import numpy as np
import random

def stratification(X,y,m,shuffle=True, seed=42):
    
    '''
    X: Training data, it can be a list or a numpy array of indexes
    y: Targets to be used in the stratification
    m: Number of folds
    Return: List (index) of stratified m folders 
    '''

    #Creating a list for every class

    narrator_list = []
    negative_list = []
    neutral_list = []
    positive_list = []

    for i in X:
        if y[i][0] == 1:
            narrator_list.append(i)
        if y[i][1] == 1:
            negative_list.append(i)
        if y[i][2] == 1:
            neutral_list.append(i)
        if y[i][3] == 1:
            positive_list.append(i)


    '''#Shuffle (senão sempre vai parcionar da mesma maneira) PRECISA FAZER?? TEM NO KFOLD.
    if shuffle:
        random.seed(seed)
        random.shuffle(narrator_list)
        random.shuffle(negative_list)
        random.shuffle(neutral_list)
        random.shuffle(positive_list)'''
    
    #Spliting every class 

    split_narrator = np.array_split(narrator_list,m)
    split_negative = np.array_split(negative_list,m)
    split_neutral = np.array_split(neutral_list,m)
    split_positive = np.array_split(positive_list,m)

    # Joining classes in stratified folders
    final_list = []
    one_fold = []
    
    for k in range(m):
        one_fold.extend(split_narrator[k])
        one_fold.extend(split_negative[k])
        one_fold.extend(split_neutral[k])
        one_fold.extend(split_positive[k])
        final_list.append(one_fold)
        one_fold = []

    #print("Lista final: ")
    #print(final_list)
    
    return final_list