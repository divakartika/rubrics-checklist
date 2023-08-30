import pandas as pd
from helper import template_app as temp_app

# capstone case
case = 'Bike Sharing API'

# read data & data preparation
caps = pd.read_csv('data-input/da_bike_sharing_api.csv')

# build app
temp_app.app(case, caps)