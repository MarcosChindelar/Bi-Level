# -*- coding: utf-8 -*-
"""
@author: Chindelar
"""
from math import degrees, atan2, sqrt

#Classe referente aos locais utilizada para todos os algoritmos
class Local:
    
    def __init__(self,ID,Type,x,y,d):
        
        #Identificador de um local
        self.id = ID
        #Tipo de um local. c-consumdior/f-estação/d-depósito
        self.type = Type
        #Coordenada x de um local
        self.x = x
        #Coordenada y de um local
        self.y = y
        #Demanda de um local
        self.demand = d
        #Angulo com o deposito
        self.angle = 0

    def getAngle(self):
        return self.angle
    
    def setAngle(self,a):
        self.angle = a    

    #Método que retorna o identificador de um local    
    def getId(self):
        return self.id
    
    #Método que retorna o tipo de um local
    def getType(self):
        return self.type
    
    #Método que retorna a coordenada x de um local
    def getX(self):
        return self.x
    
    #Método que retorna a coordenada y de um local
    def getY(self):
        return self.y
    
    #Método que retorna a demanda de um consumidor
    def getDemand(self):
        return self.demand
    
    #Método que imprime as informações de um local
    def printData(self):
        print("{:4}".format(self.getId()),"\t","{:1}".format(self.getType()),"\t","{:5}".format(self.getX()),"\t","{:5}".format(self.getY()),"\t","{:6}".format(self.getDemand()),"\t","{:6}".format(round(self.getAngle(),2)))
    
    #Método que calcula distância entre dois locais
    def getDistancia(self,local1,local2):
        return ((local1.getX()-local2.getX())**2 + (local1.getY()-local2.getY())**2)**1/2
