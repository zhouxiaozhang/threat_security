# -*- coding: utf-8 -*-
"""
Created on Sun Jul 01 09:49:59 2018

@author: zhou
"""

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
import time,re,requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import gevent
from gevent import monkey,pool
from concurrent.futures import ThreadPoolExecutor
import threading
import datetime


class WebCrawlFromthreatpost(object):
    def __init__(self,**kwarg):
#        self.ThreadsNum=kwarg['ThreadsNum']
         self.dbName=kwarg['dbName']
         self.colName=kwarg['collectionName']
         self.IP=kwarg['IP']
         self.PORT=kwarg['PORT']
         self.ThreadsNum = kwarg['ThreadsNum']
#        self.Prob=.5
#        self.realtimeNewsURL=[]

    def GenPagesLst(self,totalPages,Range,initPageID):
        PageLst=[]
        k=initPageID
        while k+Range-1<=totalPages:
            PageLst.append((k,k+Range-1)) 
            k+=Range
        if k<=totalPages:
            PageLst.append((k,totalPages)) 
        return PageLst
    def ConnDB(self):
        Conn=MongoClient(self.IP,self.PORT)
        db=Conn.test
        #db.authenticate("zhou","123456")
        self._collection=db.get_collection(self.colName)

        #self._collection.update({"Category":{'$exists' : False}},{'$set' :{"Category":"Vulnerabilities"}},False,True)
        #return self._collection.find_one()

        #result=self._collection.drop()
        print self._collection.find().count()
        print len(self._collection.distinct('Address'))
     
    def extractData(self,tag_list):
        data=[]
        for tag in tag_list:
            data.extend(self._collection.distinct(tag))
        return data
    
    def getUrlInfo(self,url):
         resp=requests.get(url)
         resp.encoding= BeautifulSoup(resp.content,"lxml").original_encoding
         bs= BeautifulSoup(resp.text,"lxml")
         span_list=bs.find_all('span')
         part=bs.find_all('p')
         article=''
         date=''
         for span in span_list:
             #print span.attrs
             if 'class' in span.attrs and span.get('class')==['date', 'alignright'] and span.time:
                 date=span.time.text
                 break
         for paragraph in part:
             if 'itemprop' in paragraph.parent.attrs and paragraph.parent.get('itemprop')=="articleBody":
                 #print  paragraph.text
                 article+=paragraph.text
                 article+=' '
#             while article.find('<')!=-1 and article.find('>')!=-1:
#                 string1=article[article.find('<'):article.find('>')+1]
#                 article=article.replace(string1,'')
         return date,article
                 
             #and paragraph.parent.get('itemprop')
                 
    def CrawHistoryNews(self,startPage,endPage,url_Part_1,result):
        self.ConnDB()
        AddressLst=self.extractData(['Address'])
        urls=[]
        for pageID in range(startPage,endPage+1):
            print pageID
            if pageID==1:
                urls.append('https://threatpost.com/category/vulnerabilities/')
            else:
                urls.append(url_Part_1+str(pageID))
        for url in urls:
            resp=requests.get(url)
            resp.encoding= BeautifulSoup(resp.content,"lxml").original_encoding
            bs= BeautifulSoup(resp.text,"lxml")
            a_list=bs.find_all('a')
            #https://threatpost.com/category/vulnerabilities/page/https://threatpost.com/category/vulnerabilities/page/https://threatpost.com/category/vulnerabilities/page/
            for a in a_list:
                #print a.parent.attrs
                #article.append(a.get('href'))
                if 'href' in a.attrs and 'itemprop' in a.attrs and 'rel' in a.attrs and a.get('href').find('https://threatpost.com')!=-1 and a.parent.get('class')==['entry-title'] :
                    #print a.get('href')
                    if a.get('href') not in AddressLst:
                        print 2
                        date,article=self.getUrlInfo(a.get('href'))
                        if article !='':
                            data={'Date':date,
                                  'Address':a.get('href'),
                                   'Title':a.text,
                                    'Article':article,
                                    'Category':'vulnerabilities'
                                    }
                            self._collection.insert_one(data)
                            
                            result.append(data)

        return result
    def multi_threads_run(self,totalPages,Range,initPageID,**kwarg):
        page_ranges_lst = self.GenPagesLst(totalPages,Range,initPageID)
#        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        th_lst = []
        result=[]
#        for page_range in page_ranges_lst:
#            thread = threading.Thread(target=self.CrawHistoryNews,\
#                                      args=(page_range[0],page_range[1],kwarg['url_Part_1'],result))
#            th_lst.append(thread)
#        for thread in th_lst:
#            thread.start()
#        for thread in th_lst:
#            thread.join()
#        print(' Using ' + str(self.ThreadsNum) + ' threads for collecting news ... ')
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with ThreadPoolExecutor(max_workers=self.ThreadsNum) as executor:
            future_url={executor.submit(self.CrawHistoryNews,page_ranges[0],page_ranges[1],kwarg['url_Part_1'],result):page_ranges for page_ranges in page_ranges_lst}
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
#k= WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-vulnerabilities-threatpost",ThreadsNum=6).multi_threads_run(523,10,1,url_Part_1='https://threatpost.com/category/vulnerabilities/page/') 
j= WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-vulnerabilities-threatpost",ThreadsNum=6).ConnDB()
#k=WebCrawlFromthreatpost(IP= '10.108.217.52',PORT=27017,dbName="test",collectionName="zhou-malware",ThreadsNum=6).extractData(['Address'])