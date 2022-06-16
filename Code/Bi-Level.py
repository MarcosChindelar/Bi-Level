        # #Custo fixo de construção das estações
        # self.A = 500
        # #Custo por consumidor de construção das estaçõe
        # self.B = 100
        # #Custo de operação dos veículos elétricos
        # self.CE = 1
        # #Custo de operação dos veículos elétricos
        # self.CI = 4# -*- coding: utf-8 -*-
"""
@author: Chindelar
"""

from Instance import Instance
from Ant import  Ant
from Colony import Colony
from Model import Model
from Solver import Solver
from VND import VND
import numpy as np
import matplotlib.pyplot as plt

#PARAMETERS#
A = 500
B = 100
CI = 4
CE = 1
qo = 0.2
rho = 0.05
beta = 2.5
alpha = 1
eVProportion = 0.0
totalAnts = 1
maxIterations = 1
strategy = 0.0

#INITIALIZATION#
# instance = Instance("E-n22-k4.evrp",1)
instance = Instance("c101C5.txt",0)
vnd = VND(instance,A,B)
model = Model(instance,eVProportion,CI,CE)
colony = Colony(qo,rho,beta,alpha,instance,totalAnts,maxIterations,strategy,eVProportion,CI,CE)

#EXECUTION#
instance.printData()
vnd.configuration()

# solver = Solver(instance2,1,1)
# solver.solve([1,1],4,"E-n22-k4.evrp") 
# solver = Solver(instance,4,1)
# solver.solve([1,1,1,1,1,1,1,1],4,"E-n22-k4.evrp") 

iteracao = 0
print("\n")
print("Solução Inicial")
vnd.solution()
melhorInfraestrutura = vnd.chosen
colony.criaSolucaoInicial(vnd.chosen)
print(colony.bestAnt.solutionCost())
melhorFormiga = colony.bestAnt
melhorFormiga.imprimeSolucao()
# infraTemp = []
# formigaTemp = []
# while iteracao < 10:
#     print("")
#     print("Iteracao",iteracao)
#     VND.configuration()
#     melhorFormiga.imprimeSolucao()
#     infraTemp = melhorInfraestrutura
#     infraTemp = VND.switch()
#     colony.criaSolucaoInicial(infraTemp)
#     formigaTemp = colony.bestAnt
#     propTemp = (len(colony.bestAnt.types)-sum(colony.bestAnt.types))/(len(colony.bestAnt.types))
#     if propTemp > eVProportion:
#         VND.chosen = infraTemp
#         VND.updateZ()
#         VND.cost = VND.getSolutionCost(VND.chosen)
#         melhorFormiga = formigaTemp
#         VND.solution()
#         melhorFormiga.imprimeSolucao()
#     iteracao += 1

# solver = Solver(instance,4,1)
# solver.solve([1,1,1,1,1,1,],1,"c101c5")




# instancia = Instancia()
# nome_arquivo = "rc101_21"
# instancia.ler(nome_arquivo+".txt")
# instancia.criaMatrizDistancia()
# instancia.imprime()
# instancia.imprimeCustoInfraEstrutura()
# # instancia.imprimeCustoInfraEstrutura()  
# qo = 0.2
# rho = 0.05
# beta = 2.5
# alpha = 1
# proporcao = 0.0
# total_formigas = 400
# total_iteracoes = 5
# estrategia = 0.0
# colonia = Colonia(qo,rho,beta,alpha,instance,totalAnts,maxIterations,strategy,eVProportion)
# colonia.imprime()

# colonia.criaSolucaoInicial()
# # # colonia.plotaSolucao(nome_arquivo+"_NNH")
# # # colonia.melhorFormiga.imprimeSolucaoArquivo(nome_arquivo+"_NNH.txt")
# # colonia.melhorFormiga.imprimeSolucao()


# pool = colonia.geraRotas()
# modelo = Modelo(instancia,proporcao)

# eletricas = []
# combustao = []
# for formiga in pool:
#     if formiga != None:
#         r = 0
#         for rota in formiga.rotas:
#             if formiga.tipos[r] == 0:
#                 if rota not in eletricas:
#                     if colonia.calculaDemandaRota(rota) > 0:
#                         eletricas.append(rota)
#             else:
#                 if rota not in combustao:
#                     if colonia.calculaDemandaRota(rota): 
#                         combustao.append(rota)
#             r += 1

# f = Formiga(colonia,instancia)
# f.tipo = 0
# for consumidor in f.consumidoresDisponiveis():
#     rota = [0,consumidor,0]
#     if f.checaViabilidadeRota(rota,0):
#         if rota not in eletricas:
#             eletricas.append(rota)
# for consumidor in instancia.consumidores:
#     custo = 0
#     rota = []
#     melhorRota = []
#     melhorCusto = 10000
#     if consumidor not in f.consumidoresDisponiveis():
#         for estacao in instancia.estacoes:
#             rota = [0,estacao,consumidor,0]
#             if f.checaViabilidadeRota(rota,0):
#                 custo = f.calculaCustoRota(rota,0)
#                 if custo < melhorCusto:
#                     melhorRota = rota.copy()
#     eletricas.append(melhorRota)

# f = Formiga(colonia,instancia)               
# f.tipo = 1
# for consumidor in f.consumidoresDisponiveis():
#     rota = [0,consumidor,0]
#     combustao.append(rota)        

# rotasEletricasSemRepeticao = []
# for rota in eletricas:
#     if len(rota) == 0 or f.calculaDemandaRota(rota)==0 or rota == []:
#         pass
#     else:
#         rotasEletricasSemRepeticao.append(rota)
# eletricas = []
# eletricas = rotasEletricasSemRepeticao.copy()

# rotasCombustaoSemRepeticao = []
# for rota in combustao:
#     if len(rota) == 0 or f.calculaDemandaRota(rota)==0 or rota == []:
#         pass
#     else:
#         rotasCombustaoSemRepeticao.append(rota)
# combustao = []
# combustao = rotasCombustaoSemRepeticao.copy()

# colonia.melhorFormiga = Formiga(colonia,instancia)
# rotasEletricas,rotasCombustao = modelo.solve(eletricas,combustao)

# t = 0
# for rota in rotasEletricas:
#     colonia.melhorFormiga.tipos.append(0)
#     colonia.melhorFormiga.rotas.append(rotasEletricas[t])
#     colonia.melhorFormiga.rotasEletricas += 1
#     for _ in rota:
#         if _ not in colonia.melhorFormiga.visitados:
#             colonia.melhorFormiga.visitados.append(_)    
#     t += 1
# t = 0
# for rota in rotasCombustao:
#     colonia.melhorFormiga.tipos.append(1)
#     colonia.melhorFormiga.rotas.append(rotasCombustao[t])
#     colonia.melhorFormiga.rotasCombustao += 1
#     for _ in rota:
#         if _ not in colonia.melhorFormiga.visitados:
#             colonia.melhorFormiga.visitados.append(_)    
#     t += 1
      
# colonia.otimizaSolucao(True)
# # colonia.plotaSolucao(nome_arquivo+"_ACO ")
# # colonia.melhorFormiga.imprimeSolucaoArquivo(nome_arquivo+"_ACO.txt")
# colonia.melhorFormiga.imprimeSolucao()
