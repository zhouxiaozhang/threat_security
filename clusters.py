# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 17:08:43 2018

@author: zhou
"""
import pickle
from gensim import matutils
from numpy import dot,array
import text_process
import feature_extract 
from feature_extract import Contentextraction,Content_extract,TFIDF
#import valid
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import linkage,dendrogram,fcluster
import numpy as np
import scipy.cluster.hierarchy as hierarchy
from matplotlib import pyplot as plt
from keywords_extraction import keywords_extraction

class clustering:
    def __init__(self,method='ward',metric='euclidean'):
        self.method =method
        self.metric =metric
    def fit(self,X):
        Z=linkage(X,method=self.method,metric=self.metric)
        max_d=0.47*np.max(Z[:,2])
        cluster=fcluster(Z,max_d,criterion='distance')
        return cluster
        
#lambda u,v:np.sqrt(((u-v)**2).sum())        
#dm=pdist(X,lambda u,v:np.sqrt(((u-v)**2).sum()))    
ytdist = [[i] for i in [662., 877., 255., 412., 996., 295., 468., 268.,400., 754., 564., 138., 219., 869., 669.]]    

#    
docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
text_list=text_process.general_processing_file(docs) 
wordvector_model=feature_extract.load_model('glove.6B.300d1') 
#content=TFIDF(model=wordvector_model,use_idf=True).fit(text_list) 
content=Contentextraction(method=2,model=wordvector_model,k=22,with_weight=True).fit(docs) 
#content=Content_extract(method=1,model=wordvector_model,with_weight=True,use_idf=True).fit(text_list)         
cluster=clustering(method='centroid',metric='euclidean').fit(content)
filename = 'clusters.txt'  
with open(filename, 'wb') as f:
    pickle.dump(cluster, f) 
#cluster1=clustering(method='ward',metric='euclidean').fit(content1)
#dn = dendrogram(cluster)
#dn1 = dendrogram(cluster1)
#plt.figure()
