# -*- coding: utf-8 -*-
"""
@author: Marcos Chindelar
"""
import random
from Model import Model
from copy import deepcopy
import numpy as np

class VND():

    def __init__(self,instance,A,B):
           self.instance = instance
           self.z = [random.randint(1,1) for i in range(len(self.instance.stations))]
           self.A = A
           self.B = B
           self.chosen = []
           for e in range(len(self.z)):
               if self.z[e]==1:
                   self.chosen.append(e+1)
           self.cost = self.getSolutionCost(self.chosen)

    def configuration(self):
        print("")
        print("-Configuration VND-")
        print("")
        print("A:", self.A)
        print("B:",self.B)
        print("1º Operator: switch")
        print("2º Operator: swap")
        
    def solution(self):
        print("")
        print("Infrastructure")
        print("")
        print("Chosen Stations: ",len(self.chosen))
        for e in self.chosen:
            print(self.instance.getId(e),self.getStationCost(e))
        print("Construction Cost", self.cost)
    
    
    def getStationCost(self,station):
        return self.A + self.B*self.neighborhoodStation(station)
    
    def getCost(self):
        return self.cost
    
    def getSolutionCost(self,infrastructure):
        cost = 0
        for e in infrastructure:
            cost += self.getStationCost(e)
        return cost
    
    def neighborhoodStation(self,station):
        neighborhood = 0
        for i in self.instance.customers:
            if self.instance.getDistanceMatrix(station,i) <= (self.instance.getFuelCapacity()/3):
                neighborhood += 1 
        return neighborhood

    def updateZ(self):
        self.z = [0 for k in range(len(self.z))]
        for e in self.chosen:
            self.z[e]=1
    
    def switch(self):
        print("Operator Switch")
        atvTemp = []
        if len(self.chosen) > 0:
            selected = random.choice(self.chosen)
            print("Chosen Stations: ",self.chosen)
            print("Construction Cost:",self.cost)
            print("Selected ",selected)
            atvTemp = self.chosen.copy()
            atvTemp.remove(selected)
            print("Trying Configuration: ","Total: ",len(atvTemp),"Cost: ", self.getSolutionCost(atvTemp),"Chosen: ",atvTemp)
        else:
            print("No Chosen Station")
        return atvTemp