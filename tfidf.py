# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 15:51:39 2021

@author: ccl13
"""
import os
retval = os.getcwd()
print("Current working directory %s" % retval)
# Now change the directory
os.chdir( retval )
################################# PACKAGE
###########################################
################################# fonction 
from nltk.corpus import stopwords
stopwords = stopwords.words('english')
import praw
import ClasseDoc as cd
from datetime import datetime
import re
import urllib
import xmltodict
from matplotlib import pyplot
import pandas as pd
import math

#### Nettoyage des données 
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
    
    #scrapping des articles Reddit
    collection_r = {}
    i_collecr = 1
    for post in reddit.subreddit(mot_clé).hot(limit = nombre_doc*10): # parcours des n*10 articles 
        post_clean = cleaner(post.selftext) # nettoyage des articles 
        if post_clean.strip(): # si l'articles n'est pas vide ajout à collection_r
            collection_r[i_collecr] = cd.RedditDocument(date = datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m'),titre = str(post.title),texte = post_clean,type_doc = 'reddit')        
            i_collecr +=1
        if len(collection_r) == nombre_doc: # condition de maniere a obtenir le nombre d'article voulu 
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

def cleaned(document):
    
    stopwords.extend(['','from', 'subject', 're', 'edu', 'use','im','&#x200B'])
    for i in range(0,len(document)): # séparation des mots dans les articles  
        document[i] = document[i].split(' ')
    Ltestclean=[]
    Ltot =[]
    
    for i in range(0,len(document)):
        for j in document[i]:
            if (j.lower() not in stopwords) : # comparaison des mots avec les stopwords
                Ltestclean.append(j) # pour ne selectionner que les mots differents des stopwords
        Ltot.append(Ltestclean)
        Ltestclean=[]   
    document = Ltot
    return document

def union(doc): #création du dictionnaire des mots de tout les articles
    U={}
    for i in range(0,len(doc)): # deplacement dans chaque article
        U = set(U).union(set(doc[i])) # ajout des mots non présent dans U
    return U

###
#### Comptage des effectifs
def comptage(doc,union):
    res=[0 for i in range(len(doc))] #création d'une liste vide
    for i in range(0,len(doc)): # déplacement dans les articles
        U1 = dict.fromkeys(union,0)
        for word in doc[i]: #déplassement dans chaque "articles" (mot)
            U1[word] += 1 # ajoute 1 a l'effectif du mot si présent 
        res[i] = U1 
    return res
#### Calcul de TF
def TF(phrase,effectif_article):
    tfdict ={}
    effectif_article = len(effectif_article) # nombre de mot présent dans l'article
    for word, count in phrase.items():
        tfdict[word] = count / float(effectif_article) #calcul de TF 
    return tfdict

def computeIDF(documents):
    import math
    N = len(documents) #nombre d'articles
    
    idfDict = dict.fromkeys(documents[0].keys(), 0) 
    for document in documents: # parcours des articles
        for word, val in document.items(): # parcours des valeurs 
            if val > 0: # condition val > 0
                idfDict[word] += 1 # si condition verifié alors ajouter 1 au mot
    
    for word, val in idfDict.items(): 
        idfDict[word] = math.log(N / float(val)) # calcul IDF nombre de documents / val 
    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items(): #parcours on recupere les vlauer de TFIDF pour chaque mot
        tfidf[word] = val*idfs[word] # calcul de TFxIDF pour chaque article
    return tfidf

def appli_TFIDF(TF,IDF): # fonction qui permet d'appliquet TFIDF
    TFIDF =[]
    for i in range(0,len(TF)):
        TFIDF.append(computeTFIDF(TF[i], IDF))
    return TFIDF
    
def total(data_init):    # fonction qui concatène toute nos fonction 
    data = cleaned(data_init)
    U = union(data)
    res = comptage(data, U)
    
    resTF = [0 for i in range(len(data))]
    for i in range(0,len(data)):
        resTF[i] = TF(res[i],data[i])
    
    idf = computeIDF(res)
    
    TFIDF_ = appli_TFIDF(resTF, idf)
    return TFIDF_