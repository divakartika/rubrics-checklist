import pandas as pd
from helper import template_app as temp_app

# capstone case
case = 'Concrete Prediction'

# read data & data preparation
caps = pd.read_csv('data-input/ml_concrete_pred.csv')

# build app
temp_app.app(case, caps)