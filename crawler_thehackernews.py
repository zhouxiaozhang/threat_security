# -*- coding: utf-8 -*-
"""
Created on Fri Jun 01 10:30:55 2018

@author: zhou
"""
#url
#https://threatpost.com/category/vulnerabilities/page/
#https://threatpost.com/category/vulnerabilities/
#https://threatpost.com/category/malware-2/page/
#https://threatpost.com/category/malware-2/
#https://thehackernews.com/search/label/Malware
import time,re,requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import gevent
from gevent import monkey,pool
from concurrent.futures import ThreadPoolExecutor
import threading
import datetime
import pickle


class WebCrawlFromthreatpost(object):
    def __init__(self,**kwarg):
#        self.ThreadsNum=kwarg['ThreadsNum']
         self.dbName=kwarg['dbName']
         self.colName=kwarg['collectionName']
         self.IP=kwarg['IP']
         self.PORT=kwarg['PORT']
         self.ThreadsNum = kwarg['ThreadsNum']
         self.Range=kwarg['Range']
#        self.Prob=.5
#        self.realtimeNewsURL=[]

    def GenPagesLst(self,totalUrls):
        Urls=[]
        k=0
        while k+self.Range-1<=len(totalUrls)-1:
            Urls.append((totalUrls[k:k+self.Range])) 
            k+=self.Range
        if k<=len(totalUrls)-1:
            Urls.append(totalUrls[k:]) 
        return Urls
    
    def ConnDB(self):
        Conn=MongoClient(self.IP,self.PORT)
        db=Conn.test
        #db.authenticate("zhou","123456")
        self._collection=db.get_collection(self.colName)
        #self._collection.distinct('Address')
        #AddressLst=self.extractData(['Address'])
        #if ''+'https://thehackernews.com/2014/11/china-made-e-cigarette-chargers-could_26.html' in AddressLst:
         #   print 1

        #self._collection.update({"Category":{'$exists' : False}},{'$set' :{"Category":"Vulnerabilities"}},False,True)
        #return self._collection.find_one()

        #self._collection.drop()
        print self._collection.find().count()
        print len(self._collection.distinct('Address'))
     
    def extractData(self,tag_list):
        data=[]
        for tag in tag_list:
            data.extend(self._collection.distinct(tag))
        return data
    
    def getUrlInfo(self,url):
         resp=requests.get(url)
         print url
         resp.encoding= BeautifulSoup(resp.content,"lxml").original_encoding
         bs= BeautifulSoup(resp.text,"lxml")
         span_list=bs.find_all('span')
         part=bs.find_all('div')
         article=''
         date=''
         for span in span_list:
             #print span.attrs
             if 'class' in span.attrs and span.get('class')==['updated'] and span.parent.get('class') and span.parent.get('class')==['dtstamp','author']:
                 #print span.parent.attrs
                                                  #and span.parent.get('class') and span.parent.get('class')==['dtstamp','author']:
                 date=span.text
                 break
         for paragraph in part:
             if 'class' in paragraph.attrs and paragraph.get('class')==['articlebodyonly']:
                 #print  paragraph.attrs
                 article+=paragraph.text
         article=' '.join(article.strip().split())
         article=article.replace( "(adsbygoogle = window.adsbygoogle || []).push({}); ","")
                
         return date,article
                 
             #and paragraph.parent.get('itemprop')
    def get_urls(self,init_url):
       # s=requests.session()
        #s.keep_alive=False
        #self.ConnDB()
        flag=True
        urls=[]
        url=init_url
        while(flag):
            flag=False
            resp=requests.get(url)
            resp.encoding= BeautifulSoup(resp.content,"lxml").original_encoding
            bs= BeautifulSoup(resp.text,"lxml")
            next_table_list=bs.find_all('span')
            for next_table in next_table_list:
                if 'id' in next_table.attrs and next_table.get('id')=="blog-pager-older-link" and next_table.a and next_table.a.get('class')==['blog-pager-older-link-mobile']:
                    print 1                                          #and next_table.a.get('class')=="blog-pager-older-link-mobile":
                   # print next_table.a.get('href')
                    urls.append(url)
                    url=next_table.a.get('href')
                    flag=True
                    break
        print len(urls)
        Url_list=self.GenPagesLst(urls)
        filename = 'urls.txt'  
        with open(filename, 'wb') as f:
            pickle.dump(Url_list, f) 
        return Url_list
                
                
                                                              #and next_table.a and next_table.a.get('class')=="blog-pager-older-link-mobile":
        
        
    def CrawHistoryNews(self,urls,result):
        self.ConnDB()
        k=0
        s=requests.session()
        s.keep_alive=False
        
        #AddressLst=self.extractData(['Address'])
        for url in urls:
            queue=[]
            resp=requests.get(url)
            resp.encoding= BeautifulSoup(resp.content,"lxml").original_encoding
            bs= BeautifulSoup(resp.text,"lxml")
            a_list=bs.find_all('a')
            #https://threatpost.com/category/vulnerabilities/page/https://threatpost.com/category/vulnerabilities/page/https://threatpost.com/category/vulnerabilities/page/
            for a in a_list:
                #print a.parent.attrs
                #article.append(a.get('href'))
                if 'href' in a.attrs and a.parent.get('class') and a.parent.get('class')==['post-title', 'url'] and a.get('href').find('https://thehackernews.com')!=-1 :
                    k+=1
                    print k
#                    print a.attrs                                                                         #and a.parent.get('class')==['entry-title'] :
#                    print a.parent.attrs
                     #print a.parent.attrs
                     #result.append(a.get('href'))
                    AddressLst=self.extractData(['Address'])
                    if a.get('href') not in AddressLst:
                        print 8
                        date,article=self.getUrlInfo(a.get('href'))
                        if article !='':
                            data={'Date':date,
                                  'Address':a.get('href'),
                                   'Title':a.text,
                                    'Article':article,
                                    'Category':'Malware'
                                    }
                            self._collection.insert_one(data)
                            
                            queue.append(data)
       
            result.append(queue)
        return result
    def multi_threads_run(self,init_url,**kwarg):
        Urls_list = self.get_urls(init_url)
        #filename = 'urls.txt' 
        #with open(filename,"rb") as f:
         #   Urls_list=pickle.load(f) 
#        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        th_lst = []
        result=[]

#        for page_range in page_ranges_lst:
#            thread = threading.Thread(target=self.CrawHistoryNews,\
#                                      args=(page_range[0],page_range[1],kwarg['url_Part_1'],result))
#            th_lst.append(thread)
#        for thread in th_lst:
#            thread.start()Fpr
#        for thread in th_lst:
#            thread.join()
#        print(' Using ' + str(self.ThreadsNum) + ' threads for collecting news ... ')
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with ThreadPoolExecutor(max_workers=self.ThreadsNum) as executor:
            future_url={executor.submit(self.CrawHistoryNews,urls,result):urls for urls in Urls_list}
            #print(future_url.result())
            #: page_range for ind, page_range  in enumerate(page_ranges_lst)}  
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return result
    def coroutine_run(self,totalPages,Range,initPageID,**kwarg):
        jobs=[]
        page_ranges_lst=self.GenPagesLst(totalPages,Range,initPageID)
        for page_range in page_ranges_lst:
            jobs.append(gevent.spawn(self.CrawHistoryNews,page_range[0],page_range[1],kwarg['url_Part_1']))
        gevent.joinall(jobs)

#k= WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-malware",ThreadsNum=6,Range=10).multi_threads_run(init_url='https://thehackernews.com/search/label/Malware') 
#j= WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-malware-thehackernews",ThreadsNum=1,Range=10).multi_threads_run(init_url='https://thehackernews.com/search/label/Malware') 
k=WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-malware-thehackernews",ThreadsNum=6,Range=10).ConnDB()
#k=WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-malware-thehackernews",ThreadsNum=6,Range=10).get_urls(init_url='https://thehackernews.com/search/label/Malware')
#k= WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-malware",ThreadsNum=6,Range=10).CrawHistoryNews(urls=['https://thehackernews.com/search/label/Malware?updated-max=2017-10-19T23:07:00-11:00&max-results=20&start=51&by-date=false'],result=result) 