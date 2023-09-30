import pandas as pd
from helper import dv_app as temp_app

# capstone case
case = 'Shiny Dashboard'

# read data & data preparation
caps = pd.read_csv('data-input/dv_shiny.csv')

# build app
temp_app.app(case, caps)