import pandas as pd
import numpy as np

#cross validation
from kfold import k_folds, train_values, test_values

from sklearn.pipeline import Pipeline

#preprocessing
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

#Processing greek text
import spacy
from spacy.lang.el.examples import sentences 

#Metrics => MUDAR PARA AS NOSSAS
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

class Trainer:

    def __init__(self, datapath, target):
        self.df = pd.read_csv(datapath)  
        self.target = target
        self.metrics = {}
        self.model = None
        self.ohe = OneHotEncoder()
        self.stopwords = []


    def remove_class(self, class_to_remove):
        '''
        df: dataframe
        class_to_remove: class to remove
        '''
        for target in class_to_remove:
            self.df = self.df[self.df[self.target] != target]

    def merge_class(self, class_to_merge, class_target):
        '''
        df: dataframe
        class_to_remove: class to remove
        '''
        self.df[self.target] = self.df[self.target].replace(class_to_merge, class_target)
        self.df[self.target] = self.df[self.target].replace(class_target, "other")




    def lemmatize_sentence(self, sentence):
        '''
        sentence: greek sentence

        return: lemmatized greek sentence as string
        '''
        lemma_list = []
        
        nlp = spacy.load("el_core_news_md")
        self.stopwords = nlp.Defaults.stop_words

        doc = nlp(sentence)
        
        lemma_list= [token.lemma_ for token in doc if token.pos_ != "PUNCT"] 
        
        return " ".join(lemma_list)

    def one_hot_encoder(self):
        '''
        target: target class

        return: one hot encoded targets
        '''
        y_temp = self.ohe.fit_transform(self.df[[self.target]])

        self.ohe.categories_

        y = y_temp.toarray()

        return y
    

    def pre_procession(self, lemmatize, ohe):
        '''
        lemmatize: true if lemmatization, false otherwise
        ohe:  true if one hot enconding, false otherwise

        return: lemmatized text and one hot encoded targets
        '''
        if lemmatize:
            X = [self.lemmatize_sentence(x) for x in self.df["greek text"].tolist()]
        else:
            X = self.df["greek text"].tolist()

        if ohe:
            y = self.one_hot_encoder()
        else:
            y = self.df["class"].values.tolist()

        return X, y

    def cross_validation(self, model, nro_folds, lemmatize, ohe, shuffle=True, seed=42):
        '''
        X: greek text
        y: target class
        model: model to be used
        nro_folds: number of folds
        lemmatize: true if lemmatization, false otherwise
        ohe:  true if one hot enconding, false otherwise
        shuffle: shuffle data
        seed: random seed
        class_to_remove: list of classes to be removed
        '''

        X, y = self.pre_procession(lemmatize, ohe)
        folds = k_folds(X=X, y=y, k=nro_folds, shuffle=shuffle, seed=seed)

        accuracy_list = []
        recall_list = []
        precision_list = []

        for (train_fold, test_fold) in folds:
            #Train and test
            X_train, y_train =  train_values(X, y, train_fold)
            X_test, y_test =  test_values(X, y, test_fold)
            
            #Naive Bayes
            model_pipeline = Pipeline([
                ('vect', TfidfVectorizer(stop_words=self.stopwords)),
                ('clf', model),
                ])

            model_pipeline.fit(X_train, y_train)
            predicted = model_pipeline.predict(X_test)

            accuracy = accuracy_score(y_test, predicted, normalize=False)
            recall = recall_score(y_test, predicted, average='macro') * 100
            precision = precision_score(y_test, predicted, average='macro') * 100
            
            accuracy_list.append(accuracy)
            recall_list.append(recall)
            precision_list.append(precision)
    
        self.metrics["accuracy"] = accuracy_list
        self.metrics["recall"] = recall_list
        self.metrics["precision"] = precision_list

    def get_metrics(self):
        '''
        returns all the metrics
        '''
        return self.metrics


    def get_metric(self, metric):
        '''
        metric: the metric name

        return the specified metric
        '''
        return self.metrics[metric]

        
