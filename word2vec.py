import re
import sys
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


sentences = LineSentence('process.txt')
model = Word2Vec(sentences, size=30, window=5, min_count=5, workers=4)
model.save('word.model')
model.wv.save_word2vec_format('word1.model',binary=False)
model1 = Word2Vec.load('word.model')
print model1.similarity('people', 'police')