from parameters import *
from train import *
from test import *
from stock_prediction import create_model, load_data, model_name
from tensorflow.keras.layers import LSTM
import os
import pandas as pd




# ticker = "SPCE"
# years = int(2)
#name = model_name(ticker)
#print(name)
#train_data(ticker,years)

def pred(ticker, years):
    train_data(ticker,years)

    data = load_data(ticker, years, N_STEPS, scale=SCALE, split_by_date=SPLIT_BY_DATE, 
                shuffle=SHUFFLE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE, 
                feature_columns=FEATURE_COLUMNS)

# construct the model
    model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                    dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)

# load optimal model weights from results folder
    name = model_name(ticker)
    model_path = os.path.join("results", name) + ".h5"
    model.load_weights(model_path)

# evaluate the model
    loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)
# calculate the mean absolute error (inverse scaling)
    if SCALE:
        mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform([[mae]])[0][0]
    else:
        mean_absolute_error = mae

# get the final dataframe for the testing set
    final_df = get_final_df(model, data)
# predict the future price
    future_price = predict(model, data)
# we calculate the accuracy by counting the number of positive profits
    accuracy_score = (len(final_df[final_df['sell_profit'] > 0]) + len(final_df[final_df['buy_profit'] > 0])) / len(final_df)
# calculating total buy & sell profit
    total_buy_profit  = final_df["buy_profit"].sum()
    total_sell_profit = final_df["sell_profit"].sum()
# total profit by adding sell & buy together
    total_profit = total_buy_profit + total_sell_profit
# dividing total profit by number of testing samples (number of trades)
    profit_per_trade = total_profit / len(final_df)
# printing metrics
    return future_price#
#print(f"Future price after {LOOKUP_STEP} days is ${future_price:.2f}")




# print(f"{LOSS} loss:", loss)
# print("Mean Absolute Error:", mean_absolute_error)
# print("Accuracy score:", accuracy_score)
# print("Total buy profit:", total_buy_profit)
# print("Total sell profit:", total_sell_profit)
# print("Total profit:", total_profit)
# print("Profit per trade:", profit_per_trade)
# plot true/pred prices graph
    #plot_graph(final_df)
# data_final = final_df.tail(10)
# print(data_final)
# # save the final dataframe to csv-results folder
# # csv_results_folder = "csv-results"
# # if not os.path.isdir(csv_results_folder):
# #     os.mkdir(csv_results_folder)
# # csv_filename = os.path.join(csv_results_folder, name + ".csv")
# #data_final2 = final_df.iloc[[0:10]]
# #print(data_final2)
# final_df.tail(10).to_csv(f"{ticker}_predict.csv")
# print(final_df)
if __name__=="__main__":
    x = pred("FB", 2)
    print(x)