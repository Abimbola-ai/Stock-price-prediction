from database.connect import DatabaseError
from flask import Flask, request, render_template, jsonify
import json
from database import db
from src.predict import *



app = Flask(__name__)

def pipeline(ticker, years):
    """Converts user input to appropriate types"""
    ticker = str(ticker)
    years = int(years)
    return ticker, years


def error_check()->str:
    """Checks for errors and outputs a string"""
    if (KeyError, json.JSONDecodeError, AssertionError, ValueError):
        return json.dumps({"error": "Check input"}), 400
    else:
        return json.dumps({"error": "Prediction Failed"}), 500

def clean_final_price(prediction:float)->float:
    """Converts the output from a tuple to a float"""
    price = np.round(prediction, decimals=2)
    string_price = " ".join(map(str, price))
    final_price = float(string_price)
    return final_price

def get_database_data(query, args=(), one=False):
    """Gets data from the postgres database hosted on heroku"""
    cursor = db().connect()
    cursor.execute(query, args)
    r = [dict((cursor.description[i][0], value)\
                    for i, value in enumerate(row)) for row in cursor.fetchall()]
    cursor.close()
    return (r[0] if r else None) if one else r

def insert_data(ticker:str, years: int, final_price:float):
    """Connects to the postgres database and reads database"""
    try:
        cursor = db().connect()
        cursor.execute("INSERT INTO Data (ticker_name, years_analysed, Future_price)\
                VALUES (%s, %s, %s)" ,(ticker, years, final_price))
        cursor.close()
    except DatabaseError:
        raise DatabaseError("Unable to add data")

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
        final_price = clean_final_price(prediction)
        insert_data(ticker, years, final_price)
        return render_template("index.html", prediction_text="{} price tomorrow will be ${:.2f} with a \
             confidence of {}%".format(ticker,final_price, lr_confidence))
    except:
        return error_check()



@app.route('/results', methods = ["POST"])
def results_json():
    """Takes in form data from user and returns future price and accuracy of prediction in json format"""
    data = request.get_json()
    ticker = data[0]
    years = data[1]
    ticker,years = pipeline(ticker, years)
    pred = predict_future_price(ticker,years)
    predicted_price = pred[0]
    final_price = clean_final_price(predicted_price)
    return json.dumps({"Predicted future Price in Dollars":final_price})
    


@app.route('/read_database', methods = ["GET"])
def output():
    """Prints out the first 10 rows in the database"""
    my_query = get_database_data("SELECT * FROM Data LIMIT %s", (10,))
    json_output = json.dumps(my_query, default=str)
    return json_output
    

 
if __name__ == "__main__":
    app.run(debug=True)




