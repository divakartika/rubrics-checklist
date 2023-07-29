import pandas as pd
from helper import template_app as temp_app

# capstone case
case = 'Where were You'

# read data & data preparation
caps = pd.read_csv('data-input/ml_wwy.csv')

# build app
temp_app.app(case, caps)