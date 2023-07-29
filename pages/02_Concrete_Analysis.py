import streamlit as st
import pandas as pd
from string import Template
from helper import functions as func
from helper import template_app as temp_app

# capstone case
case = 'Concrete Analysis'

# read data & data preparation
caps = pd.read_csv('data-input/ml_concrete_analysis.csv')

# build app
temp_app.app(case, caps)