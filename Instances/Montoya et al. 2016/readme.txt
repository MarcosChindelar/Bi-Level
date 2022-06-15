Montoya et al. 2016
Instances for the electric vehicle routing problemw with non-linear charging functions
Number of instances: 120
-------------------------------------------------------------------------------------------------------------
<network>
- the node with type=0 is the depot
- the nodes with type=1 are the customers
- the nodes with type=2 are the charging stations (CSs)
- coordinates are given in km
- nodes with type=2 define the type of charging station (slow, normal, fast) in tag <cs_type>
- computations must be done using double precision (14 decimal) Euclidean distances
<fleet>
- There is just one type of electric vehicle in the 120 instances
- Routes start and end at node 0 (the depot)
- <speed_factor> is given in km/h
- <consumption_rate> defines the energy consumption in wh/km
- <battery_capacity> defines the total capacity in wh
- <function cs_type="X"> defines the charging function of the electric vehicle when charged at a station of type X
- The charging functions are piecewise linear functions with 3 break points (pus point 0,0)
- The break points are given in 2D coordinates (X:<charging_time>,Y:<battery_level>)
- <battery_level> is given in wh
- <charging_time> is given in h
<requests>
- Each customer has 1 request
- Each customer has a service time

Instances are named using the following convention: tcAcBsCcDE, where:
- A is the method used to place the customers (i.e., 0: random uniform, 1: clustered, 2: mixture of both)
- B is the number of customers
- C is the number of the CSs, 
- D is 't' if the CSs are located using a p-median heuristic and 'f' if the CSs were randomly located
- E is the number of the instance for each combination of parameters (i.e., E={0,1,2,3,4}).