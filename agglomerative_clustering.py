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
from feature_extract import Content_extract,Contentextraction
import valid


class Agglomerativeclustering:
    LINKAGE_CENTROID='centroid'
    SIMILARITY_DOT='dot'
    def __init__(self,threshold,linkage=LINKAGE_CENTROID,similarity=SIMILARITY_DOT):
        self.threshold = threshold
        self.linkage =linkage
        self.similarity_mode =similarity
        self.id=0
    def fit(self,contents,docs,labels):
        clusters=self._init_clusters(contents,docs,labels)
        print('building similarity table...')
        cluster_pair_list=self._build_cluster_pair_list(clusters)
        most_closest_pair=cluster_pair_list[0]
        while len(clusters)>1 and most_closest_pair['similarity']>self.threshold:
            
            print most_closest_pair['similarity']
            cluster_a=most_closest_pair['key']
            print cluster_a['id']
            cluster_b=most_closest_pair['target']
            print cluster_b['id']
            if len(cluster_pair_list)%10==0:
                print(len(cluster_pair_list))
            #类型是属于对象的，而不是变量(定义的变量，所有的变量都可以理解是内存中一个对象的“引用”)。c++ 函数参数传值还是引用通过有无&，*区别。python 函数参数传值还是引用
            #通过对象是可改变对象还是不可改变区别，eg strings, tuples, 和numbers是不可更改的对象，
            #而list,dict等则是可以修改的对象
            cluster_pair_list,clusters=self._merge_clusters(cluster_a,cluster_b,cluster_pair_list,clusters)
            most_closest_pair=cluster_pair_list[0]
            print len(cluster_pair_list)
            print len(clusters)
        
        return clusters
     
    def _merge_clusters(self,cluster_a,cluster_b,cluster_pair_list=None,clusters=None):
        cluster_a['docs'].extend(cluster_b['docs'])
        cluster_a['vector']=self._cluster_vector(cluster_a)
#        cluster_c={}
#        self.id=self.id+1
#        print self.id 
#        cluster_c['id']=self.id
#        cluster_c['docs']=cluster_a['docs']
#        cluster_c['docs'].extend(cluster_b['docs'])
#        cluster_c['vector']=self._cluster_vector(cluster_c)
        if clusters is not None:
            #range 计算完返回list,后续不再计算range而是使用返回的list,so list index out of range,如果使改变生效 使用 for a in clusters,但是无 index
            for cluster_counter in range(len(clusters)):
                if cluster_b['id'] is clusters[cluster_counter]['id'] :
                    clusters.pop(cluster_counter)
                    break
            for cluster_counter in range(len(clusters)):
                if cluster_a['id'] is clusters[cluster_counter]['id']:
                    clusters[cluster_counter]=cluster_a
                    break
            #del cluster_a,cluster_b,key,有问题
        if cluster_pair_list is not None:
            print 1
            for pair_counter in range(len(cluster_pair_list)):
                pair=cluster_pair_list[pair_counter]
                if cluster_b['id'] is pair['key']['id'] :
                    cluster_pair_list.pop(pair_counter)
                    break
            for pair_counter in range(len(cluster_pair_list)):
                pair=cluster_pair_list[pair_counter]
                if cluster_a['id'] is pair['key']['id']:
                    update_pair=self._find_closest_pair(clusters,cluster_a)
                    if update_pair is not None:
                        cluster_pair_list[pair_counter]['target']=update_pair['target']
                        cluster_pair_list[pair_counter]['similarity']=update_pair['similarity']
                        cluster_pair_list[pair_counter]['key']=cluster_a
                    break                
            #add cluster_c
#            pair=self._find_closest_pair(clusters,cluster_c)
#            cluster_pair_list.append(pair) 
      
            #cluster_pair update
            for i,pair in enumerate(cluster_pair_list):
                if cluster_b['id'] is pair['target']['id'] or cluster_a['id'] is pair['target']['id']:
                    update_pair=self._find_closest_pair(clusters,pair['key'])
                    if update_pair is not None:
                        cluster_pair_list[i]['target']=update_pair['target']
                        cluster_pair_list[i]['similarity']=update_pair['similarity']
            for i,pair in enumerate(cluster_pair_list):
                if pair['key']['id']==cluster_a['id']:
                    continue
                similarity=self._similarity(pair['key'],cluster_a)
                if similarity > pair['similarity']:
                   cluster_pair_list[i]['target']=cluster_a
                   cluster_pair_list[i]['similarity']=similarity
               
        return sorted(cluster_pair_list,key=lambda cluster_pair:cluster_pair['similarity'],reverse=True),clusters
                        
            
                     
    def _cluster_vector(self,cluster_c):
        k=array([a[0] for a in cluster_c['docs']]).mean(axis=0)
        print k.shape
        return k
        
    def _init_clusters(self,contents,docs,labels):
        clusters=[]
        for i,content in enumerate(contents):
            #if self.similarity_mode==self.SIMILARITY_DOT:
            content=matutils.unitvec(content)
            #'vector' centroid vector
            clusters.append({'id':i,'vector':content,'docs':[(content,docs[i],labels[i],i)]})
        self.id=len(clusters)-1
        return clusters
    def _build_cluster_pair_list(self,clusters):
        similarity_table=[]
        for i in range(len(clusters)):
            pair=self._find_closest_pair(clusters,clusters[i])
            similarity_table.append(pair)
        return sorted(similarity_table,key=lambda cluster_pair:cluster_pair['similarity'],reverse=True)
                   
    def _find_closest_pair(self,clusters,cluster):
        pair=None
        for j in range(len(clusters)):
            if cluster['id']==clusters[j]['id']:
                continue
            similarity=self._similarity(cluster,clusters[j])
            if pair is None or similarity > pair['similarity']:
                pair={'similarity':similarity,'key':cluster,'target':clusters[j]}
        if pair is None:
            print(len(clusters))
        return pair
                
        
    def _similarity(self,cluster_a,cluster_b):
        return self._dot_cos_similarity(cluster_a['vector'],cluster_b['vector'])
    def _dot_cos_similarity(self,vector_a,vector_b):
        return dot(vector_a,vector_b)
    
    
#docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
#text_list=text_process.text_processing(docs) 
#wordvector_model=feature_extract.load_model('glove.6B.300d1') 
#content=Content_extract(method=1,model=wordvector_model,with_weight=True,use_idf=True).fit(text_list) 
#clusters=Agglomerativeclustering(0.46).fit(content,docs,labels)  
#filename = 'cluster.txt'  
#with open(filename, 'wb') as f:
#    pickle.dump(clusters, f) 
##clusters1=valid._make_cluster_number(clusters)   
#result=valid.validate_cluster(clusters)

docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')            
text_list=text_process.general_processing_file(docs)
wordvector_model=feature_extract.load_model('glove.6B.300d1') 
content=Contentextraction(method=1,model=wordvector_model,k=22,with_weight=True).fit(docs) 
#content=Content_extract(method=1,model=wordvector_model,with_weight=True,use_idf=True).fit(text_list) 
clusters=Agglomerativeclustering(0.70).fit(content,docs,labels)  
filename = 'cluster.txt'  
with open(filename, 'wb') as f:
    pickle.dump(clusters, f) 
#clusters1=valid._make_cluster_number(clusters)   
#result=valid.validate_cluster(clusters)

         
    


 

                
        
        
        
        
        
    
