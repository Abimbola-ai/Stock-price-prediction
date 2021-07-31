from types import MethodDescriptorType
from database.connect import DatabaseError
from flask import Flask, request, render_template
from tensorflow.keras.layers import LSTM
import json
from database import db
import numpy
from psycopg2.extensions import register_adapter, AsIs
from src.predict import *

cursor = db().connect()

app = Flask(__name__)


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
        years= request.form.get('Number of years', type=int)
        val= predict_future_price(ticker,years)
        prediction = val[0]
        lr_confidence = round(val[1] * 100,2)
        price = np.round(prediction, decimals=2)
        string_price = " ".join(map(str, price))
        final_price = float(string_price)
        try:
            cursor.execute("INSERT INTO Data (ticker_name, years_analysed, Future_price)\
                VALUES (%s, %s, %s)" ,(ticker, years, final_price))
        except DatabaseError:
            raise DatabaseError("Unable to add data")
        
        return render_template("index.html", prediction_text="{} price tomorrow will be ${:.2f} with a \
             confidence of {}%".format(ticker,final_price, lr_confidence))
    except:
        return error_check()


@app.route('/results', methods = ["POST"])
def results_json():
    if request.method == "POST": 
        input_params = process_input(request.data)
        ticker = input_params[0]
        years = input_params[1]
        output = predict_future_price(ticker,years)
        return json.dumps({f"{ticker} price tomorrow will be $": output.tolist()})

@app.route('/read_database', methods = ["GET"])
def output():
    my_query = get_database_data("SELECT * FROM Data LIMIT %s", (10,))
    json_output = json.dumps(my_query, default=str)
    return json_output
    

 
if __name__ == "__main__":
    app.run(debug=True)




