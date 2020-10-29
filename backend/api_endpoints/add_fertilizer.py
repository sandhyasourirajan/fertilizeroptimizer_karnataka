import sqlite3;
from flask_restful import Resource;
from webargs import fields;
from webargs.flaskparser import use_args;
from backend.data.database_handler import DatabaseConnection;
from backend.queries import insert_fertilizer;

class AddFertilizer(Resource):

    """

        Endpoint that is called to add a new fertilizer to the DB

    """

    input_args = {
    'fertilizer_name':fields.Str(required=True),
    'cost_per_kg':fields.Float(required=True),
    'unit_in_kg':fields.Float(required=True),
    'n_per_unit':fields.Int(required=True),
    'p_per_unit':fields.Int(required=True),
    'k_per_unit':fields.Int(required=True),
    's_per_unit':fields.Int(),
    }

    @use_args(input_args)

    def __init__(self,args):

        ###################### Inputs from API ######################

        self.fertilizer_name = args["fertilizer_name"];
        self.cost_per_kg = args["cost_per_kg"];
        self.unit_in_kg = args["unit_in_kg"]
        self.n_per_unit = args["n_per_unit"]
        self.p_per_unit = args["p_per_unit"]
        self.k_per_unit = args["k_per_unit"]
        self.s_per_unit = args["s_per_unit"]

        #############################################################
        self.bag_cost = 0
        self.input_list = []

    def post(self):

        # Insert a new fertilizer into the fertilizer_ref_tbl

        self.bag_cost = self.cost_per_kg * self.unit_in_kg;

        if (self.s_per_unit is None):
            self.s_per_unit = 0

        self.input_list = [self.fertilizer_name, self.cost_per_kg, self.unit_in_kg,self.bag_cost,
                            self.n_per_unit,self.p_per_unit,self.k_per_unit,self.s_per_unit]

        input_parm = tuple(self.input_list)

        sql = insert_fertilizer.insert_fertilizer_ref_tbl

        message = DatabaseConnection().insert_table_detail(sql,input_parm)

        return message
