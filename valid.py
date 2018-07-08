from sklearn import metrics
import numpy as np
import cPickle as pickle
import text_process
def _make_cluster_number(clusters):
    #i pre label
    for i in range(len(clusters)):
        for j,doc in enumerate(clusters[i]['docs']):
            clusters[i]['docs'][j]=doc+(i,)
    return clusters
def _make_cluster_pre(clusters):
    #i pre label
    cluster_pre=[]
    for i in range(len(clusters)):
        for j,doc in enumerate(clusters[i]['docs']):
            clusters[i]['docs'][j]=doc+(i,)
        cluster_pre.append(clusters[i]['docs'])
    return cluster_pre

def _make_cluster_true(clusters):
    cluster_true=[]
    cluster_inter=[]
 #   _make_cluster_number(clusters)
    label_docs=[doc for cluster in clusters for doc in cluster]
    label_docs.sort(key=lambda d:d[2])
    cluster_inter.append(label_docs[0])
    for label in label_docs[1:]:
        if label[2]==cluster_inter[-1][2]:
            cluster_inter.append(label)
        else:
            cluster_true.append(cluster_inter)
            cluster_inter=[]
            cluster_inter.append(label)
    cluster_true.append(cluster_inter)
    return cluster_true
            
        
    
    

def _get_docs_cluster(clusters):
   _make_cluster_number(clusters)
   label_docs=[doc for cluster in clusters for doc in cluster["docs"]]
   label_docs.sort(key=lambda d:d[3])
   #docs=[doc for doc in label_docs]
   return label_docs
   
            
def validate_cluster(clusters):
##clusters    
    filename = 'clusters.txt' 
    docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')
    with open(filename,"rb") as f:
        data=pickle.load(f) 
    labels_true=labels
    labels_pred=data.tolist()
#    docs=_get_docs_cluster(clusters)
#    labels_true=[doc[2] for doc in docs]
#    labels_pred=[doc[4] for doc in docs]
    result = {
        'ARI': '{0:.2f}'.format(metrics.adjusted_rand_score(labels_true, labels_pred)),
        'AMI': '{0:.3f}'.format(metrics.adjusted_mutual_info_score(labels_true, labels_pred)),
        'Homogeneity': '{0:.2f}'.format(metrics.homogeneity_score(labels_true, labels_pred)),
        'Completeness': '{0:.2f}'.format(metrics.completeness_score(labels_true, labels_pred)),
        'V-measure': '{0:.2f}'.format(metrics.v_measure_score(labels_true, labels_pred))
    }
    return result

def pre_recall(clusters):
    cluster_pre=_make_cluster_pre(data)
    cluster_true=_make_cluster_true(cluster_pre)    
    precision=np.zeros((len(cluster_true),len(cluster_pre))) 
    recall=precision=np.zeros((len(cluster_true),len(cluster_pre)))
    F_measure=np.zeros((len(cluster_true),len(cluster_pre)))
    F_measure_max=np.zeros(len(cluster_true))
    for index_i,i in enumerate(cluster_true):
        for index_j,j in enumerate(cluster_pre):
            n_i_j=0
            ni=[num_i[3] for num_i in i]
            nj=[num_j[3] for num_j in j]
            n_i_j=list(set(ni).intersection(set(nj)))
            #print ni
            #print nj
            print n_i_j
            precision[index_i][index_j]=(1.0*len(n_i_j))/(1.0*len(j))
            recall[index_i][index_j]=(1.0*len(n_i_j))/(1.0*len(i)) 
            F_measure[index_i][index_j]=2*precision[index_i][index_j]*recall[index_i][index_j]/(precision[index_i][index_j]+recall[index_i][index_j]+0.00001)
        F_measure_max[index_i]=max(F_measure[index_i])


def pre_recall1(dict_pre,dict_act):
 
    precision=np.zeros((len(dict_act),len(dict_pre))) 
    recall=precision=np.zeros((len(dict_act),len(dict_pre)))
    F_measure=np.zeros((len(dict_act),len(dict_pre)))
    F_measure_max=np.zeros(len(dict_act))
    for index_i,(act_key,act_value) in enumerate(dict_act.items()):
        for index_j,(pre_key,pre_value) in enumerate(dict_pre.items()):
            n_i_j=list(set(act_value).intersection(set(pre_value)))
            print n_i_j
            precision[index_i][index_j]=(1.0*len(n_i_j))/(1.0*len(pre_value))
            recall[index_i][index_j]=(1.0*len(n_i_j))/(1.0*len(act_value)) 
            F_measure[index_i][index_j]=2*precision[index_i][index_j]*recall[index_i][index_j]/(precision[index_i][index_j]+recall[index_i][index_j]+0.00001)
        F_measure_max[index_i]=max(F_measure[index_i])
          

                   
filename = 'clusters.txt' 
#filename = 'cluster.txt'
docs,labels=text_process.extract_articles('acl2017dataset/story_clusters.txt')
with open(filename,"rb") as f:
    data=pickle.load(f)
result=validate_cluster(data)
#dict_pre={}
#dict_act={}
#for i,value in enumerate(data):
#    dict_pre.setdefault(value, []).append(i)
#for j,value1 in enumerate(labels):
#    dict_act.setdefault(value1, []).append(j)
#for i,(key,values) in enumerate(dict_pre.items()):
#    print i, key,values    
#    
#precision=np.zeros((len(dict_act),len(dict_pre))) 
#recall=np.zeros((len(dict_act),len(dict_pre)))
#F_measure=np.zeros((len(dict_act),len(dict_pre)))
#F_measure_max=np.zeros(len(dict_act))
#precision_max=np.zeros(len(dict_act))
#recall_max=np.zeros(len(dict_act))
#F_measures=0.0
#for index_i,(act_key,act_value) in enumerate(dict_act.items()):
#    for index_j,(pre_key,pre_value) in enumerate(dict_pre.items()):
#        n_i_j=list(set(act_value).intersection(set(pre_value)))
#        #print n_i_j
#        precision[index_i][index_j]=(1.0*len(n_i_j))/(1.0*len(pre_value))
#        recall[index_i][index_j]=(1.0*len(n_i_j))/(1.0*len(act_value)) 
#        print len(pre_value)
#        print len(act_value)
#        F_measure[index_i][index_j]=2*precision[index_i][index_j]*recall[index_i][index_j]/(precision[index_i][index_j]+recall[index_i][index_j]+0.00001)
#    F_measure_max[index_i]=max(F_measure[index_i])
#    precision_max[index_i]=max(precision[index_i])
#    recall_max[index_i]=max( recall[index_i])
#    F_measures+=F_measure_max[index_i]*len(act_value)/len(labels)
#
#result=validate_cluster()
