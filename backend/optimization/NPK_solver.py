import numpy as np
from scipy.optimize import minimize
import math

def find_max(NPK_required,N_required,P_required,K_required):
    for i in range(0,len(N_required)):
        NPK_required[i] = (max(N_required[i],P_required[i],K_required[i]))
        g = math.modf(NPK_required[i])
        if g[0] >= 0.6:
            NPK_required[i] = math.ceil(NPK_required[i])
        elif g[0] <= 0.5:
            NPK_required[i] = math.floor(NPK_required[i])

    return NPK_required

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

def objective(fertilizer_bag_cost,N_required):
  return (sum(x*y for x,y in zip(fertilizer_bag_cost,N_required)))

def constraint(N_required,N_qty_per_bag,N_deficit):
  return (sum(x*y for x,y in zip(N_required,N_qty_per_bag)) - N_deficit)

def roundup(x):
    return round(int(math.ceil(x / 0.05)) * 0.05,1)

def single_optimize_minimize(NPK_deficit,fertilizer_bag_required,fertilizer_bag_cost,fertilizer_name,NPK_qty_per_bag):

    #boundary logic
    b = []

    for i in range(len(fertilizer_name)):
        indiv_bound = []
        # Defining lower boundary as 0
        indiv_bound.append(0) # Lower boundary
        # Boundary for fertilizer type
        if NPK_qty_per_bag[i] == 0:
            npk_bound = 0
        else:
            npk_bound = (math.floor(NPK_deficit/NPK_qty_per_bag[i]))
        # Defining Upper boundary
        indiv_bound.append(npk_bound)
        b.append(tuple(indiv_bound))

    bnds = tuple(b)

    cons = {'type':'eq','fun': constraint,'args':(NPK_qty_per_bag,NPK_deficit) }

    sol = minimize(objective,fertilizer_bag_required,(fertilizer_bag_cost),method='SLSQP',bounds=bnds,constraints=cons)

    return sol.x

def optimize_minimize(N_deficit,P_deficit,K_deficit,fertilizer_bag_required,fertilizer_bag_cost,fertilizer_name,N_qty_per_bag, P_qty_per_bag,K_qty_per_bag,fertilizer_bag_weight):

    N_qty_per_bag = nitrogen_fert_filter(fertilizer_name,N_qty_per_bag,fertilizer_bag_cost);

    N_required = np.zeros(len(fertilizer_name))
    P_required = np.zeros(len(fertilizer_name))
    K_required = np.zeros(len(fertilizer_name))
    NPK_required = np.zeros(len(fertilizer_name))

    N_required = single_optimize_minimize(N_deficit,N_required,fertilizer_bag_cost,fertilizer_name,N_qty_per_bag);
    P_required = single_optimize_minimize(P_deficit,P_required,fertilizer_bag_cost,fertilizer_name,P_qty_per_bag);
    K_required = single_optimize_minimize(K_deficit,K_required,fertilizer_bag_cost,fertilizer_name,K_qty_per_bag);

    NPK_required = find_max(NPK_required,N_required,P_required,K_required)

    updated_x = [ (roundup(elem)) for elem in NPK_required ]

    optimized_output = {
    "optimized_N_qty": sum(x*y for x,y in zip(updated_x,N_qty_per_bag)),
    "optimized_P_qty": sum(x*y for x,y in zip(updated_x,P_qty_per_bag)),
    "optimized_K_qty": sum(x*y for x,y in zip(updated_x,K_qty_per_bag)),
    "total_cost": sum(x*y for x,y in zip(updated_x,fertilizer_bag_cost)),
    "fertilizer_name": fertilizer_name,
    "fertilizer_bag_required": updated_x,
    "fertilizer_bag_cost": fertilizer_bag_cost,
    "fertilizer_bag_weight": fertilizer_bag_weight
    }

    print(optimized_output)

    return optimized_output
