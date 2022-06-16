# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 13:28:15 2020

@author: Marcos Chindelar
"""

from gurobipy import gurobipy as grbpy

class Model():
  
    def __init__(self,instance,proportion,CI,CE):
        self.instance = instance
        self.C = instance.customers.copy()
        self.CI = CI
        self.CE = CE
        self.model = grbpy.Model()
        self.alfa = proportion

    
    def solve(self,electricRouteSet,combustionRouteSet):

        electricMatrix = [[0 for j in electricRouteSet] for i in self.instance.places]
        combustionMatrix = [[0 for j in combustionRouteSet]  for i in self.instance.places]
        x = [self.model.addVar(vtype=grbpy.GRB.BINARY,name="x[%d]"%(r)) for r in range(len(electricRouteSet)) ]        
        y = [self.model.addVar(vtype=grbpy.GRB.BINARY,name="y[%d]"%(r)) for r in range(len(combustionRouteSet)) ]  

        #CALCULO DA MATRIZ DE customersXROTAS#
        r = 0
        for route in electricRouteSet:
            for _ in route:
                if self.instance.getType(_) == "c":
                    electricMatrix[_][r] = 1
            r += 1
  
        r = 0
        for route in combustionRouteSet:
            for _ in route:
                if self.instance.getType(_) == "c":
                    combustionMatrix[_][r] = 1
            r += 1        
        
        #CALCULO DO VETOR DE DISTANCIAS#
        k = 0
        distC = [0 for i in combustionRouteSet]
        for routeC in combustionRouteSet:
            for _ in range(1,len(routeC)):
                i = routeC[_-1]
                j = routeC[_]
                distC[k] += round(self.instance.getDistanceMatrix(i,j),2)
            distC[k] = distC[k]*self.CI
            k += 1
        
        k = 0
        distE = [0 for i in electricRouteSet]
        for routeE in electricRouteSet: 
            for _ in range(1,len(routeE)):
                i = routeE[_-1]
                j = routeE[_]
                distE[k] += round(self.instance.getDistanceMatrix(i,j),2)
            distE[k] = distE[k]*self.CE
            k += 1
                
        #RESTRICAO DO NUMERO DE VEICULOS ELETRICOS#
        self.model.addConstr(sum(x),grbpy.GRB.GREATER_EQUAL,(sum(x)+sum(y))*self.alfa,"Total of Electric Vehicles")        
        d = 0
        v = 0
        for c in self.instance.customers:
            d += self.instance.getDemand(c)
        v = round(d/self.instance.getLoadCapacity()+1)    
        self.model.addConstr(sum(x)+sum(y),grbpy.GRB.LESS_EQUAL,v*1.50+1,"Total of Electric Vehicles")        
        
        #RESTRICAO DA ESCOLHA DAS routeS#
        it = 0
        for customer in self.C:
            sumE = 0
            r = 0
            for route in electricRouteSet:
                sumE += x[r]*electricMatrix[customer][r]
                r += 1
            r = 0
            for route in combustionRouteSet:
                sumE += y[r]*combustionMatrix[customer][r]
                r += 1
            self.model.addConstr(sumE,grbpy.GRB.EQUAL,1,"C[%d]_restriciton"%(it))
            it  += 1
        
        #Função OBJETIVO#
        sumE = 0
        r = 0
        for _ in range(len(x)):
            sumE +=x[r]*distE[r]
            r += 1
        sumD = 0
        r = 0
        for _ in range(len(y)):
            sumD += y[r]*distC[r]
            r += 1
        funcao_objetivo = (sumE+sumD)
        self. modelo.setObjective(funcao_objetivo,grbpy.GRB.MINIMIZE)    
        self.model.optimize()
        self.model.write("LP.lp")
        
        
        electricRoutes = []
        e = 0
        for _ in x:
            if _.x == 1:
                electricRoutes.append(electricRouteSet[e])
            e += 1
        
        combustionRoutes = []
        c = 0
        for _ in y:
            if _.x == 1:
                combustionRoutes.append(combustionRouteSet[c])
            c += 1
        
        print("")
        print("Model Status:",self.model.Status,"-Optimal" ) if self.model.Status == 2 else print("Not Optinal Solution/Infeasible")
        print("Objective Function: ",round(self.model.ObjVal,2))
        print("Vehicles:",len(electricRoutes)+len(combustionRoutes))
        print("Electric Routes:")
        for re in electricRoutes:
            print(re)
        print("Combustion Routes")
        for rc in combustionRoutes:
            print(rc)      
       
        return electricRoutes,combustionRoutes
    