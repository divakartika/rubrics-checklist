import pandas as pd
from helper import template_app as temp_app

# capstone case
case = 'Telegram Chatbot'

# read data & data preparation
caps = pd.read_csv('data-input/da_telebot.csv')

# build app
temp_app.app(case, caps)