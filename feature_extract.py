# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 10:48:28 2017

@author: zhou
"""
from numpy import dot,array
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import word2vec
from gensim.models.keyedvectors import KeyedVectors
import gensim
from gensim.models import Word2Vec
import text_process
from keywords_extraction import keywords_extraction
def load_model(model_path):
    #model=Word2Vec.load(model_path)
    #model = KeyedVectors.load_word2vec_format(model_path, binary=False)
    model=gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False) 
    return model

class TFIDF():
    def __init__(self,model,use_idf=True):
        self.use_idf=use_idf
        self.vectorizer=TfidfVectorizer(stop_words='english',use_idf=self.use_idf)
    def fit(self,articles):
        tfidf_keywords=self.vectorizer.fit_transform(articles)
        essays_vector=[]
        for article in tfidf_keywords:
            v=[0 for k in range(len(self.vectorizer.get_feature_names()))]
            #print len(v)
            #print len(self.vectorizer.get_feature_names())
            for j in range(len(self.vectorizer.get_feature_names())):
                v[j]=article[0,j]
            v=array(v,float)
            essays_vector.append(v)    
        return essays_vector
    
class Content_extract():
    def __init__(self,method,model,with_weight,use_idf):
        self.method=method
        self.model=model
        self.with_weight=with_weight
        self.use_idf=use_idf
        self.vectorizer=TfidfVectorizer(stop_words='english',use_idf=self.use_idf)
    def compute_vector(self,tfidf_vector):
        essays_vector=[]
        tokens=self.vectorizer.get_feature_names()
        for article in tfidf_vector:
            context_vector=[]
            for i,token in enumerate(tokens):
                if token in self.model:
                    word_vector=self.model[token]
                    #print word_vector.shape
                    weight=article[0,i]
                    #print weight
                    #print 1
                    word_vector= weight * word_vector 
                    context_vector.append(word_vector)   
            essays_vector.append(sum(context_vector))
        return essays_vector
                    
    def fit(self,articles):
        #vectorizer=TfidfVectorizer(stop_words='english',use_idf=self.use_idf)
        tfidf_keywords=self.vectorizer.fit_transform(articles)
        content=self.compute_vector(tfidf_keywords)
        return content
    

class Contentextraction():   
    def __init__(self,method,model,k,with_weight):
        self.method=method
        self.model=model
        self.with_weight=with_weight
        self.k=k
    def compute_vector(self,input_data):
        weights=None
        if isinstance(input_data,list):
            if len(input_data)==0:
                tokens=[]
            elif isinstance(input_data[0],tuple):
                tokens = [data_tuple[0] for data_tuple in input_data]
                weights = [data_tuple[1] for data_tuple in input_data] 
            else:
                tokens=input_data
        else:
            tokens=[item for item in input_data.strip().split()]
        context_vector=[]
        for word in tokens:
            if word in self.model:
                word_vector=self.model[word]
                if weights:
                    weight=weights[tokens.index(word)] 
                    word_vector=word_vector*weight
                context_vector.append(word_vector) 
        return sum(context_vector)       
        
        
    def fit(self,articles):
        essays_vector=[]
        for article in articles:
            keyword_list=keywords_extraction(article,method=self.method, k=self.k,with_weight=self.with_weight)
            content=self.compute_vector(keyword_list)
            essays_vector.append(content)
        return essays_vector
docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
#text_list=text_process.general_processing_file(docs) 
wordvector_model=load_model('glove.6B.300d1') 
content=Contentextraction(method=1,model=wordvector_model,k=22,with_weight=True).fit(docs) 
#content1=Content_extract(method=1,model=wordvector_model,with_weight=True,use_idf=True).fit(text_list)         
#content=TFIDF(model=wordvector_model,use_idf=True).fit(text_list)        
        
        
    