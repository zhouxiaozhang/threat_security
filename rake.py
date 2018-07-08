# -*- coding: utf-8 -*-

from rake_nltk import Rake
import pickle
from nltk.tokenize import sent_tokenize
file='process_non.txt'
r = Rake()
a=[]

#open return file object
with open(file,'r') as f:
    docsk=pickle.load(f)
#    for line in f:
#        a.append(line)
    doc1='Massive protests against Mohamed Morsi develop all over Egypt on the second anniversary of the 2011 revolution, including in Tahrir Square, where thousands of protesters gathered. At least 6 civilians and 1 police officer are shot dead in the Egyptian city of Suez, while 456 others are injured nationwide'
    for doc in docsk[0:1]:
        
        #sent_tokenize_list = sent_tokenize(doc)
        r.extract_keywords_from_text(doc)
        rank=r.get_ranked_phrases()
        score=r.get_ranked_phrases_with_scores()
        
        