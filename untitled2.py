# -*- coding: utf-8 -*-
"""
Created on Tue May 29 16:31:39 2018

@author: zhou
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import pymongo

client=pymongo.MongoClient(host='10.108.217.52',port=27017)
db=client.test
db.authenticate("zhou","123456")

#
#collection=db.get_collection("zhou")
#student={
#        'id':'2016110729',
#        'name':'jordan'
#        }
#
#collection.insert_one(student)
#result=collection.find_one({'name':'jordan'})
#print result
