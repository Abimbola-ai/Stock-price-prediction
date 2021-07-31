from ml.predict import ticker
from ml.parameters import *

def model_name(ticker:str):
    
    # model name to save, making it as unique as possible based on parameters
    model_name = f"{date_now}_{ticker}-{shuffle_str}-{scale_str}-{split_by_date_str}-\
        {LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
    if BIDIRECTIONAL:
        return str(model_name) + "-b"
    else:
        return model_name