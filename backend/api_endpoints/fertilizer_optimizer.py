import sqlite3;
import copy;
import numpy as np;
from flask_restful import Resource;
from webargs import fields;
from webargs.flaskparser import use_args;
from backend.data.database_handler import DatabaseConnection;
from backend.queries import api_dropdown_options;
from backend.optimization import single_solver,NPK_solver;

class FertilizerOptimizer(Resource):

    """

        Endpoint that is called after deficit N,P,K calculation to suggest fertilizer based on N,P,K

    """

    input_args = {
    'opts':fields.Str(required=True),
    'N_deficit':fields.Int(required=True),
    'P_deficit':fields.Int(required=True),
    'K_deficit':fields.Int(required=True),
    'fertilizer_name':fields.List(fields.Str(),required=True),
    'fertilizer_bag_cost':fields.List(fields.Float(),required=True)
    }

    @use_args(input_args)

    def __init__(self,args):

        self.fertilizer_json = {};
        self.npk_json = {};
        self.temp_array = [];

        ###################### Inputs from API ######################

        self.input1 = args["fertilizer_name"];
        self.input2 = args["fertilizer_bag_cost"];
        self.opts = args["opts"]

        #optimizer variables - constraint for N,P,K calculation
        self.N_deficit = args["N_deficit"];
        self.P_deficit = args["P_deficit"];
        self.K_deficit = args["K_deficit"];
        #############################################################

        #N,p,K composition for each fertilizer
        self.N_qty_per_bag = [];
        self.P_qty_per_bag = [];
        self.K_qty_per_bag = [];
        self.fertilizer_name = [];
        self.fertilizer_bag_cost = [];
        self.fertilizer_bag_weight = [];

    def post(self):

        # perform sort of fertilizer_name & bag_cost in ascending order to match the sql output as bag cost will come from UI and NPK quantities and fertilier name will come from DB
        self.temp_array = []

        self.fertilizer_bag_cost = [x for _,x in sorted(zip(self.input1,self.input2))]
        self.fertilizer_name = sorted(self.input1)

        fertilizer_name_list = []

        sql = api_dropdown_options.select_fertilizer_ref_tbl_npk.format(str(tuple(self.fertilizer_name)))
        npk_output = DatabaseConnection().select_table_detail(sql)

        for i in range(len(npk_output)):
            for j in range(5):

                if (j == 0):
                    self.N_qty_per_bag.append(npk_output[i][0])

                if (j == 1):
                    self.P_qty_per_bag.append(npk_output[i][1])

                if (j == 2):
                    self.K_qty_per_bag.append(npk_output[i][2])
                if (j == 3):
                    fertilizer_name_list.append(npk_output[i][3])
                if (j == 4):
                    self.fertilizer_bag_weight.append(npk_output[i][4])
                j=j+1;

            i=i+1;

        order = len(self.fertilizer_name)

        fertilizer_bag_required = np.zeros(order)

        if self.opts == 'single':
            #Optimized result - Single solver
            optimized_output = single_solver.optimize_minimize(self.N_deficit,self.P_deficit,self.K_deficit,fertilizer_bag_required,self.fertilizer_bag_cost,self.fertilizer_name,self.N_qty_per_bag, self.P_qty_per_bag, self.K_qty_per_bag,self.fertilizer_bag_weight)
            final_output = {"optimized_output": optimized_output}
        else:
            #Optimized result - Seperate solver for N,P & K
            optimized_output = NPK_solver.optimize_minimize(self.N_deficit,self.P_deficit,self.K_deficit,fertilizer_bag_required,self.fertilizer_bag_cost,self.fertilizer_name,self.N_qty_per_bag, self.P_qty_per_bag, self.K_qty_per_bag,self.fertilizer_bag_weight)
            final_output = {"optimized_output": optimized_output}

        return final_output
