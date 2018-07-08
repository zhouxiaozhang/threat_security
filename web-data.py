# -*- coding: utf-8 -*-
"""
Created on Sun Jul 08 19:38:47 2018

@author: zhou
"""


import json

#with open('zhou-malware-thehackernews.json', 'r') as f:
#    data = json.load(f)
def search2(sortname,keyword2):


	f = open('test2.txt','a')

	file = open('acl2017dataset/zhou-malware-securityweek.json','r')
	for line in file.readlines():
	    dic = json.loads(line)
	    count = 0
	    for sort in keyword2:
	    	if(dic['Article'].find(sort)!=-1 or dic['Article'].find(sort.lower())!=-1 or dic['Title'].find(sort)!=-1 ):
	    		count = count +1

	    if((dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1 or dic['Title'].find(sortname)!=-1 ) and count == 1):
	    	dic = json.dumps(line)
	    	dic = dic.replace("\\","")
	    	f.write(str(dic))
	    	f.write("\n")
	    	
	file = open('acl2017dataset/zhou-malware-thehackernews.json','r')
	for line in file.readlines():
	    dic = json.loads(line)
	    count = 0
	    for sort in keyword2:
	    	if(dic['Article'].find(sort)!=-1 or dic['Article'].find(sort.lower())!=-1 or dic['Title'].find(sort)!=-1 ):
	    		count = count +1

	    if((dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1 or dic['Title'].find(sortname)!=-1 ) and count == 1):
	    	dic = json.dumps(line)
	    	dic = dic.replace("\\","")
	    	f.write(str(dic))
	    	f.write("\n")

	file = open('acl2017dataset/zhou-malware-threatpost.json','r')
	for line in file.readlines():
	    dic = json.loads(line)
	    count = 0
	    for sort in keyword2:
	    	if(dic['Article'].find(sort)!=-1 or dic['Article'].find(sort.lower())!=-1 or dic['Title'].find(sort)!=-1 ):
	    		count = count +1

	    if((dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1 or dic['Title'].find(sortname)!=-1 ) and count == 1):
	    	dic = json.dumps(line)
	    	dic = dic.replace("\\","")
	    	f.write(str(dic))
	    	f.write("\n")

def search(sortname,keyword):


	f = open('test.txt','a')

	file = open('acl2017dataset/zhou-vulnerabilities-securityweek.json','r')
	for line in file.readlines():
	    dic = json.loads(line)
	    count = 0
	    for sort in keyword:
	    	if(dic['Article'].find(sort)!=-1 or dic['Article'].find(sort.lower())!=-1 or dic['Title'].find(sort)!=-1 ):
	    		count = count +1

	    if((dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1 or dic['Title'].find(sortname)!=-1 ) and count == 1):
	    	dic = json.dumps(line)
	    	dic = dic.replace("\\","")
	    	f.write(str(dic))
	    	f.write("\n")


	file = open('acl2017dataset/zhou-vulnerabilities-threatpost.json','r')
	for line in file.readlines():
	    dic = json.loads(line)
	    count = 0
	    for sort in keyword:
	    	if(dic['Article'].find(sort)!=-1 or dic['Article'].find(sort.lower())!=-1 or dic['Title'].find(sort)!=-1 ):
	    		count = count +1

	    if((dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1 or dic['Title'].find(sortname)!=-1 ) and count == 1):
	    	dic = json.dumps(line)
	    	dic = dic.replace("\\","")
	    	f.write(str(dic))
	    	f.write("\n")


def date(sortname):
	f = open('test.txt','a')

	datemin = 2019
	datemax = 2000
	file = open('acl2017dataset/zhou-vulnerabilities-securityweek.json','r')
	for line in file.readlines():
	    dic = json.loads(line)

	    if(dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1):
	    	datetmp = int((dic['Date'][-4:]))
	    	if datetmp <= datemin : datemin = datetmp
	    	if datetmp >= datemax : datemax = datetmp

	file = open('acl2017dataset/zhou-vulnerabilities-threatpost.json','r')
	for line in file.readlines():
	    dic = json.loads(line)

	    if(dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1):
	    	n = 0
	    	for k in dic['Date']:
	    		n = n+1
	    		if k == ',':
	    			datetmp = int(dic['Date'][n:n+5])
	    			break
	    	if datetmp <= datemin : datemin = datetmp
	    	if datetmp >= datemax : datemax = datetmp
	    	
	f.write("%%%"+sortname+str(datemin)+"——"+str(datemax))
	f.write("\n")


def date2(sortname):
	f = open('test2.txt','a')

	datemin = 2019
	datemax = 2000
	file = open('acl2017dataset/zhou-malware-securityweek.json','r')
	for line in file.readlines():
	    dic = json.loads(line)

	    if(dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1):
	    	datetmp = int((dic['Date'][-4:]))
	    	if datetmp <= datemin : datemin = datetmp
	    	if datetmp >= datemax : datemax = datetmp

	file = open('acl2017dataset/zhou-malware-threatpost.json','r')
	for line in file.readlines():
	    dic = json.loads(line)

	    if(dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1):
	    	n = 0
	    	for k in dic['Date']:
	    		n = n+1
	    		if k == ',':
	    			datetmp = int(dic['Date'][n:n+5])
	    			break
	    	if datetmp <= datemin : datemin = datetmp
	    	if datetmp >= datemax : datemax = datetmp

	file = open('acl2017dataset/zhou-malware-thehackernews.json','r')
	for line in file.readlines():
	    dic = json.loads(line)

	    if(dic['Article'].find(sortname)!=-1 or dic['Article'].find(sortname.lower())!=-1):
	    	datetmp = int(dic['Date'][0:4])
	    	if datetmp <= datemin : datemin = datetmp
	    	if datetmp >= datemax : datemax = datetmp

	f.write("%%%"+sortname+str(datemin)+"——"+str(datemax))
	f.write("\n")






keyword = ['Meltdown','Spectre','EternalBlue','Heartbleed bug','DROWN','ImageTragick','OpenSSL','Stagefright','Sandworm','Venom']
keyword2 = ['Stuxnet','Wannacry','Petya','VPNFilter','TeslaCrypt','Proton','Shamoon','Careto','CryptoLocker','Flamer']
#search(sortname)
f = open('test.txt','w')
f = open('test2.txt','w')



for sortname in keyword:
	date(sortname)
	search(sortname,keyword)
#
#for sortname in keyword2:
#	date2(sortname)
#	search2(sortname,keyword2)



file = open('acl2017dataset/zhou-vulnerabilities-securityweek.json','r')
dic=[]
for line in file.readlines():
    dic.append(json.loads(line))




