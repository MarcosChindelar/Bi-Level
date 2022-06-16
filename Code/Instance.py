# -*- coding: utf-8 -*-
"""
@author: Chindelar
"""
from math import degrees, atan2, sqrt
from Local import Local

#Classe responsável por gerenciar os dados das instâncias para todos os algoritmos
class Instance():
    
    def __init__(self,archive,archiveType):
        #Capacidade do tanque do veículos
        self.fuelCapacity = 0
        #Capaciade de transporte dos veículos
        self.loadCapacity = 0
        #Taxa de consumo do combustível/bateria por unidade de tempo
        self.consuptionRatio = 0
        #Taxa de recarga da bateria por unidade de tempo
        self.rechargeRatio = 0
        #Velocidade dos veículos
        self.velocity = 0
        #Matriz de distância gerado a patir de todas as localizações
        self.distanceMatrix = []
        #Lista contendo todos os locais e suas informações. Elementos do tipo Local 
        self.places = []
        #Lista contendo todos/o deposito(s). Elementos do tipo inteiro. Indice referente a posição na instância
        self.depot = []
        #Lista contendo todos consumidores. Elementos do tipo inteiro. Indice referente a posição na instância
        self.customers = []
        #Lista contendo todas as estações. Elementos do tipo inteiro. Indice referente a posição na instância
        self.stations = []
        #Lista contendo todos os locais. Elementos do tipo inteiro. Indice referente a posição na instancia
        self.points = []
        #Archive with probem data#
        self.archive = archive
        self.readFile(self.archive,archiveType)
        
    def angleWithDepot(self,local,depot):
        bearing = 0
        angle = degrees(atan2(local.getY() - depot.getY(),local.getX() - depot.getX()))
        bearing = (90 - angle) %360
        return bearing
           
    #Método que realiza leitura do arquivo com as informações da instância   
    def readFile(self,archive,archiveType):
        if archiveType == 0:
            with open(archive) as arq:
                lines = arq.readlines()
            line = lines[0].split()
            n = int(line[0])
            self.fuelCapacity = float(line[1])
            self.loadCapacity = float(line[2])
            self.consuptionRatio = float(line[3])
            self.rechargeRatio = float(line[4])
            self.velocity = float(line[5])
            for i in range(1,n+1):
                line = lines[i].split()
                Id = line[0]
                Type = line[1]
                x = float(line[2])
                y = float(line[3])
                demand = float(line[4])
                local = Local(Id,Type,x,y,demand)
                if Type =="d":
                    local.setAngle(0)
                    self.depot.append(i-1)
                    local = Local("D0","d",x,y,demand)
                    #Salva o depósito para ser utilziado como estação (caso seja possível)
                    self.places.append(local)
                if Type =="f":
                    self.places.append(local)
                    self.stations.append(i-1)
                if Type == "c":
                    local.angle = self.angleWithDepot(local,self.places[0])
                    self.places.append(local)
                    self.customers.append(i-1)
                self.points.append(i-1)
        if archiveType == 1:
            with open(archive) as arq:
                lines = arq.readlines()
            line = lines[0].split()
            n = int(line[0])
            s = int(line[1])
            c = n - s
            self.fuelCapacity = float(line[2])
            self.loadCapacity = float(line[3])
            self.consuptionRatio = float(line[4])
            self.rechargeRatio = 1.0
            self.velocity = 1.0
            line = lines[1].split()
            Id = line[0]
            x = float(line[1])
            y = float(line[2])
            local = Local(Id,"d",x,y,0)
            self.places.append(local)
            self.points.append(0)
            self.depot.append(0)
            aux = 1
            for i in range(c+1,n+1):
                line = lines[i].split()
                Id = line[0]
                x = float(line[1])
                y = float(line[2])            
                local = Local(Id,"f",x,y,0)
                self.places.append(local)
                self.points.append(aux)
                self.stations.append(aux)
                aux+=1
            for i in range(2,c+1):
                line = lines[i].split()
                Id = line[0]
                x = float(line[1])
                y = float(line[2])
                line = lines[i+n].split()
                local = Local(Id,"c",x,y,float(line[1]))
                local.angle = self.angleWithDepot(local,self.places[0])
                self.places.append(local)
                self.points.append(aux)
                self.customers.append(aux)
                aux += 1
        
        self.makeDistanceMatrix()
        
    def readFile2(self,archive):
        with open(archive) as arq:
            lines = arq.readlines()
        line = lines[0].split()
        n = int(line[0])
        s = int(line[1])
        c = n - s
        self.fuelCapacity = float(line[2])
        self.loadCapacity = float(line[3])
        self.consuptionRatio = float(line[4])
        line = lines[1].split()
        Id = line[0]
        x = float(line[1])
        y = float(line[2])
        local = Local(Id,"d",x,y,0)
        self.places.append(local)
        self.points.append(0)
        self.depot.append(0)
        aux = 1
        for i in range(c+1,n+1):
            line = lines[i].split()
            Id = line[0]
            x = float(line[1])
            y = float(line[2])            
            local = Local(Id,"f",x,y,0)
            self.places.append(local)
            self.points.append(aux)
            self.stations.append(aux)
            aux+=1
        for i in range(2,c+1):
            line = lines[i].split()
            Id = line[0]
            x = float(line[1])
            y = float(line[2])
            line = lines[i+n].split()
            local = Local(Id,"c",x,y,float(line[1]))
            self.places.append(local)
            self.points.append(aux)
            self.customers.append(aux)
            aux += 1
        self.makeDistanceMatrix()
        
    
    #Método que retorna o identificador de um local           
    def getId(self,local):
        return self.places[local].getId()
    
    #Método que retorna a demanda de um consumidor
    def getDemand(self,customer):
        return self.places[customer].getDemand()
    
    #Método que retorna a capacidade do tanque do veículos
    def getFuelCapacity(self):
        return self.fuelCapacity
    
    #Método que retorna a capacidade de carga dos veículos
    def getLoadCapacity(self):
        return self.loadCapacity
    
    #Método que retorna a taxa de consumo de combustível/bateria dos veículos
    def getConsuptionRatio(self):
        return self.consuptionRatio
    
    #Método que retorna a taxa de recarga da bateria dos véículos elétricos
    def getRechargeRatio(self):
        return self.rechargeRatio
    
    #Método que retorna a velocidade de deslocamento dos veículos
    def getVelocity(self):
        return self.velocity
    
    #Método que retorna a coordenada x de um local
    def getX(self,local):
        return self.places[local].getX()
    
    #Método que retorna a coordenda y de um local
    def getY(self,local):
        return self.places[local].getY()
    
    #Método que retorna o tipo de um local. c-consumdior/f-estação/d-depósito
    def getType(self,local):
        return self.places[local].getType()
    
    #Método que retorna o(s) indíce(s) do(s) depósito(s)
    def getDepot(self):
        return self.depot[0]
    
    #Método que retorna o indíce de uma estação na lista de estações
    def getStation(self,station):
        return self.stations[station]
    
    #Método que retorna o indíce de um consumidor na lista de consumidores
    def getCustomer(self,customer):
        return self.customers[customer]
    
    #Método que retorna o indíce de um consumidor na lista de consumidores
    def distance(self,local1,local2):
        x = local1.getX()-local2.getX()
        y = local1.getY()-local2.getY()
        return round((x**2 + y**2)**(1/2),2)
    
    #Método que aloca o espaço da matriz de distância
    def makeDistanceMatrix(self):
        for i in range(len(self.places)):
            self.distanceMatrix.append([self.distance(self.places[i],self.places[j]) 
                                          for j in range(len(self.places))])
    
    #Método que imprime a matriz de distância
    def printDistanceMatrix(self):
        auxList = []
        for i in range(len(self.places)):
            auxList.append(self.places[i].getId())
        print("  ",auxList)
        for i in range(len(self.places)):
            print(self.places[i].getId(),self.distanceMatrix[i])
    
    #Método que retorna a distancia entre dois locais com base na matriz de distancia
    def getDistanceMatrix(self,local1,local2):
        return self.distanceMatrix[local1][local2]
    
    #Método que aloca o espaço da matriz de distância - Alternativo
    def makeDistanceMatrix2(self,locais):
        for i in range(len(locais)):
            self.distanceMatrix.append([self.distancia(locais[i],locais[j]) 
                                          for j in range(len(locais))])
    
    #Método que imprime a matriz de distância - Alternativo
    def printDistanceMatrix2(self,locais):
        auxList = []
        for i in range(len(locais)):
            auxList.append(locais[i].getId())
        print("  ",auxList)
        for i in range(len(locais)):
            print(locais[i].getId(),self.distanceMatrix[i])

    #Método que retorna a distancia entre dois locais com base na matriz de distancia - Alternativo
    def getDistanceMatrix2(self,local_1,local_2):
        return self.distanceMatrix[local_1][local_2]    
    
    #Método que imprime dos dados da instância
    def printData(self):
        print("")
        print("-Data-")
        print("")
        print("Load Capacity: ",self.getLoadCapacity())
        print("Fuel Capacity: ",self.getFuelCapacity())
        print("Consuption Rate: ",self.getConsuptionRatio())
        print("Recharge Rate: ",self.getRechargeRatio())
        print("Velocity: ",self.getVelocity())
        print("")
        print("-Points-")
        print("")
        print("ID\t \t Type\t x\t \t y\t \t Demand\t Angle")
        for l in self.places:
            l.printData()
            
    
    