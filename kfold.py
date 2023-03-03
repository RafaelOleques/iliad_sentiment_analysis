import numpy as np
import random
from stratification import stratification


def k_folds(k, X, y, shuffle=True, seed=42):
    '''
    k: Number of k folds
    X: Training data, it can be a list or a numpy array (stratification will be aplicated inside this function)
    y: Targets to be used in the stratification
    shuffle: True if want shuffle list values
    seed: Seed to shuffle

    Return: List of tuples in the format: (train_folds, test_folds), being train_folds and test_folds a list of indexes
    '''

    #Index list
    idx_list = [idx for idx, value in enumerate(X)]

    #List to numpy array
    idx_list = np.array(idx_list)

    #Shuffle
    if shuffle:
        random.seed(seed)
        random.shuffle(idx_list)
    
    #Get stratificaded folds
    folds = stratification(y, k)

    final_folds = []

    #Cross validation loop
    for idx_test, test_fold in enumerate(folds):
        #Matrix of folds that will be used as train in this iteration
        folds_list = [fold for idx_train, fold in enumerate(folds) if idx_train != idx_test]
        folds_tuple = tuple(folds_list)

        #Train folds concat in on array
        train_fold = np.concatenate(folds_tuple, axis=None)

        #Saving
        final_folds.append((train_fold, test_fold))

    return final_folds

def train_values(X, y, train_fold):
    X_train = [x for idx, x in enumerate(X) if idx in train_fold]
    y_train = [target for idx, target in enumerate(y) if idx in train_fold]

    return X_train, y_train

def test_values(X, y, test_fold):
    X_test = [x for idx, x in enumerate(X) if idx in test_fold]
    y_test = [target for idx, target in enumerate(y) if idx in test_fold]

    return X_test, y_test