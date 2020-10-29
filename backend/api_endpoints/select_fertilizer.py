import sqlite3
import copy
from flask_restful import Resource
from backend.data.database_handler import DatabaseConnection
from backend.queries import api_dropdown_options

class FetchFertilizerDetail(Resource):

    """

        Endpoint that is called after deficit N,P,K calculation to suggest fertilizer based on N,P,K

    """

    def __init__(self):
        self.fertilizer_json = {};
        self.temp_array = [];

    def get(self):
        # Fetch data from micronutrient_ref_tbl
        sql = api_dropdown_options.select_fertilizer_ref_tbl;
        g = DatabaseConnection().select_table_detail(sql=sql);

        # Convert tuple data from fertilizer_ref_tbl to JSON array fertilizer_dtl_json
        for i in range(len(g)):
            for j in range(4):
                if (j == 0):
                    self.fertilizer_json["fertilizer_name"] = g[i][0]
                # if (j == 1):
                #     self.fertilizer_json["cost_per_kg"] = g[i][1]
                if (j == 2):
                    self.fertilizer_json["unit_in_kg"] = g[i][2]
                if (j == 3):
                    self.fertilizer_json["bag_cost"] = g[i][3]
                j=j+1;

            self.temp_array.append(copy.deepcopy(self.fertilizer_json))
            i=i+1;

        fertilizer_dtl_json = {"fertilizer": copy.copy(self.temp_array)}
        return fertilizer_dtl_json
