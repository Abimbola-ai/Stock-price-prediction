from types import MethodDescriptorType
from database.connect import DatabaseError
from flask import Flask, request, render_template
from ml.parameters import *
from ml.train import *
from ml.test import *
from ml.stock_prediction import create_model, load_data, model_name
from tensorflow.keras.layers import LSTM
import os
import json
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from database import db
import numpy
from psycopg2.extensions import register_adapter, AsIs


cursor = db().connect()

app = Flask(__name__)

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)
register_adapter(numpy.float32, addapt_numpy_float32)

def pred(ticker:str, years:int):
    #train_data(ticker,years)
    test(ticker,years)
    data = load_data(ticker, years, N_STEPS, scale=SCALE, split_by_date=SPLIT_BY_DATE, 
                shuffle=SHUFFLE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, 
                feature_columns=FEATURE_COLUMNS)
    model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                    dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)
    name = model_name(ticker)
    model_path = os.path.join("results", name) + ".h5"
    model.load_weights(model_path)
    #final_df = get_final_df(model, data)
    #plot_graph(final_df)
    future_price = predict(model, data)
    return future_price 

def error_check()->str:
    """Checks for errors and outputs a string"""
    if (KeyError, json.JSONDecodeError, AssertionError, ValueError):
        return json.dumps({"error": "Check input"}), 400
    else:
        return json.dumps({"error": "Prediction Failed"}), 500

def process_input(request_data:str) -> np.array:
    """Takes in the input data and converts it to an array
    that the model can understand"""
    parsed_body = np.asarray(json.loads(request_data)["inputs"])
    assert len(parsed_body.shape) == 2, "'Input must be a 2-D array"
    return parsed_body

def get_database_data(query, args=(), one=False):
        cursor.execute(query, args)
        r = [dict((cursor.description[i][0], value)\
                    for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.close()
        return (r[0] if r else None) if one else r

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods = ["POST"])
def predict_output():
    try:
        ticker = request.form.get('Stock Ticker Name')
        years = request.form.get('Number of years', type=int)
        prediction= pred(ticker,years)
        cursor.execute("INSERT INTO Data (ticker_name, years_analysed, Future_price)\
            VALUES (%s, %s, %s)" ,(ticker,years, prediction))
        print("Record added successfully")
        return render_template("index.html", prediction_text="Future price after {} days is ${:.2f}".format(LOOKUP_STEP,prediction))
    except:
        return error_check()


@app.route('/results', methods = ["POST"])
def results_json():
    if request.method == "POST": 
        input_params = process_input(request.data)
        ticker = input_params[0]
        years = input_params[1]
        output = pred(ticker,years)
        return json.dumps({f"Future price after {LOOKUP_STEP} days is $": output.tolist()})

@app.route('/read_database', methods = ["GET"])
def output():
    my_query = get_database_data("SELECT * FROM Data LIMIT %s", (10,))
    json_output = json.dumps(my_query, default=str)
    return json_output
    

 
if __name__ == "__main__":
    app.run(debug=True)




