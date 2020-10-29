from webargs import fields
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_restful import Api
from backend.api_endpoints.select_micronutrient import FetchMicronutrientDetail
from backend.api_endpoints.select_fertilizer import FetchFertilizerDetail
from backend.api_endpoints.fertilizer_optimizer import FertilizerOptimizer
from backend.api_endpoints.add_fertilizer import AddFertilizer

# from backend.api_endpoints.select
#from backend.config.production_web_server import StandaloneApplication
#from flask_compress import Compress

import multiprocessing


def number_of_workers():

    """
        Number of threads = CPU cores + 1
        :return:
    """

    return (multiprocessing.cpu_count() * 2) + 1


app = Flask(__name__)

#Compress(app)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# =================================
#  Set up the routing here
# =================================

api.add_resource(FetchMicronutrientDetail, '/micronutrient')
api.add_resource(FetchFertilizerDetail, '/fertilizer')
api.add_resource(FertilizerOptimizer, '/optimize')
api.add_resource(AddFertilizer, '/addfertilizer')

# ====================================================================================================
#  Catch All, wild-card. For any unknown URL, just route it to Vue.JS and let it handle the 404 error
# ====================================================================================================


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

# =================================
#  Initialize the flask app.
#  1) Set the gunicorn options
#  2) Start the web-server
# =================================


if __name__ == "__main__":

    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8000'),
        'workers': number_of_workers(),
    }

    #StandaloneApplication(app, options).run()  # -- Production server (multi threaded)
    app.run(host="0.0.0.0", debug=True, threaded=True, port=8000) # -- Dev server
