import sqlite3
import copy
from flask_restful import Resource
from backend.data.database_handler import DatabaseConnection
from backend.queries import api_dropdown_options

class FetchMicronutrientDetail(Resource):

    """

        Endpoint that is called on page load to populate crop/micronutrient details.

    """

    def __init__(self):
        self.micronutrient_json = {};
        self.temp_array = [];


    def get(self):
        # Fetch data from micronutrient_ref_tbl
        sql = api_dropdown_options.select_micronutrient_ref_tbl;
        g = DatabaseConnection().select_table_detail(sql=sql);

        # Convert tuple data from micronutrient_ref_tbl to JSON array micronutrient_dtl_json
        for i in range(len(g)):
            for j in range(5):
                if (j == 0):
                    self.micronutrient_json["crop_name"] = g[i][0];
                if (j == 1):
                    self.micronutrient_json["irrigation_type_code"] = g[i][1];
                if (j == 2):
                    self.micronutrient_json["N_per_hectare"] = g[i][2];
                if (j == 3):
                    self.micronutrient_json["P_per_hectare"] = g[i][3];
                if (j == 4):
                    self.micronutrient_json["K_per_hectare"] = g[i][4];
                j=j+1;

            self.temp_array.append(copy.deepcopy(self.micronutrient_json));
            i=i+1;

        micronutrient_dtl_json = {"micronutrient": copy.copy(self.temp_array)};

        return micronutrient_dtl_json
