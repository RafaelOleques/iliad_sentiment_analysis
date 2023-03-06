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

#Metrics
from confusion_matrix import build_matrix
from metrics import accuracy_score, macro_recall, macro_precision, macro_specificity, f1_score

#sbert
from sentence_transformers import SentenceTransformer

class Trainer:

    def __init__(self, datapath, target):
        self.df = pd.read_csv(datapath)  
        self.target = target
        self.model = None
        self.ohe = OneHotEncoder()
        self.stopwords = []
        self.X = None
        self.y = None
        self.use_pipeline = True

    def remove_class(self, class_to_remove):
        '''
        Remove a specific class from the dataset

        df: dataframe
        class_to_remove: class to remove
        '''
        for target in class_to_remove:
            self.df = self.df[self.df[self.target] != target]

    def merge_class(self, class_to_merge, class_target):
        '''
        Merge to class of the dataframe and rename to "other"

        df: dataframe
        class_to_remove: class to remove
        '''
        self.df[self.target] = self.df[self.target].replace(class_to_merge, class_target)
        self.df[self.target] = self.df[self.target].replace(class_target, "other")


    def lemmatize_sentence(self, sentence):
        '''
        Remove stopwords and lemmatize a sentence

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
        One hot encode the target class

        target: target class

        return: one hot encoded targets
        '''
        y_temp = self.ohe.fit_transform(self.df[[self.target]])

        self.ohe.categories_

        y = y_temp.toarray()

        return y

    def sbert_embedding(self, X):
        '''
        Generate the sbert embeddings

        X: greek sentence

        return: sbert embedding
        '''
        self.sbert_model = SentenceTransformer('lighteternal/stsb-xlm-r-greek-transfer')
        
        return self.sbert_model.encode(X)
    

    def pre_procession(self, lemmatize, sbert):
        '''
        Operations of pre processing: lemmatization or sbert embeddings

        lemmatize: true if lemmatization, false otherwise
        ohe:  true if one hot enconding, false otherwise
        sbert: true if use sbert embedding, false otherwise
                If its true, lemmatize will be ignored

        return: lemmatized text and one hot encoded targets
        '''

        if sbert:
            X = self.sbert_embedding(self.df["greek text"].tolist())
            self.use_pipeline = False
        elif lemmatize:
            X = [self.lemmatize_sentence(x) for x in self.df["greek text"].tolist()]
        else:
            X = self.df["greek text"].tolist()

        y = self.one_hot_encoder()

        return X, y

    def prepare_data_to_train(self, lemmatize, sbert):
        '''
        Call pre processing function and assing the attributes X and y
        '''
        self.X, self.y = self.pre_procession(lemmatize=lemmatize, sbert=sbert)
    
    def cross_validation(self, model, nro_folds, shuffle=True, seed=42):
        '''
        Do k fold cross validation

        X: greek text
        y: target class
        model: model to be used
        nro_folds: number of folds
        lemmatize: true if lemmatization, false otherwise
        ohe:  true if one hot enconding, false otherwise
        shuffle: shuffle data
        seed: random seed
        class_to_remove: list of classes to be removed

        return: dict of metrics
        '''
        accuracy_list = []
        recall_list = []
        precision_list = []
        spec_list = []
        f1_list = []

        folds = k_folds(X=self.X, y=self.y, k=nro_folds, shuffle=shuffle, seed=seed)

        for (train_fold, test_fold) in folds:
            #Train and test
            X_train, y_train =  train_values(self.X, self.y, train_fold)
            X_test, y_test =  test_values(self.X, self.y, test_fold)
            
            #Model
            if self.use_pipeline:
                model_pipeline = Pipeline([
                ('vect', TfidfVectorizer(stop_words=self.stopwords)),
                ('clf', model),
                ])
            else:
                model_pipeline = Pipeline([('clf', model),])

            model_pipeline.fit(X_train, y_train)
            predicted = model_pipeline.predict(X_test)
            
            cm = build_matrix(y_test, predicted)
            
            accuracy = accuracy_score(cm)
            recall = macro_recall(cm)
            precision = macro_precision(cm)
            spec = macro_specificity(cm)
            f1 = f1_score(cm)
            
            accuracy_list.append(accuracy)
            recall_list.append(recall)
            precision_list.append(precision)
            f1_list.append(f1)
            spec_list.append(spec)

        metrics = {}

        metrics["accuracy"] = accuracy_list
        metrics["recall"] = recall_list
        metrics["precision"] = precision_list
        #metrics["especificity"] = spec_list
        metrics["f1"] = f1_list

        return metrics


        
