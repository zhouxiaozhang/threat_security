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
import rake
def load_model(model_path):
    #model=Word2Vec.load(model_path)
    #model = KeyedVectors.load_word2vec_format(model_path, binary=False)
    model=gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False) 
    return model
    
class Content_extract():
    def __init__(self,method,model,with_weight,use_idf):
        self.method=method
        self.model=model
        self.with_weight=with_weight
        self.use_idf=use_idf
        self.vectorizer=TfidfVectorizer(stop_words='english',use_idf=self.use_idf)
#    def compute_vector(self,tfidf_vector):
#        essays_vector=[]
#        tokens=self.vectorizer.get_feature_names()
#        #print len(tokens)
#        #5600
#        #print tokens
#        for article in tfidf_vector:
#            #print article.shape
#            context_vector=[]
#            for i,token in enumerate(tokens):
#                if token in self.model:
#                #print token
#                    word_vector=self.model[token]
#                    #print word_vector.shape
#                    weight=article[0,i]
#                    #print weight.shape
#                    word_vector= weight * word_vector 
#                    #print word_vector
#                    context_vector.append(word_vector)   
#            essays_vector.append(sum(context_vector))
#        return essays_vector
                    
    def fit(self,key_phase):
        essays_vector=[]
        for article_list in key_phase:
            context_vector=[]
            for key in article_list:
                tokens=key[1]
                tokens=tokens.strip().split()
                weight=key[0]
                for i,token in enumerate(tokens):
                    if token in self.model:
                        print token
                        word_vector=self.model[token]
                        #print weight.shape
                        word_vector= weight * word_vector 
                        #print word_vector
                        context_vector.append(word_vector)
            essays_vector.append(sum(context_vector))
        return essays_vector
     
       
docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
text_list=text_process.text_processing_key_words(docs)
key_phase=rake.rake()
wordvector_model=load_model('glove.6B.300d1') 
#essays_vector=[]
#for article_list in key_phase[0:1]:
#    context_vector=[]
#    for key in article_list:
#        tokens=key[1]
#        tokens=tokens.strip().split()
#        weight=key[0]
#        for i,token in enumerate(tokens):
#            if token in wordvector_model:
#                print token
#                word_vector=wordvector_model[token]
#                #print weight.shape
#                word_vector= weight * word_vector 
#                #print word_vector
#                context_vector.append(word_vector)
#    essays_vector.append(sum(context_vector))
#                
content=Content_extract(method=1,model=wordvector_model,with_weight=True,use_idf=True).fit(key_phase) 
        
        