# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 15:51:39 2021

@author: ccl13
"""
################################# PACKAGE
import pandas as pd
import re
from nltk.corpus import stopwords
import math
###########################################
#################################  STOPWORD
stopwords = stopwords.words('english')
stopwords.extend(['','from', 'subject', 're', 'edu', 'use','im','&#x200B'])
###########################################
################################# fonction 

#### Nettoyage des données 
 
def cleaned(document):
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

def union(doc):  #création du dictionnaire des mots de tout les articles
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
    for document in documents:
        for word, val in document.items(): #
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():  
        tfidf[word] = val*idfs[word] # calcul de TFxIDF
    return tfidf

def appli_TFIDF(TF,IDF):
    TFIDF =[]
    for i in range(0,len(TF)):
        TFIDF.append(computeTFIDF(TF[i], IDF))
    return TFIDF

def graphique(redditIDF,arxivIDF):
    from matplotlib import pyplot
    DF_reddit = pd.DataFrame(redditIDF) #transoformation en data frame
    DF_arxiv = pd.DataFrame(arxivIDF)
    
    colr = DF_reddit.columns; len(colr) # stockage des index
    cola = DF_arxiv.columns; len(cola)
    
    A = colr.intersection(cola) # index communs à reddit et arxiv
    
    mean_arxiv = DF_arxiv[A].mean() # moyenne de TFIDF pour les mots communs aux 
    mean_reddit = DF_reddit[A].mean() # deux forums
    
    A = mean_arxiv.sort_values(ascending=False)[0:10] #stockage des 10 moyennes maximale
    B = mean_reddit.sort_values(ascending=False)[0:10]
    
    liste_index = []      
    for i in range(0,len(A)): # concaténation des index du top 10 de reddit et arxiv
        liste_index.append(A.index[i])  
    for i in range(0,len(A)):
        liste_index.append(B.index[i])
    X_a = pd.Series(mean_arxiv, index=liste_index)  # valuer pour arxiv
    X_r = pd.Series(mean_reddit, index=liste_index)
    long = range(len(X_r))
  
    pyplot.barh(long, X_a, color = 'blue',linewidth = 3) # création du graphique
    pyplot.barh(long, X_r, left = X_a, color = 'grey',linewidth = 3)
    pyplot.yticks(range(len(X_r)), liste_index)

    