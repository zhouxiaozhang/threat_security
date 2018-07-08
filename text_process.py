# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 16:01:53 2017

@author: zhou
"""
#preprocessing each line label str
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import pickle
import string
import nltk
def extract_articles(in_file):
    with open(in_file,"r") as f:
        clusters=f.read().strip("%%%").split("\n%%%")
    docs=[]
    labels=[]
    for i,cluster in enumerate(clusters):
        for text in cluster.strip().split('\n')[1:]:
            docs.append(text)
            labels.append(i)
    return docs,labels
def general_processing_file(list_text):
    stop_to_clearn=set(list(stopwords.words('english')))
    text_contain=[]
    for index,text in enumerate(list_text):
        single_text=[]
        for punctuate in string.punctuation:
            text=text.replace(punctuate,' ')
        #print text
        for digit in string.digits:
            text=text.replace(digit,'')
        text=nltk.word_tokenize(text.decode('utf-8'))
        #print text
        for word_c in text:
            #print word_c
            if len(word_c)>=3 and word_c not in stop_to_clearn :
                  word_c=WordNetLemmatizer().lemmatize(word_c)
                  word_c=word_c.lower()
                  single_text.append(word_c)
        text_contain.append(' '.join(single_text))
    return text_contain
                  
    
def text_processing(list_text):
    text_contain=[]
    stop_to_clearn=set(list(stopwords.words('english'))+['\n',',','.'])
    regex_non_alphanumeric=re.compile('[^0-9a-zA-Z]')
    #NLP Stemming,Lemmatization(maybe better)
    stemmer=PorterStemmer()
   # print 1
    for index,text in enumerate(list_text):
        single_text=[]
        for item in text.strip().split():
            item=regex_non_alphanumeric.sub('',item)
            item=item.lower()
            #item=stemmer.stem(item)
            single_text.append(item)
        clearned_list=[elem for elem in single_text if elem not in stop_to_clearn]
        text_contain.append(' '.join(clearned_list))
    return text_contain
#需要处理有待考证
def text_processing_rake(list_text):
    text_contain=[]
    #stop_to_clearn=set(list(stopwords.words('english'))+['\n',',','.'])
    regex_non_alphanumeric=re.compile('[^0-9a-zA-Z,.!?:;#$%&]')   
    for index,text in enumerate(list_text):
        single_text=[]
        for item in text.strip().split():
            item=regex_non_alphanumeric.sub('',item)
            item=item.lower()
            #item=stemmer.stem(item)
            single_text.append(item)
        #clearned_list=[elem for elem in single_text if elem not in stop_to_clearn]
        text_contain.append(' '.join(single_text))
    return text_contain



            
docs,labels=extract_articles('acl2017dataset/story_clusters.txt')            
text_list=text_processing(docs)    
text_key=text_processing_rake(docs)
text_list1=general_processing_file(docs)  
filename = 'process.txt'  
with open(filename, 'wb') as f:
    pickle.dump(text_list, f)    
filename1 = 'process_non.txt'  
with open(filename1, 'wb') as f:
    pickle.dump(text_key, f)      
            

            
            
            
        
    
    
    
    
