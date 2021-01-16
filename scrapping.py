
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 08:14:50 2020

@author: pierre
"""
import os
retval = os.getcwd()
print("Current working directory %s" % retval)
# Now change the directory
os.chdir( retval )

import ClasseDoc as cd

from datetime import datetime
import praw
import re
import urllib
import xmltodict

def cleaner(text):
    text= str(text)
    text= text.replace('’',"'") #pour les compter en tant qu'apostrophe
    text = text.lower()#Make text lowercase
    text = re.sub('\[.*?\]', ' ', text) #remove text in square brackets
    text = re.sub('https?://\S+|www\.\S+', ' ', text) #enlève hyperlien (à placer avant d'enlever la ponctuation)
    text = re.sub(r"[^\w\d'\s]+", ' ', text)#supprime toute la ponctuation sauf apostrophe pr stop word
    text = re.sub('\n', ' ', text) # enlève les retour à la ligne
    return text

def data_transfo(mot_clé, nombre_doc):
    #Preparation
    reddit = praw.Reddit(client_id='pHUCSrH3ywJgtw', client_secret='1OtiyFduFjJBSsg2e8LG1kVDrXs', user_agent='Reddit WebSrapping')
    url = 'http://export.arxiv.org/api/query?search_query=all:' + str(mot_clé) +'&start=0&max_results=' + str(nombre_doc*10)
    data =  urllib.request.urlopen(url).read().decode()
    arxiv_doc = xmltodict.parse(data)['feed']['entry']
    
    #Reddit
    collection_r = {}
    i_collecr = 1
    for post in reddit.subreddit(mot_clé).hot(limit = nombre_doc*10):
        post_clean = cleaner(post.selftext)
        if post_clean.strip():
            collection_r[i_collecr] = cd.RedditDocument(date = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m'),titre = str(post.title),texte = post_clean,type_doc = 'reddit')        
            i_collecr +=1
        if len(collection_r) == nombre_doc:
            break
    
    #Arxiv
    collection_a = {}
    i_colleca = 1
    for i in arxiv_doc:
        text_clean = cleaner(i['summary'])
        if text_clean.strip():
            collection_a[i_colleca] = cd.ArxivDocument(date = datetime.fromisoformat(i['published'][:-1]).strftime('%Y-%m'),titre = i['title'],texte = text_clean,type_doc = 'arxiv')    
            i_colleca +=1  
        if len(collection_a) == nombre_doc:
            break
    
    #Transformation en liste
    lr = []
    for i in range(1,len(collection_r)+1):
        lr.append(collection_r[i].texte)
    la = []
    for i in range(1,len(collection_a)+1):
        la.append(collection_a[i].texte)
    return lr,la

