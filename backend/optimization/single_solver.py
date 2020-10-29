import numpy as np
from scipy.optimize import minimize
import math


# For Nitrogen, specially handle Urea and Vijetha to ignore one of them when prices of both are same
def nitrogen_fert_filter(fertilizer_name,N_qty_per_bag,fertilizer_bag_cost):
    urea_found = False;
    urea_index = vijetha_index = 0;
    vijetha_found = False;

    for i in range(len(fertilizer_name)):
        # Check if Urea and Vijetha exist together and if both have the same cost, remove Vijetha
        if fertilizer_name[i] == "Urea":
            urea_found = True;
            urea_index = i;
        if fertilizer_name[i] == "Vijetha":
            vijetha_found = True;
            vijetha_index = i;

    if (urea_found) and (vijetha_found):
        if(fertilizer_bag_cost[urea_found] == fertilizer_bag_cost[vijetha_found]):
            N_qty_per_bag[vijetha_index] = 0;

    return N_qty_per_bag

# Objective function - minimize total cost
def objective(fertilizer_bag_cost,fertilizer_bag_required):
  return (sum(x*y for x,y in zip(fertilizer_bag_cost,fertilizer_bag_required)))

# # Objective function - minimize number of fertilizers
# def objective2(fertilizer_bag_required):
#   return (len(np.nonzero(fertilizer_bag_required)[0]))

# Constraint function - For ach of N,P,K : deficit = sumproduct(quantity (N or P or K) * fertilizer_bag_required)
def constraint(fertilizer_bag_required,fertilizer_qty_per_bag,fertilizer_deficit):
  return (sum(x*y for x,y in zip(fertilizer_bag_required,fertilizer_qty_per_bag)) - fertilizer_deficit)

# Constraint function - For ach of N,P,K : deficit = sumproduct(quantity (N or P or K) * fertilizer_bag_required)
def roundup(x):
    g0 = round(int(math.ceil(x / 0.05)) * 0.05,2)
    g1 = math.modf(g0);

    if g1[0] >= 0.7:
        t = math.ceil(g0);
    elif g1[0] <= 0.3:
        t = math.floor(g0);
    else:
        # round to nearest 0.5 when the fertilizer value is between 0.31 to 0.69
        t = round(g0 * 2.0) / 2.0;

    return t

#Main optimization logic to derive the quantity of each fertilizer
def optimize_minimize(N_deficit,P_deficit,K_deficit,fertilizer_bag_required,fertilizer_bag_cost,fertilizer_name,N_qty_per_bag, P_qty_per_bag,K_qty_per_bag,fertilizer_bag_weight):
    N_qty_per_bag = nitrogen_fert_filter(fertilizer_name,N_qty_per_bag,fertilizer_bag_cost);
    b  = [];

    for i in range(0,len(fertilizer_name)):
        individual_bound = [];

        # Defining lower boundary as 0
        individual_bound.append(0);

        # Boundary for N
        if N_qty_per_bag[i] == 0:
            n_bound = 0;
        else:
            n_bound = (math.floor(N_deficit/N_qty_per_bag[i]));
        # Boundary for P
        if P_qty_per_bag[i] == 0:
            p_bound = 0;
        else:
            p_bound = (math.floor(P_deficit/P_qty_per_bag[i]));
        # Boundary for K
        if K_qty_per_bag[i] == 0:
            k_bound = 0
        else:
            k_bound = (math.floor(K_deficit/K_qty_per_bag[i]));

        # Defining Upper boundary
        individual_bound.append(n_bound + p_bound + k_bound);

        b.append(tuple(individual_bound));

    bnds = tuple(b);

    # Defining constraints for the optimization
    constraint1 = {'type':'eq','fun': constraint,'args':(N_qty_per_bag,N_deficit) };
    constraint2 = {'type':'eq','fun': constraint,'args':(P_qty_per_bag,P_deficit) };
    constraint3 = {'type':'eq','fun': constraint,'args':(K_qty_per_bag,K_deficit) };
    constraint_final = [constraint1, constraint2, constraint3]

    # Derive the solution with SLSQP (Sequential Least SQuare Programming)
    sol = minimize(objective,fertilizer_bag_required,(fertilizer_bag_cost),method='SLSQP',bounds=bnds,constraints=constraint_final)

    # Performing round up for the decimal point
    updated_x = [ (roundup(elem)) for elem in sol.x ]
    ceil_x = np.ceil(updated_x)

    optimized_output = {
    "optimized_N_qty": sum(x*y for x,y in zip(updated_x,N_qty_per_bag)),
    "optimized_P_qty": sum(x*y for x,y in zip(updated_x,P_qty_per_bag)),
    "optimized_K_qty": sum(x*y for x,y in zip(updated_x,K_qty_per_bag)),
    "total_cost": sum(x*y for x,y in zip(ceil_x,fertilizer_bag_cost)),
    "fertilizer_name": fertilizer_name,
    "fertilizer_bag_required": updated_x,
    "fertilizer_bag_cost": fertilizer_bag_cost,
    "fertilizer_bag_weight": fertilizer_bag_weight
    }

    return optimized_output
