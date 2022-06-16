# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:04:31 2019

@author: chind
"""

from Ant import Ant
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Colony:

    def __init__(self,q,rho,beta,alpha,instance,totalAnts,maxIterations,strategy,proportion,CI,CE):
        self.qo = q
        self.rho = rho
        self.beta = beta
        self.alfa = alpha
        self.totalAnts = totalAnts
        self.maxIterations = maxIterations
        self.instance = instance
        self.strategy = strategy
        self.pheromone = [[0 for j in range(len(self.instance.places))] for k in range(len(self.instance.places))]
        self.visited = []
        self.evProportion = proportion
        self.ants = []
        self.bestAnt = None
        self.bestIterationAnt = None
        self.maxPheromone = 0
        self.minPheromone = 0
        self.CI = CI
        self.CE = CE
        for k in range(self.totalAnts):
            ant = Ant(self,instance) 
            self.ants.append(ant)
           
    def checkRouteViability(self,route,Type):
        demanda = 0
        distancia = 0
        bateria = 0
        for _ in range(1,len(route)):
            i = route[_-1]
            j = route[_]
            distancia += round(self.instance.distanceMatrix[i][j],2)
            bateria += round(self.instance.distanceMatrix[i][j],2)       
            if self.instance.getType(j)=="f":
                bateria = 0
            if Type == 0:
                if bateria > self.instance.getFuelCapacity():
                    return False
        demanda = self.routeDemand(route)
        if demanda > self.instance.getLoadCapacity():
            return False
        
        return True
           
    def routeDemand(self,route):
        demanda = 0
        for _ in range(1,len(route)):
            i = route[_-1]
            demanda += round(self.instance.getDemand(i),2)
        return  round(demanda,2)
    
    def routeCost(self,route,Type):
        custo = 0
        distancia = 0
        for _ in range(1,len(route)):
            i = route[_-1]
            j = route[_]
            distancia += round(self.instance.distanceMatrix[i][j],2)
        if Type == 0:
            custo = distancia*self.CE
        if Type ==1:
            custo = distancia* self.CI
        return  round(custo,2)

    def plotPoints(self,archiveName):
        fig, ax = plt.subplots(figsize=(20, 16))
        ax.set_xlim(xmin=-20, xmax=100)
        ax.set_ylim(ymin=-20, ymax=100)
        plt.title(archiveName)
        chosenStations = []
        for customer in self.instance.customers:
            ax.plot(self.instance.getX(customer),self.instance.getY(customer),color="blue",marker="o",markersize=6)                
            ax.text(self.instance.getX(customer),self.instance.getY(customer),self.instance.getId(customer),fontsize=10)
        for station in self.instance.stations:
            ax.plot(self.instance.getX(station),self.instance.getY(station),color="green",marker="^",markersize=6)                
            ax.text(self.instance.getX(station),self.instance.getY(station),self.instance.getId(station))
        plt.savefig(archiveName+".pdf",format="pdf")        



    def plotSolution(self,archiveName):
        fig, ax = plt.subplots(figsize=(20, 16))
        ax.set_xlim(xmin=-20, xmax=100)
        ax.set_ylim(ymin=-20, ymax=100)
        plt.title(archiveName)
        
        chosenStations = []
        for route in self.bestAnt.routes:
            for local in route:
                if self.instance.getType(local)=="f":
                    chosenStations.append(local)
        
        for customer in self.instance.customers:
            ax.plot(self.instance.getX(customer),self.instance.getY(customer),color="blue",marker="o",markersize=6)                
        for station in self.instance.stations:
            if station not in chosenStations:
                ax.plot(self.instance.getX(station),self.instance.getY(station),color="green",marker="^",markersize=6, label="Customers")                
        x = []
        y = []
        r = 0
        t = 0
        for r in range(len(self.bestAnt.routes)):
            route = self.bestAnt.routes[r]
            Type = self.bestAnt.types[t]
            for _ in range(1,len(self.bestAnt.routes[r])):
                i = route[_-1]
                j = route[_]
                if self.instance.getType(i)=="d":
                    ax.plot(self.instance.getX(0),self.instance.getY(0),color="red",fillstyle="none",marker="o",markersize=14)
                if self.instance.getType(i)=="c":
                    ax.plot(self.instance.getX(i),self.instance.getY(i),color="blue",marker="o",markersize=6)
                if self.instance.getType(i)=="f":
                    ax.plot(self.instance.getX(i),self.instance.getY(i),color="green",marker="s",markersize=6)
                if self.instance.getType(j)=="c":
                    ax.plot(self.instance.getX(j),self.instance.getY(j),color="blue",marker="o",markersize=6)
                if self.instance.getType(j)=="f":
                    ax.plot(self.instance.getX(j),self.instance.getY(j),color="green",marker="s",markersize=6)           
                x.append(self.instance.getX(i))
                y.append(self.instance.getY(i))
                x.append(self.instance.getX(j))
                y.append(self.instance.getY(j))
                if Type == 0:
                    ax.plot(x,y,color="black",linestyle="-")
                if Type == 1:
                    ax.plot(x,y,color="black",linestyle="--")
                x = []
                y = []
            t += 1
        ax.plot(self.instance.getX(0),self.instance.getY(0),color="red",fillstyle="none",marker="o",label="Depot",markersize=14)
        ax.plot(self.instance.getX(j),self.instance.getY(j),color="green",marker="^",markersize=6, label="Infrastructure(unchosen)")
        ax.plot(self.instance.getX(chosenStations[0]),self.instance.getY(chosenStations[0]),color="green",marker="s",markersize=6, label="Infrastructure(chosen)")
        ax.plot(self.instance.getX(40),self.instance.getY(40),color="blue",marker="o",markersize=6,label="Customers")
        r = 0
        for r in range(len(self.bestAnt.routes)):
            route = self.bestAnt.routes[r]
            Type = self.bestAnt.types[r]
            if Type == 0:
                x = self.instance.getX(route[0])
                y = self.instance.getY(route[1])
                ax.plot(x,y,color="black",linestyle="-",label="Routes of EV")
                break
        for r in range(len(self.bestAnt.routes)):
            route = self.bestAnt.routes[r]
            Type = self.bestAnt.types[r]
            if Type == 1:
                x = self.instance.getX(route[0])
                y = self.instance.getY(route[1])
                ax.plot(x,y,color="black",linestyle="--",label="Routes of CV")
                break     
        
        
        
        plt.legend()
        plt.savefig(archiveName+".pdf",format="pdf")
 
    def plotRoutes(self,archiveName):
        fig, ax = plt.subplots(figsize=(20, 16))
        ax.set_xlim(xmin=-20, xmax=100)
        ax.set_ylim(ymin=-20, ymax=100)
        plt.title(archiveName)
        chosenStations = []
        for route in self.bestAnt.routes:
            for local in route:
                if self.instance.getType(local)=="f":
                    chosenStations.append(local)
        for station in self.instance.stations:
            if station not in chosenStations:
                ax.plot(self.instance.getX(station),self.instance.getY(station),color="green",marker="^",markersize=6)    
        i = 0
        for i in range(len(self.bestAnt.routes)):
            self.plotRoute(self.bestAnt.routes[i],self.bestAnt.types[i])

        plt.savefig(archiveName+".pdf",format="pdf")    
    
    def plotRoute(self,route,Type):
        fig, ax = plt.subplots(figsize=(20, 16))
        ax.set_xlim(xmin=-20, xmax=100)
        ax.set_ylim(ymin=-20, ymax=100)
        x = []
        y = []
        for _ in range(1,len(route)):
            i = route[_-1]
            j = route[_]
            if self.instance.getType(i)=="d":
                ax.plot(self.instance.getX(0),self.instance.getY(0),color="red",fillstyle="none",marker="o",markersize=14)
                ax.plot(self.instance.getX(0),self.instance.getY(0),color="red",fillstyle="none",marker="^",markersize=10)
            if self.instance.getType(i)=="c":
                ax.plot(self.instance.getX(i),self.instance.getY(i),color="blue",marker="o",markersize=6)
            if self.instance.getType(i)=="f":
                ax.plot(self.instance.getX(i),self.instance.getY(i),color="green",marker="s",markersize=6)
            if self.instance.getType(j)=="c":
                ax.plot(self.instance.getX(j),self.instance.getY(j),color="blue",marker="o",markersize=6)
            if self.instance.getType(j)=="f":
                ax.plot(self.instance.getX(j),self.instance.getY(j),color="green",marker="s",markersize=6)           
            x.append(self.instance.getX(i))
            y.append(self.instance.getY(i))
            x.append(self.instance.getX(j))
            y.append(self.instance.getY(j))
            if Type == 0:
                ax.plot(x,y,color="black",linestyle="-")
            if Type == 1:
                ax.plot(x,y,color="black",linestyle="--")
            x = []
            y = []

    def configuration(self):
        print("")
        print("-Configuração ACO-")
        print("")
        print("rho:",self.rho)
        print("beta:",self.beta)
        print("alfa:",self.alfa)
        print("ants:",self.totalAnts)
        print("iterações:",self.maxIterations)
        print("estrategia:",self.strategy)

    def solution(self):
        custoEletrico = 0
        distanciaEletrica = 0
        distanciaCombustao = 0
        custoCombustao = 0
        routesEletricas = []
        routesCombustao = []
        t = 0
        for route in self.bestAnt.routes:
            if self.bestAnt.types[t] == 0:
                routesEletricas.append(route)
                for _ in range(1,len(route)):
                    i = route[_-1]
                    j = route[_]
                    distanciaEletrica += round(self.instance.distanceMatrix[i][j],2)              
                t += 1
            else:
                routesCombustao.append(route)
                for _ in range(1,len(route)):
                    i = route[_-1]
                    j = route[_]
                    distanciaCombustao += round(self.instance.distanceMatrix[i][j],2)
                t += 1
        custoEletrico = round(distanciaEletrica*self.CE,2)
        custoCombustao = round(distanciaCombustao*self.CI,2)
        print("")
        print("Solucao:")
        print("Distancia EV: ",distanciaEletrica)
        print("Custo EV: ",custoEletrico)
        print("routes EV: ")
        for routeEletrica in routesEletricas:
            print(routeEletrica)
        print("Distancia CV: ",distanciaCombustao)
        print("Custo CV: ",custoCombustao)
        print("routes CV: ")
        for routeCombustao in routesCombustao:
            print(routeCombustao)        
        print("Custo total: ",custoCombustao+custoEletrico)
        print("visited:",self.visited, len(self.visited))
    
    def pheromoneUpdate(self,globalBest):
        for i in range(len(self.instance.places)):
            for j in range(len(self.instance.places)):
                self.pheromone[i][j] = (1-self.rho)*self.pheromone[i][j]
        
        if globalBest == False:
            for route in self.bestIterationAnt.routes:
                for _ in range(1,len(route)):
                    i = route[_-1]
                    j = route[_]
                    self.pheromone[i][j] += self.bestIterationAnt.delta[i][j]
        else:
            for route in self.bestAnt.routes:
                for _ in range(1,len(route)):
                    i = route[_-1]
                    j = route[_]
                    self.pheromone[i][j] += self.bestAnt.delta[i][j]            
        
        for i in range(len(self.instance.places)):
            for j in range(len(self.instance.places)):
                if self.pheromone[i][j] <self.minPheromone:
                    self.pheromone[i][j] =self.minPheromone
                if self.pheromone[i][j] > self.maxPheromone:
                    self.pheromone[i][j] = self.maxPheromone                                
    
    def pheromoneInitialization(self):
        custoSolInicial = self.bestAnt.solutionCost()
        self.maxPheromone = 100/(self.rho*custoSolInicial)
        self.minPheromone = (self.maxPheromone*(1-(0.05**(1/100))))/((50-1)*(0.05**(1/100)))
        for i in range(len(self.instance.places)):
            for j in range(len(self.instance.places)):                
                self.pheromone[i][j] = self.maxPheromone
                
    def removeStation(self,route):
        newRoute = []
        for local in route:
            if self.instance.getType(local)=="f":
                newRoute = route.copy()
                newRoute.remove(local)
                viabilidade = self.checkRouteViability(newRoute,0)
                if viabilidade == True:
                    route = newRoute.copy()
        return route

    def changeStation(self,route):
        newRoute = []
        for local in route:
            if self.instance.getType(local)=="f":
                for station in self.instance.stations:                    
                    newRoute = route.copy()
                    indiceLocal = newRoute.index(local)
                    newRoute.remove(local)
                    newRoute.insert(indiceLocal,station)
                viabilidade = self.checkRouteViability(newRoute,0)
                if viabilidade == True:
                    custoNovo = self.routeCost(newRoute,0)
                    custoAtual = self.routeCost(route,0)
                    if custoNovo < custoAtual:                        
                        route = newRoute.copy()
                    else:
                        newRoute = route.copy()
                else:
                    newRoute = route.copy()
        return route        

    def twoOpt(self,route,Type):
        if Type == 1:
            melhorroute = route.copy()
            melhora = True
            while melhora:
                melhora = False
                for i in range(1, len(route)-2):
                    for j in range(i+1, len(route)):
                        if j-i == 1: continue # changes nothing, skip then
                        newRoute = route[:]
                        newRoute[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                        if self.routeCost(newRoute,Type) < self.routeCost(melhorroute,Type):
                            melhorroute = newRoute.copy()
                            melhora = True
                route = melhorroute.copy()
            return melhorroute
        if Type == 0:
            melhorroute = route.copy()
            melhora = True
            while melhora:
                melhora = False
                for i in range(1, len(route)-2):
                    for j in range(i+1, len(route)):
                        if j-i == 1: continue # changes nothing, skip then
                        newRoute = route[:]
                        newRoute[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                        if round(self.routeCost(newRoute,Type),2) < round(self.routeCost(melhorroute,Type),2):
                            if self.checkRouteViability(newRoute,Type)==True:
                                melhorroute = newRoute.copy()
                                melhora = True
                route = melhorroute.copy()
            return melhorroute     

    def combinaroutes(self,globalBest):
        if globalBest == True:
            currentRoute = []
            routeAux = []
            bestrCurrentRoute = []
            bestRouteAux = []
            TypebestrCurrentRoute = -1
            TypebestRouteAux = -1
            for route in range(len(self.bestAnt.routes)):
                currentRoute = self.bestAnt.routes[route].copy()
                bestrCurrentRoute = self.bestAnt.routes[route].copy()
                TypebestrCurrentRoute = self.bestAnt.types[route]
                for currentLocal in currentRoute:
                    if currentLocal != 0 and self.instance.getType(currentLocal)!="f":
                        for routeAux in range(route+1,len(self.bestAnt.routes)):
                            routeAux = self.bestAnt.routes[route+1].copy()
                            bestRouteAux = self.bestAnt.routes[route+1].copy()
                            TypebestRouteAux = self.bestAnt.types[route+1]
                            for localAux in routeAux:
                                if localAux != 0 and self.instance.getType(localAux)!="f":
                                    currentIndex = currentRoute.index(currentLocal)
                                    auxIndex = routeAux.index(localAux)
                                    currentRoute.remove(currentLocal)
                                    routeAux.remove(localAux)
                                    currentRoute.insert(currentIndex,localAux)
                                    routeAux.insert(auxIndex,currentLocal)
                                    if self.checkRouteViability(currentRoute,self.bestAnt.types[route]) == True and self.checkRouteViability(routeAux,self.bestAnt.types[route+1])==True:
                                        newCost = self.routeCost(currentRoute,self.bestAnt.types[route])+self.routeCost(routeAux,self.bestAnt.types[route+1])
                                        bestCost = self.routeCost(bestrCurrentRoute,TypebestrCurrentRoute)+self.routeCost(bestRouteAux,TypebestRouteAux)
                                        if newCost < bestCost:                                            
                                            bestrCurrentRoute = []
                                            bestrCurrentRoute = currentRoute.copy()
                                            bestRouteAux = []
                                            bestRouteAux = routeAux.copy()
                                            currentRoute = self.bestAnt.routes[route].copy()
                                            routeAux = self.bestAnt.routes[route+1].copy()
                                        else:
                                            currentRoute = self.bestAnt.routes[route].copy()
                                            routeAux = self.bestAnt.routes[route+1].copy()
                                    else:
                                        currentRoute = self.bestAnt.routes[route].copy()
                                        routeAux = self.bestAnt.routes[route+1].copy()
                            self.bestAnt.routes[route+1] = bestRouteAux.copy()
            if globalBest==False:
                currentRoute = []
                routeAux = []
                bestrCurrentRoute = []
                bestRouteAux = []
                TypebestrCurrentRoute = -1
                TypebestRouteAux = -1
                for route in range(len(self.bestIterationAnt.routes)):
                    currentRoute = self.bestIterationAnt.routes[route].copy()
                    bestrCurrentRoute = self.bestIterationAnt.routes[route].copy()
                    TypebestrCurrentRoute = self.bestIterationAnt.types[route]
                    for currentLocal in currentRoute:
                        if currentLocal != 0 and self.instance.getType(currentLocal)!="f":
                            for routeAux in range(route+1,len(self.bestIterationAnt.routes)):
                                routeAux = self.bestIterationAnt.routes[route+1].copy()
                                bestRouteAux = self.bestIterationAnt.routes[route+1].copy()
                                TypebestRouteAux = self.bestIterationAnt.types[route+1]
                                for localAux in routeAux:
                                    if localAux != 0 and self.instance.getType(localAux)!="f":
                                        currentIndex = currentRoute.index(currentLocal)
                                        auxIndex = routeAux.index(localAux)
                                        currentRoute.remove(currentLocal)
                                        routeAux.remove(localAux)
                                        currentRoute.insert(currentIndex,localAux)
                                        routeAux.insert(auxIndex,currentLocal)
                                        if self.checkRouteViability(currentRoute,self.bestIterationAnt.types[route]) == True and self.checkRouteViability(routeAux,self.bestIterationAnt.types[route+1])==True:
                                            newCost = self.routeCost(currentRoute,self.bestIterationAnt.types[route])+self.routeCost(routeAux,self.bestIterationAnt.types[route+1])
                                            bestCost = self.routeCost(bestrCurrentRoute,TypebestrCurrentRoute)+self.routeCost(bestRouteAux,TypebestRouteAux)
                                            if newCost < bestCost:                                                
                                                bestrCurrentRoute = []
                                                bestrCurrentRoute = currentRoute.copy()
                                                bestRouteAux = []
                                                bestRouteAux = routeAux.copy()
                                                currentRoute = self.bestIterationAnt.routes[route].copy()
                                                routeAux = self.bestIterationAnt.routes[route+1].copy()
                                            else:
                                                currentRoute = self.bestIterationAnt.routes[route].copy()
                                                routeAux = self.bestIterationAnt.routes[route+1].copy()
                                        else:
                                            currentRoute = self.bestIterationAnt.routes[route].copy()
                                            routeAux = self.bestIterationAnt.routes[route+1].copy()
                                self.bestIterationAnt.routes[route+1] = bestRouteAux.copy()                
                                        
    
    def optmizeSolution(self,globalBest):
        r = 0
        t = 0
        newRoute = []               
        if globalBest == True:
            previously = self.bestAnt.solutionCost() 
            for r in range(len(self.bestAnt.routes)):
                newRoute = self.removeStation(self.bestAnt.routes[r])
                self.bestAnt.routes[r] = newRoute.copy()
                newRoute = self.changeStation(self.bestAnt.routes[r])
                self.bestAnt.routes[r] = newRoute.copy()
                newRoute = self.twoOpt(self.bestAnt.routes[r],self.bestAnt.types[t])
                self.bestAnt.routes[r] =  newRoute.copy()
                t +=1
            # print("melhora solução global:",-100*round((self.bestAnt.solutionCost()-previously)/previously,2),"%")
        
        else:
            previously = self.bestIterationAnt.solutionCost() 
            for r in range(len(self.bestIterationAnt.routes)):
                newRoute = self.removeStation(self.bestIterationAnt.routes[r])
                self.bestIterationAnt.routes[r] = newRoute.copy()
                newRoute = self.changeStation(self.bestIterationAnt.routes[r])
                self.bestIterationAnt.routes[r] = newRoute.copy()
                newRoute = self.twoOpt(self.bestIterationAnt.routes[r],self.bestIterationAnt.types[t])
                self.bestIterationAnt.routes[r] =  newRoute.copy()
                t +=1            
            # print("melhora solução iteração:",-100*round((self.bestIterationAnt.solutionCost()-previously)/previously,2),"%")

 
