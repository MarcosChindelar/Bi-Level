# -*- coding: utf-8 -*-
"""
@author: Chindelar
"""
import random
import math
from operator import itemgetter
#Cada formiga representa uma solução completa para o problema
class Ant():
    
    def __init__(self,col,inst):
        #Colonia que a formiga pertence
        self.colony = col
        #Matriz de distancia
        self.DistanceMatrix = inst.distanceMatrix
        #Tipo da formiga. 0 - eletrico 1 - combustao
        self.type = -1
        #Distancia total percorrida pelo carro
        self.distance = 0.00
        #Nível atual de combustível/bateria
        self.batery = 0.00
        #Demanda atual
        self.demand = 0
        #Posição atual
        self.position = 0
        #Rota atual
        self.route = []
        self.routes = []
        self.types = []
        self.visited = []
        self.electricRoutes = 0
        self.combustionRoutes = 0
        #Atualização do Feromonio feita pela melhor formiga
        self.delta = [[0 for j in range(len(inst.places))] for k in range(len(inst.places))] #Delta - Atualização dos feromonios
        #Informação Heuristica
        self.eta = [[0 if k==j else 1/self.DistanceMatrix[k][j] for k in range(len(inst.places))] for j in range(len(inst.places))] #eta - Informação Heuristica
        #Posição inicial da formiga. 0 - depósito
        inicio = 0
        self.route.append(inicio)
        #Posiciona a formiga no inicio
        self.position = inicio
        #Indica o fim da rota
        self.finish = False
        
    def checkDemand(self,local):
        demandaLocal = self.colony.instance.getDemand(local)
        if self.demand + demandaLocal <= self.colony.instance.getLoadCapacity():
            return True
        else:
            return False
    
    def checkBatery(self,local):
        distanciaLocal = round(self.DistanceMatrix[self.position][local],2)
        bateriaLocal = round(distanciaLocal*self.colony.instance.getConsuptionRatio(),2)
        if round(self.batery + bateriaLocal,2) <= self.colony.instance.getFuelCapacity():
            return True
        else:
            return False

    def checkDispLocalStation(self,local,estacao):
        if self.checkBatery(local):
            distPosLocal = round(self.DistanceMatrix[self.position][local],2)
            distLocalEstacao = round(self.DistanceMatrix[local][estacao],2)
            distanciaTotal = round(distPosLocal + distLocalEstacao,2)
            bateriaTotal = round(distanciaTotal*self.colony.instance.getConsuptionRatio(),2)
            if round(self.batery + bateriaTotal,2) <= self.colony.instance.getFuelCapacity():
                return True
            else:
                return False
        else:
            return False
    
    def checkDispLocalDepot(self,local):
        if self.checkBatery(local):
            distPosLocal = round(self.DistanceMatrix[self.position][local],2)
            distLocalDeposito = round(self.DistanceMatrix[local][0],2)
            distanciaTotal = round(distPosLocal + distLocalDeposito,2)
            bateriaTotal = round(distanciaTotal*self.colony.instance.getConsuptionRatio(),2)
            if round(self.batery + bateriaTotal,2) <= self.colony.instance.getFuelCapacity():
                return True
            else:
                return False
        else:
            return False
    
    def checkRouteBatery(self,rota):
        bateria = 0
        for _ in range(1,len(rota)):
            i = rota[_-1]
            j = rota[_]
            bateria += round(self.DistanceMatrix[i][j],2)
            if self.colony.instance.getType(j)=="f":
                bateria = 0
            if bateria > self.colony.instance.getFuelCapacity():
                return False
            else:
                return True
    
    def checkRouteDemand(self,rota):
        demanda = 0
        for _ in range(1,len(rota)):
            i = rota[_-1]
            demanda += self.colony.instance.getDemand(i)
        if demanda <= self.colony.instance.getLoadCapacity():
            return True
        else:
            return False
        
    def checkRouteViability(self,rota,tipo):
        if self.checkRouteDemand(rota)==True:
            if tipo == 0:
                if self.checkRouteBatery(rota)==True:        
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False 
        
    def checkSolutionViability(self):
        viabilidade = True
        if len(self.visited) < len(self.colony.instance.customers):
            return False
        else:
            for i in range(len(self.routes)):
                viabilidade = self.checkRouteViability(self.routes[i],self.types[i])
                if viabilidade == False:
                    return False
        return viabilidade

    def routeCost(self,rota,tipo):
        custo = 0
        distancia = 0
        for _ in range(1,len(rota)):
            i = rota[_-1]
            j = rota[_]
            distancia += round(self.DistanceMatrix[i][j],2)
        if tipo == 0:
            custo = distancia*self.colony.CE
        if tipo == 1:
            custo = distancia*self.colony.CI
        return custo

    def solutionCost(self):
        custo = 0
        i = 0
        for i in range(len(self.routes)):
            custo += self.routeCost(self.routes[i],self.types[i])            
        return custo
            
    def routeDistance(self,rota):
        distancia = 0
        for _ in range(1,len(rota)):
            i = rota[_-1]
            j = rota[_]
            distancia += round(self.DistanceMatrix[i][j],2)
        return distancia

    def routeDemand(self,rota):
        demanda = 0
        for _ in rota:
            demanda += self.colony.instance.getDemand(_)
        return demanda    

    def avaliableStations(self,chosen):
        avaliableStations = []
        for station in chosen:
            if self.checkBatery(station):
                avaliableStations.append(station)
        if len(avaliableStations) > 0:      
            tam = len(self.colony.instance.customers)
            if len(avaliableStations)>tam/4:
                con_dst = {}
                for e in avaliableStations:
                    con_dst[e]=self.colony.instance.getDistanceMatrix(self.position,e)
                con_dst_o = sorted(con_dst.items(),key=itemgetter(1))
                avaliableStations = []
                i = 0
                for i in range(int(tam/4)):
                    avaliableStations.append(con_dst_o[i][0])
        return avaliableStations

    def avaliableCustomers(self,chosen):
        avaliableCustomers = []
        if self.type == 0:
            if self.demand < self.colony.instance.getLoadCapacity():    
                for consumidor in self.colony.instance.customers:
                    if consumidor not in self.visited:
                        if self.checkBatery(consumidor):
                            if self.checkDemand(consumidor):
                                if self.colony.instance.stations == []:
                                    if self.checkDispLocalDepot(consumidor):
                                        avaliableCustomers.append(consumidor)
                                else: 
                                    for estacao in chosen:
                                        if self.checkDispLocalStation(consumidor,estacao):
                                            avaliableCustomers.append(consumidor)
                                            break
                                        else:
                                            if self.checkDispLocalDepot(consumidor):
                                                avaliableCustomers.append(consumidor)
                                                break
            else:
                avaliableCustomers = []
        if self.type ==1:
            if self.demand < self.colony.instance.getLoadCapacity():    
                for consumidor in self.colony.instance.customers:
                    if consumidor not in self.visited:
                        if self.checkDemand(consumidor):
                            avaliableCustomers.append(consumidor)
            else:
                avaliableCustomers = []         
        
       
        return avaliableCustomers

    def localClosestStation(self,local):
        selecionado = -1
        distEstMaisProxima = 10000
        for estacao in self.colony.instance.stations:
                dist_estacao = round(self.DistanceMatrix[local][estacao],2)
                if dist_estacao < distEstMaisProxima:        
                    selecionado = estacao
                    distEstMaisProxima = dist_estacao
        return selecionado

    def closestStation(self):
        selecionado = -1
        avaliableStations = self.avaliableStations()
        if len(avaliableStations) > 0:
            distEstMaisProxima = 10000
            for estacao in avaliableStations:
                dist_estacao = round(self.DistanceMatrix[self.position][estacao],2)
                if dist_estacao < distEstMaisProxima:        
                    selecionado = estacao
                    distEstMaisProxima = dist_estacao
        return selecionado
    
    def pheromoneUpdate(self):
        for i in range(len(self.colony.instance.places)):
            for j in range(len(self.colony.instance.places)):
                self.delta[i][j] = 0
        r = 0 
        for rota in self.routes: 
            for _ in range(1,len(rota)):
                i = rota[_-1]
                j = rota[_]
                self.delta[i][j] = 100/(self.colony.rho*self.solutionCost())
            r += 1
  
    def updatePosition(self,local):
        if self.type == 0:
            if local == 0:    
                self.route.append(local)
                self.routes.append(self.route)
                self.route = []
                self.distance = 0
                self.batery = 0   
                self.position = 0
                self.demand = 0    
                self.route.append(self.position)
                if self.type == 0:
                    self.electricRoutes += 1
                    self.types.append(0)
                if self.type == 1:
                    self.combustionRoutes += 1
                    self.types.append(1)
                self.type = -1
            if self.colony.instance.places[local].getType()=="c":
                distancia_consumidor = round(self.DistanceMatrix[self.position][local],2)
                self.distance  += round(distancia_consumidor,2)
                bateriaLocal = round(distancia_consumidor*self.colony.instance.getConsuptionRatio(),2)
                self.batery += round(bateriaLocal,2)
                demanda_consumidor = self.colony.instance.getDemand(local)
                self.demand += demanda_consumidor
                self.route.append(local)
                self.position = local
                self.visited.append(local)          
            if self.colony.instance.places[local].getType()=="f":
                distancia_estacao = round(self.DistanceMatrix[self.position][local],2)
                self.distance  += round(distancia_estacao,2)
                self.batery = 0
                self.position = local
                self.route.append(local)               
        if self.type == 1:
            if local == 0:
                self.route.append(local)
                self.routes.append(self.route)
                self.route = []
                self.distance = 0
                self.batery = 0   
                self.position = 0
                self.demand = 0    
                self.route.append(self.position)
                if self.type == 0:
                    self.electricRoutes += 1
                    self.types.append(0)
                if self.type == 1:
                    self.combustionRoutes += 1
                    self.types.append(1)
                self.type = -1      
            if self.colony.instance.places[local].getType()=="c":
                distancia_consumidor = round(self.DistanceMatrix[self.position][local],2)
                self.distance  += round(distancia_consumidor,2)
                demanda_consumidor = self.colony.instance.getDemand(local)
                self.demand += demanda_consumidor
                self.route.append(local)
                self.position = local
                self.visited.append(local)
    
    def selectNextGreedy(self,chosen):
        selecionado = -1
        if self.type == 0:
            if self.demand < self.colony.instance.getLoadCapacity():
                avaliableCustomers = self.avaliableCustomers(chosen)
                if len(avaliableCustomers) > 0:
                    distConsMaisProx = 1000000
                    for consumidor in avaliableCustomers:
                        distanciaConsumidor = round(self.DistanceMatrix[self.position][consumidor],2)
                        if distanciaConsumidor < distConsMaisProx:        
                            selecionado = consumidor
                            distConsMaisProx = distanciaConsumidor
                else:
                    if self.colony.instance.getType(self.position)=="f":
                        if self.checkBatery(0):
                            selecionado = 0
                        else:
                            avaliableStations = self.avaliableStations()
                            if len(avaliableStations) > 0:
                                distEstMaisProxima = 10000
                                for estacao in avaliableStations:
                                    dist_estacao = round(self.DistanceMatrix[self.position][estacao],2)
                                    if dist_estacao < distEstMaisProxima:        
                                        selecionado = estacao
                                        distEstMaisProxima = dist_estacao
                    else:
                        avaliableStations = self.avaliableStations(chosen)
                        if len(avaliableStations) > 0:
                            distEstMaisProxima = 10000
                            for estacao in avaliableStations:
                                dist_estacao = round(self.DistanceMatrix[self.position][estacao],2)
                                if dist_estacao < distEstMaisProxima:        
                                    selecionado = estacao
                                    distEstMaisProxima = dist_estacao
                        else:
                            if self.checkBatery(0):
                                selecionado = 0
                            else:
                                for estacao in self.colony.instance.stations:
                                    print("distnacia estacao:", estacao, self.DistanceMatrix[self.position][estacao])
            if self.demand == self.colony.instance.getLoadCapacity():
                if self.checkBatery(0):
                    selecionado = 0
                else:
                    avaliableStations = self.avaliableStations(chosen)
                    if len(avaliableStations) > 0:
                        distEstMaisProxima = 10000
                        for estacao in avaliableStations:
                            dist_estacao = round(self.DistanceMatrix[self.position][estacao],2)
                            if dist_estacao < distEstMaisProxima:        
                                selecionado = estacao
                                distEstMaisProxima = dist_estacao                          
        if self.type == 1:          
            if self.demand < self.colony.instance.getLoadCapacity():
                avaliableCustomers = self.avaliableCustomers(chosen)
                if len(avaliableCustomers) > 0:
                    distConsMaisProx = 10000
                    for consumidor in avaliableCustomers:
                        distanciaConsumidor = round(self.DistanceMatrix[self.position][consumidor],2)
                        if distanciaConsumidor < distConsMaisProx:        
                            selecionado = consumidor
                            distConsMaisProx = distanciaConsumidor
                else:
                    selecionado = 0
            else:
                selecionado = 0
        return selecionado       

    def selecionaProximo(self):
        selecionado = -1
        if self.type == 0:
            # print("-Selecionando Proximo-")
            if self.demand < self.colony.instance.getLoadCapacity():
                # print("Capacidade máxima não atingida")
                numerador = 0
                denominador = 0
                p = 0
                avaliableCustomers = self.avaliableCustomers(chosen)
                q = random.random()
                probabilidades = []
                # print("consumidores disponíveis: ",avaliableCustomers)
                if len(avaliableCustomers) > 0:
                    # print("Há consumidores disponiveis")
                    for consumidor in avaliableCustomers:
                        denominador +=(self.colony.feromonio[self.position][consumidor]**self.colony.alfa)*(self.eta[self.position][consumidor]**self.colony.beta)
                    for consumidor in avaliableCustomers:
                        numerador = (self.colony.feromonio[self.position][consumidor]**self.colony.alfa)*(self.eta[self.position][consumidor]**self.colony.beta)
                        p = numerador/denominador
                        probabilidades.append(p)
                    if q >= self.colony.qo:
                        p_max = max(probabilidades)
                        p_pos = probabilidades.index(p_max)
                        selecionado = avaliableCustomers[p_pos]
                    else:
                        aleatorio = random.random()
                        acumulador = 0
                        for consumidor in avaliableCustomers:
                            acumulador += probabilidades[avaliableCustomers.index(consumidor)]
                            if acumulador >= aleatorio:        
                                selecionado = consumidor
                else:
                    # print("Não ha consumidores disponiveis")
                    if self.colony.instance.getType(self.position)=="f":
                        if self.checkBatery(0):
                            selecionado = 0
                        else:
                            avaliableStations = self.avaliableStations()
                            # print("estações disponiveis: ",avaliableStations)
                            if len(avaliableStations) > 0:
                                distEstMaisProxima = 10000
                                for estacao in avaliableStations:
                                    dist_estacao = self.DistanceMatrix[self.position][estacao]
                                    if dist_estacao < distEstMaisProxima:        
                                        selecionado = estacao
                                        distEstMaisProxima = dist_estacao
                            else:
                                print("Formiga Perdida")
                    else:        
                        avaliableStations = self.avaliableStations()
                        # print("estações disponíveis: ",avaliableStations)
                        if len(avaliableStations) > 0:
                            distEstMaisProxima = 10000
                            for estacao in avaliableStations:
                                dist_estacao = self.DistanceMatrix[self.position][estacao]
                                if dist_estacao < distEstMaisProxima:        
                                    selecionado = estacao
                                    distEstMaisProxima = dist_estacao
                        else:
                            if self.checkBatery(0):
                                selecionado = 0                               
                            else:
                                for estacao in self.colony.instance.stations:
                                    print("distnacia estacao:", estacao, self.DistanceMatrix[self.position][estacao])
                                    print("Formiga Perdida")          
            if self.demand == self.colony.instance.getLoadCapacity():
                if self.checkBatery(0):
                    selecionado = 0
                else:
                    avaliableStations = self.avaliableStations()
                    # print("avaliableStations: ",avaliableStations)
                    if len(avaliableStations) > 0:
                        distEstMaisProxima = 10000
                        for estacao in avaliableStations:
                            dist_estacao = round(self.DistanceMatrix[self.position][estacao],2)
                            if dist_estacao < distEstMaisProxima:        
                                selecionado = estacao
                                distEstMaisProxima = dist_estacao                                          
        else:          
            if self.demand < self.colony.instance.getLoadCapacity():
                numerador = 0
                denominador = 0
                p = 0
                avaliableCustomers = self.avaliableCustomers(chosen)
                q = random.random()
                probabilidades = []
                # print("consumidores disponíveis: ",avaliableCustomers)
                if len(avaliableCustomers) > 0:
                    # print("Há consumidores disponiveis")
                    for consumidor in avaliableCustomers:
                        denominador +=(self.colony.feromonio[self.position][consumidor]**self.colony.alfa)*(self.eta[self.position][consumidor]**self.colony.beta)
                    for consumidor in avaliableCustomers:
                        numerador = (self.colony.feromonio[self.position][consumidor]**self.colony.alfa)*(self.eta[self.position][consumidor]**self.colony.beta)
                        p = (numerador/denominador)
                        probabilidades.append(p)                
                    if q >= self.colony.qo:
                        p_max = max(probabilidades)
                        p_pos = probabilidades.index(p_max)
                        selecionado = avaliableCustomers[p_pos]
                    else:
                        aleatorio = random.random()
                        acumulador = 0
                        for consumidor in avaliableCustomers:
                            acumulador += probabilidades[avaliableCustomers.index(consumidor)]
                            if acumulador >= aleatorio:        
                                selecionado = consumidor                  
                else:
                    selecionado = 0
            if self.demand == self.colony.instance.getLoadCapacity():
                selecionado = 0
        if selecionado == -1:
            print("Selecionado=-1, Rota=1")
            print(self.avaliableCustomers(chosen))
            print(self.colony.visitados,len(self.colony.visitados))
            for c in self.colony.instance.customers:
                if c not in self.colony.visitados:
                    print(c)
        return selecionado    