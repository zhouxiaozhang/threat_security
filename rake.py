# -*- coding: utf-8 -*-


from rake_nltk import Rake
import pickle
from nltk.tokenize import sent_tokenize


#open return file object
def rake():
    file='process_non.txt'
    r = Rake()
    with open(file,'r') as f:
        docsk=pickle.load(f)
        docs_phase=[]
    #    for line in f:
    #        a.append(line)
        for doc in docsk:
            
            #sent_tokenize_list = sent_tokenize(doc)
            r.extract_keywords_from_text(doc)
            rank=r.get_ranked_phrases()
            score=r.get_ranked_phrases_with_scores()
            total_key=len(rank)
            score_key=score[0:total_key/2]
            docs_phase.append(score)
    return docs_phase
            
docs_phase=rake()            
        
        
        