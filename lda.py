# -*- coding: utf-8 -*-
"""
Created on Wed May 09 17:03:00 2018

@author: zhou
"""
import text_process
import re
from nltk.corpus import stopwords
from gensim import corpora,models
import pickle
def build_lda_model(input_data,num_topics=1):
    single_text=[]
    if isinstance(input_data,str):
        input_data=[input_data]
    input_data=text_process.general_processing_file(input_data)
    for data in input_data:
        texts=[elem for elem in data.strip().split()]
        single_text.append(texts)
    dictionary=corpora.Dictionary(single_text)
    corpus=[]
    corpus=[dictionary.doc2bow(text) for text in single_text]
    lda_model=models.ldamodel.LdaModel(corpus,num_topics=num_topics,id2word=dictionary)
    return lda_model
def get_topic(model,num_topics=1,num_words=15,with_weight=False):
    pattern=re.compile('([^ \*]*)\*([^ ]*)')
    result={}
    for topic_tuple in model.show_topics(num_topics,num_words):
        #print(topic_tuple)
        words=pattern.findall(topic_tuple[1])
        print words
        if with_weight:
              result[topic_tuple[0]]=[(term_tuple[1][1:-1],float(term_tuple[0])) for term_tuple in words]
        else:
             result[topic_tuple[0]]=[term_tuple[1][1:-1] for term_tuple in words]
    return result

docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
#text_key=text_process.text_processing_key_words(docs)

def test_keyword_extraction(docs):
    for doc in docs:
         doc1=u'Massive protests against Mohamed Morsi develop all over Egypt on the second anniversary of the 2011 revolution, including in Tahrir Square, where thousands of protesters gathered. At least 6 civilians and 1 police officer are shot dead in the Egyptian city of Suez, while 456 others are injured nationwide'
         #print doc
         model=build_lda_model(doc,1)
         topic_tokens=get_topic(model,with_weight=True)
         for topic_token in topic_tokens[0]:
             pass
             #print "%s" %(topic_token[1])
    return topic_tokens
docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt') 
topic_tokens=test_keyword_extraction(docs)
#print topic_tokens
#for topic in topic_tokens[0]:
#    a=topic[0]
#    b=a.encode("utf-8")
#    b=b[1:-1]
#    
