# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 21:42:02 2019

@author: chind
"""

from gurobipy import gurobipy as grbpy

class Solver():
  
    def __init__(self,instance,CI,CE):
        self.instance = instance
        self.V = instance.points
        self.S = instance.stations
        self.C = instance.customers
        self.CI = CI
        self.CE = CE
        self.M = 10000
    
    def solve(self,z,k,instance_name):
        #RESTRICAO DO NUMERO DE VEICULOS ELETRICOS#
        TotalDemand = 0
        for c in self.instance.customers:
            TotalDemand += self.instance.getDemand(c)
        # v = round(TotalDemand/self.instance.getLoadCapacity()+1)    
        self.K = k
        self.Z = z
        self.model = grbpy.Model()
        TD_EV = [self.model.addVar(vtype=grbpy.GRB.CONTINUOUS,lb=0.0,ub=self.M,name="TDEV[%d]"%(k)) for k in range(self.K)]        
        TD_CV = [self.model.addVar(vtype=grbpy.GRB.CONTINUOUS,lb=0.0,ub=self.M,name="TDCV[%d]"%(k)) for k in range(self.K)]
        y = [self.model.addVar(vtype=grbpy.GRB.BINARY,lb=0,ub=1,name="y[%d]"%(k)) for k in range(self.K)]
        p_1 = [[self.model.addVar(vtype=grbpy.GRB.CONTINUOUS,lb=0,name="p1[%d][%d]"%(g,k)) for k in range(self.K)] for g in self.V]
        p_2 = [[self.model.addVar(vtype=grbpy.GRB.CONTINUOUS,ub=self.instance.getFuelCapacity(),name="p2[%d][%d]"%(g,k)) for k in range(self.K)] for g in self.V]
        x = [[[self.model.addVar(vtype=grbpy.GRB.BINARY,lb=0,ub=1,name="x[%d][%d][%d]"%(g,h,k)) 
        for k in range(self.K)] for h in range(len(self.V))] for g in range(len(self.V))]
        u = [[self.model.addVar(vtype=grbpy.GRB.BINARY,lb=0,ub=1,name="u[%d][%d]"%(g,k)) for k in range(self.K)] for g in self.V]
        t = [self.model.addVar(vtype=grbpy.GRB.INTEGER,ub=self.M,name="u[%d]"%(g)) for g in self.V]

        #Eliminação de Subrotas#
        it = 0
        for g in range(1,len(self.V)):
            for h in range(len(self.V)):
                for k in range(self.K):
                    if g!=h:
                        self.model.addConstr(t[g]-t[h]+(len(self.V)*x[g][h][k]),
                                              grbpy.GRB.LESS_EQUAL,len(self.V)-1,"Sub_Route%d"%(it))
                        it = it + 1
                        
        #R5#
        it = 0
        for c in self.C:
            restricao = 0
            for g in self.V:
                if g!=c:
                    for k in range(self.K):
                        restricao = restricao + x[g][c][k]
            self.model.addConstr(restricao,grbpy.GRB.EQUAL, 1,"R5_%d"%(it))
            it = it + 1
            
        #R6#
        it = 0
        for k in range(self.K):
            restricao = 0
            for h in range(1,len(self.V)):
                restricao = restricao + x[0][h][k]
            self.model.addConstr(restricao,grbpy.GRB.LESS_EQUAL,1,"R6_%d"%(it))
            it = it + 1
            
        #R7#
        it = 0
        for k in range(self.K):
            for v in self.V:
                restricao_esquerda = 0
                restricao_direita = 0
                for g in self.V:
                    if g!=v:
                        restricao_esquerda = restricao_esquerda + x[g][v][k]
                for h in self.V:
                    if h!=v:
                        restricao_direita = restricao_direita + x[v][h][k]
                self.model.addConstr(restricao_esquerda,grbpy.GRB.EQUAL,restricao_direita,"R7_%d"%(it))
                it = it + 1

        #R8#
        it = 0
        for k in range(self.K):
            restricao = 0
            for c in self.C:
                for v in self.V:
                    restricao = restricao + self.instance.getDemand(c)*x[c][v][k]
            self.model.addConstr(restricao, grbpy.GRB.LESS_EQUAL, self.instance.getLoadCapacity(),"R8_%d"%(it))
            it = it + 1
        
        #R9->R15#
        it = 0
        for k in range(self.K):
            for g in self.V:
                for h in self.V:
                    self.model.addConstr(p_1[h][k],grbpy.GRB.LESS_EQUAL, p_2[g][k] - 
                                     (self.instance.getConsuptionRatio()*self.instance.getDistanceMatrix(g,h)*x[g][h][k]) + 
                                     (self.M*(2 - x[g][h][k] - y[k])),"R9->R15_%d"%(it))
                    it = it + 1
                    
        #R10#
        it = 0
        for k in range(self.K):
            self.model.addConstr(p_2[0][k],grbpy.GRB.EQUAL, self.instance.getFuelCapacity(),"R10_%d"%(it))
            it = it + 1
        
        #R11#
        it = 0
        for k in range(self.K):
            estacao = 0
            for s in self.S:
                self.model.addConstr(p_2[s][k] ,grbpy.GRB.EQUAL,self.instance.getFuelCapacity()*self.Z[estacao],"R11_%d"%(it))
                it = it + 1
                estacao = estacao + 1
        
        #R12#
        for k in range(self.K):
            for c in self.C:
                self.model.addConstr(p_2[c][k],grbpy.GRB.EQUAL,p_1[c][k],"R112_%d"%(it))
                it = it + 1
                
        #R13#
        for k in range(self.K):
            for v in self.V:
                self.model.addConstr(p_1[v][k],grbpy.GRB.GREATER_EQUAL, 0,"R13_%d"%(it))
                it = it + 1
        
        #R17#
        it = 0
        for k in range(self.K):
            restricao = 0
            for g in self.V:
                for h in self.V:
                    restricao = restricao + self.instance.getDistanceMatrix(g,h)*x[g][h][k]
            self.model.addConstr(restricao,grbpy.GRB.LESS_EQUAL, TD_EV[k] + (self.M*(1 - y[k])),"R17_%d"%(it))
            it = it + 1
 
        #R18#
        it = 0
        for k in range(self.K):
            restricao = 0
            for g in self.V:
                for h in self.V:
                    restricao = restricao + self.instance.getDistanceMatrix(g,h)*x[g][h][k]
            self.model.addConstr(restricao ,grbpy.GRB.LESS_EQUAL, TD_CV[k] + (self.M*y[k]),"R18_%d"%(it))
            it = it + 1
            
        #R19#
        it = 0
        for k in range(self.K):
            self.model.addConstr(TD_EV[k] ,grbpy.GRB.GREATER_EQUAL,0,"R19EV_[%d]"%(it))
            self.model.addConstr(TD_CV[k],grbpy.GRB.GREATER_EQUAL, 0,"R19CV_[%d]"%(it))
            it = it + 1
        
        #R4->R16/FC#
        funcao_objetivo = (self.CI*sum(TD_CV)) + (self.CE*sum(TD_EV))
        self. model.setObjective(funcao_objetivo,grbpy.GRB.MINIMIZE)
        
        self.model.setParam("Heuristics",0.25)
        self.model.setParam("MIPGap",0.50)
        self.model.setParam("MIPFocus",1) 
        self.model.setParam("TimeLimit",300)
        self.model.setParam("OutputFlag",0)
        self.model.optimize()
        
        if self.model.SolCount > 0:
            print("\nModel Stats: %d - "%(self.model.status),"Optimal") if self.model.status == 2 else print("\nModel Stats: %d"%(self.model.status))
            print("\nObjective Function: %.2f"%(self.model.objVal))
            print("\nTime: %.2f"%(self.model.Runtime))
            self.model.write(instance_name+"_LPmodel.lp")
                  
            matriz_distancia = [[[0 for k in range(self.K)] for h in range(len(self.V))] for g in range(len(self.V))]    
            for k in range(self.K):
                for g in range(len(self.V)):
                    for h in range(len(self.V)):
                        if x[g][h][k].x > 0.0:
                            matriz_distancia[g][h][k] = int(x[g][h][k].x)
            
            arq_name = instance_name+"_result.txt"
            with open(arq_name,'a') as f:
                print("Objective Function: ",file = f)
                print("fc = %.2f"%(self.model.objVal),file = f)
                
                print("\nTime: ",file = f)
                print("tc = %.2f"%(self.model.Runtime),file = f)
               
                if self.model.status == 2:
                    print("\nModel Stats:",file =f)
                    print("%d - Optimal Solution"%(self.model.status),file =f)
                
                print("\nVehicles:",file = f)
                print(self.K,file = f)
                
                print("\nAlfa: ",file = f)
                alfa = 0
                for i in range(self.K):
                    if y[i].x == 1:
                        alfa = alfa + 1
                alfa = (alfa/self.K)*100
                print("alfa = %2.f"%(alfa),"%",sep='',file = f)
                
                print("\nRoute Matrix:",file = f)
                for k in range(self.K):
                    for g in range(len(self.V)):
                        for h in range(len(self.V)):
                            if x[g][h][k].x >0.0:
                                print("x[%d][%d][%d] = %d"%(g,h,k,x[g][h][k].x),file = f)            
                rotas = []
                rota = []
                i = 0
                for k in range(self.K):
                    for g in range(len(self.V)):
                        for h in range(len(self.V)):
                            if matriz_distancia[g][h][k] > 0:
                                rota.append(self.instance.getId(g))
                                i = h
                        break
                    h = 0
                    while i != 0 and h != len(self.V):
                        if matriz_distancia[i][h][k] > 0:
                            rota.append(self.instance.getId(i))
                            i = h
                            h = 0
                        else:
                            h = h +1
                    if len(rota)>0:
                        rota.append(self.instance.getId(0))
                        rotas.append(rota)
                        rota = []
                                
                
                for rota in rotas:
                    print("\Route%d:"%(k),file = f)
                    for r in range(len(rota)-1):
                        print(rota[r],"->",end="",sep="",file = f)
                    print(self.instance.getId(0),file = f)
                                                    
                print("\nDistance of each vehicle: ",file = f)
                for k in range(self.K):
                    print("TDEV[%d] = %.2f"%(k,TD_EV[k].x),file = f)
                
                for k in range(self.K):
                    print("TDCV[%d] = %.2f"%(k,TD_CV[k].x),file = f)
                
                print("\Stations: ",file = f)    
                for s in range(len(self.S)):
                    print("z[%d] = %d"%(s,z[s]),file = f)
                
                print("\Vehicles: ",file = f)    
                for k in range(self.K):
                    print("y[%d] = %d"%(k,y[k].x),file = f)
                f.close()
            
            grbpy.disposeDefaultEnv()
            
            return matriz_distancia
        else:
            print("No feasible solution found in time limit: ",self.model.Params.TimeLimit)