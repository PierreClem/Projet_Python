#!/usr/bin/env python3


import datetime
class Document:
    def __init__(self,type_doc = "",titre="",url="",auteur="",date=datetime.datetime.now(),texte=""):
        self.titre=titre
        self.url = url
        self.auteur=auteur
        self.date=date
        self.texte=texte #contenu du texte
        self.type_doc=type_doc
        
    def __str__(self):
        return ("Le titre du doc :"+ self.titre) #+ "\n L'url :"+ self.__url +"\n L'auteur :"+ self.__auteur +"\n La date :" + str(self.__date) +"\n Le texte :"+ self.__texte)

class Author:
    def __str__(self):
        return ("Nom de l'auteur : "+ self.name)
    
    def __init__(self,name=""):
        self.name=name
        self.production={}
        self.ndoc = 0
    
    def add(self,contenu):
        self.ndoc +=1
        self.production[self.ndoc] = contenu

class RedditDocument(Document):
    def __init__(self,type_doc = "",titre="",url="",auteur="",date=datetime.datetime.now(),texte="",score = 0):
        super().__init__(type_doc = type_doc,titre=titre,url=url,auteur=auteur,date=date,texte=texte)
        self.score = score
        
    def setScore(self,score):
        if score == 0:
            return 
        self.__score = score
    
    def getType(self):
        return "Reddit"
        
    def __str__(self):
       return ("Le titre du doc :"+ self.titre ," et son score est de :" + self.score)
   
class ArxivDocument(Document): # vu que subreddit, pris les commentaires et non co autheur
  def __init__(self,type_doc = "",titre="",url="",auteur="",date=datetime.datetime.now(),texte="",comment =""):
        super().__init__(type_doc = type_doc,titre=titre,url=url,auteur=auteur,date=date,texte=texte)
        self.comment = comment
        
  def setComment(self,comment):
        if comment == "":
            return 
        self.__comment = comment
        
  def __str__(self):
     return ("Le titre du doc :"+ self.titre ," et un exemple de commentaire est :" + self.comment)
 
  def getType(self):
     return "Arxiv"