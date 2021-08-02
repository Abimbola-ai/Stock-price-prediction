from database.connect import DatabaseError
from flask import Flask, request, render_template, jsonify
import json
from database import db
from src.predict import *



app = Flask(__name__)


def error_check()->str:
    """Checks for errors and outputs a string"""
    if (KeyError, json.JSONDecodeError, AssertionError, ValueError):
        return json.dumps({"error": "Check input"}), 400
    else:
        return json.dumps({"error": "Prediction Failed"}), 500



@app.route("/")
def home():
    """Renders initial template for the app"""
    return render_template("index.html")

@app.route('/predict', methods = ["POST"])
def predict_output()->str:
    """Takes in form data from user and returns future price and accuracy of prediction"""
    try:
        ticker = request.form.get('Stock Ticker Name')
        years = request.form.get('Number of years', type=int)
        val = predict_future_price(ticker,years)
        prediction = val[0]
        lr_confidence = round(val[1] * 100,2)
        price = np.round(prediction, decimals=2)
        string_price = " ".join(map(str, price))
        final_price = float(string_price)
        return render_template("index.html", prediction_text="{} price tomorrow will be ${:.2f} with a \
             confidence of {}%".format(ticker,final_price, lr_confidence))
    except:
        return error_check()


    

 
if __name__ == "__main__":
    app.run(debug=True)




