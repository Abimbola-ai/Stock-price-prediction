# Daily Stock Price Prediction
The project is carried out to fulfill the following requirements:

* Create an API using Flask
* Save and load trained models 
* Store inputs and output in Heroku postgres database
* Create inference pipeline for the trained model
* Deploy the Flask application using Heroku

### Features of the dataset:
#### Application Input
* TICKER: Name of the stock price you want to predict
* YEARS: Number of years of data to be used for analysis 

#### Application Output
* PRICE: Next day price of the stock
* CONFIDENCE: Accuracy of the model

You can use the app by clicking on the url below:

https://daily-stock-price-prediction.herokuapp.com/


### For further development:

```
pip install requirements.txt
```

### Below is an example on how to make a price request on 2 inputs:
```
import requests
import json

url = 'http://127.0.0.1:5000/results'
data = ["TSLA",5]
j_data= json.dumps(data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r,r.text)

```
Prints out:
```
 {"Predicted future Price in Dollars": 717.73}
```