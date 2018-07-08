# -*- coding: utf-8 -*-
from rake_nltk import Rake
from nltk.tokenize import sent_tokenize
import jieba.analyse
import text_process
import textrank
import lda
import pickle
import nltk
def keywords_extraction(article,method, k=20,with_weight=False):
    doc=""
    if method==0:
        model=lda.build_lda_model(article,1)
        return lda.get_topic(model,num_topics=1,num_words=k,with_weight=with_weight)[0]
    if method==1:
        if isinstance(article,str):
            article=[article]
        text_list=text_process.general_processing_file(article) 
        for arti in text_list:
            doc+=arti
        return jieba.analyse.extract_tags(doc,topK=k,withWeight=with_weight,allowPOS=())
    elif method==2:
        if isinstance(article,str):
            article=[article]
        article=text_process.general_processing_file(article)
        for arti in article:
            doc+=arti
        return textrank.extract_key_phrases(doc)
    elif method==3:
        if isinstance(article,str):
            article=[article]
        article=text_process.text_processing_rake(article)
        for arti in article:
            doc+=arti
        r = Rake()
        r.extract_keywords_from_text(doc)
        rank=r.get_ranked_phrases()
        if with_weight==False:
            return rank[0:len(rank)/2+1]
        score=r.get_ranked_phrases_with_scores()
        return score[0:len(rank)/2]
    #docs_phase
    else:
        raise ValueError('wrong method code')
        
def test_keyword_extraction(docs):
#    file='process_non.txt'
#    with open(file,'r') as f:
#        docsmu=pickle.load(f)
    for doc in docs[0:11]:
         doc1=u'Massive protests against Mohamed Morsi develop all over Egypt on the second anniversary of the 2011 revolution, including in Tahrir Square, where thousands of protesters gathered. At least 6 civilians and 1 police officer are shot dead in the Egyptian city of Suez, while 456 others are injured nationwide'
         #print doc
         tag=keywords_extraction(doc,method=2, k=20,with_weight=True)
         print tag
    return tag
        
def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP','VB','VBP','VBZ','VBD','VBN','VBG','NNS','NNPS']):
    """Apply syntactic filters based on POS tags."""
    return [item for item in tagged if item[1] in tags]        
#tag=test_keyword_extraction()
#print tag
        
docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
a=test_keyword_extraction(docs)

