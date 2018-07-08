# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:16:05 2017

@author: zhou
"""

import text_process
import feature_extract 

def main():
    docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
    text_list=text_process.text_processing(docs) 
    wordvector_model=feature_extract.load_model('glove.6B.300d') 
    content_vector=feature_extract.Content_extract(method=1,model=wordvector_model,with_weight=True,use_idf=True).fit(text_list)
    print content_vector