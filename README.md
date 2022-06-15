<h1>Project Description</h1>

Electric vehicles are becoming increasingly popular in transportation systems dueto subsidies provided by governments that seek to increase their adoption by companies
that, in turn, seek to lower the operating cost of their fleet. In this way, we have two agents involved in the process, with each one aiming to solve its own 
optimization problem, namely the Recharge Station Allocation Problem, which is the responsibility of the government, and the Vehicle Routing Problem, the responsibility of the company. company. A two-level
optimization problem arises when the interests of both are addressed simultaneously. In addition, both electric and internal combustion vehicles can be used, 
increasing the complexity of the problem. This work proposes a solution strategy that combines the Variable Neighborhood Descent metaheuristic with Ant Colony 
Optimization with Local Search and a Route Selection Procedure for solving a two-level optimization problem involving the Allocation Problem of Stations at the upper 
level and the Vehicle Routing Problem at the lower level. Variable Neighborhood Descent is applied at the top level, while Ant Colony Optimization and other methods 
are used at the lower level.

Below are the works that were used as a basis for the elaboration of this strategy:

https://onlinelibrary.wiley.com/doi/abs/10.1002/9781119686750.ch9

Summary

This chapter presents a general analysis of multilevel optimization problems involving electric vehicles. It initially presents models commonly found in the literature 
for multilevel optimization problems, as well as details regarding the objectives and constraints involved in multilevel models. Most of them are bi-level optimization 
problems and involve the allocation of charging stations and users' equilibrium. In the sequence, some search techniques commonly adopted for solving multilevel 
optimization problems of electric vehicles are presented. These search techniques can be classified as exact or approximate methods. The approximate methods can be 
classified as populational-based or single-solution based approaches, where the populational methods evolve a set of candidate solutions. Simulated Annealing and 
Neighborhood Search can be classified as single and stochastic methods. On the other hand, populational and stochastic techniques, such as Genetic Algorithms, ]
Imperialism Competitive Algorithm, and Particle Swarm Optimization, were also found in the literature solving the type of problem outlined in the chapter.

https://link.springer.com/article/10.1007/s10489-021-02748-x

Abstract

Electric vehicles are becoming popular in transport systems due to subsidies provided by the governments and the reduction of environmental issues. A bilevel 
optimization problem rises when the interests of governments (minimizing the infrastructure costs) and transportation companies (minimizing the routing costs) are 
considered. Also, both electric vehicles and internal combustion vehicles can be used, increasing the complexity of the problem. This work proposes a Variable 
Neighborhood Descent combined with an Ant Colony Optimization with local search and a Route Selection Procedure for solving a bilevel optimization problem. Variable 
Neighborhood Descent is applied at the upper level in the Station Allocation Problem while Ant Colony Optimization with local search and Route Selection Procedure are 
applied to the lower level in the Vehicle Routing Problem. Computational experiments were performed using two different sets of instances and the results obtained 
indicate that the proposal achieved good results at both levels when compared with other approaches from the literature, with low construction and routing cost and 
always keeping the proportion of electric vehicles higher than requested.

https://link.springer.com/chapter/10.1007/978-3-030-86230-5_17

Abstract

With the grown of global concern with environmental issues and incentives on the part of governments, the use of electric vehicles (EVs) by companies has increased. 
By joining the interest of governments on minimizing the costs of building the recharging infrastructure and of companies on minimizing their transport costs with 
the adoption of electric vehicles in their fleet, a bilevel optimization problem arises. An approach that combines the Variable Neighborhood Search (VND) with an Ant 
Colony Optimization (ACO) to solve this bilevel model is proposed here. The results of the computational experiments using different benchmark instances indicate the 
superior performance of the proposed approach, mainly in the allocation of the charging infrastructure (objective of the leader). Also, the proposal found better 
solutions than those from the literature while maintains the percentage of electric vehicles that compose the fleet above the required limit.

https://ieeexplore.ieee.org/document/8628831

Abstract:

Ant colony optimization (ACO) algorithms have proved to be powerful tools to solve difficult optimization problems. In this paper, ACO is applied to the electric 
vehicle routing problem (EVRP). New challenges arise with the consideration of electric vehicles instead of conventional vehicles because their energy level is 
affected by several uncertain factors. Therefore, a feasible route of an electric vehicle (EV) has to consider visit(s) to recharging station(s) during its daily 
operation (if needed). A look ahead strategy is incorporated into the proposed ACO for EVRP (ACO-EVRP) that estimates whether at any time EVs have within their range 
a recharging station. From the simulation results on several benchmark problems it is shown that the proposed ACO-EVRP approach is able to output feasible routes, 
in terms of energy, for a fleet of EVs.

https://www.sciencedirect.com/science/article/abs/pii/S0959652617328123

Abstract

Governments take an active role in promoting electric vehicles (EVs), but the lack of recharging infrastructures restricts companies to adopt EVs. To promote EVs' 
penetration in companies, a suitable public recharging infrastructure grid should be systematically designed by governments. This paper proposes a public recharging 
infrastructure location strategy for governments based on the bi-level programming. In the upper-level problem, the government optimizes his location strategy, i.e., 
selects infrastructures from candidate locations, to minimize the construction budget and meet desired EV adoption rate. In the lower-level problem, the company 
decides the percentage of the electric vehicles in her mixed fleet and the corresponding vehicle routing plan to minimize her operational cost utilizing the 
infrastructures constructed by the government. A two-phase heuristic combining variable neighborhood descent and scatter search is presented to solve the problem. 
The hybrid method hires scatter search to derive the optimal routing plan of mixed fleet and variable neighborhood descent to select infrastructure locations. 
The proposed method is examined against Cplex using benchmark instances. The results from extensive numerical studies reveal that the government should thoughtfully 
determine the desired adoption rate. The short-term optimal locations might be inefficient design for the long run if the rate varies. In order to minimize the budget,
the government may not choose the infrastructure locations that are the most beneficial for the company. It's hard to achieve the desired adoption rate while 
considering the covering areas of the infrastructures merely. The subsidy policy and recharging infrastructure location strategy should be systematically designed to 
achieve a higher promoting effect with a lower budget.
