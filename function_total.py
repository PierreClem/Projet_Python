# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 15:43:19 2021

@author: ccl13
"""
import sys
sys.path.insert(0, 'C:/Users/ccl13/Desktop/Master 1/projet python') # location of src 
import All_function_TFIDF as AFT
import pandas as pd


def total(data_init):
    #exécution des fonctions crée dans All_function_TFIDF
    data = AFT.cleaned(data_init)
    U = AFT.union(data)
    res = AFT.comptage(data, U)
    
    resTF = [0 for i in range(len(data))]
    for i in range(0,len(data)):
        resTF[i] = AFT.TF(res[i],data[i])
    
    idf = AFT.computeIDF(res)
    
    TFIDF_ = AFT.appli_TFIDF(resTF, idf)
    return TFIDF_


data_init_r = lr.copy()
data_init_a = la.copy()

reddit_IDF = total(data_init_r); len(reddit_IDF )
arxiv_IDF = total(data_init_a); len(arxiv_IDF)

AFT.graphique(reddit_IDF, arxiv_IDF)

