# import streamlit as st
import pandas as pd
from string import Template

def generate_text(student, case, text_output, total_earned):
    # read text from template.txt
    with open('template.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        temp = Template(content)
        feedback = temp.substitute(
            NAME = student,
            CASE = case,
            POINTS = text_output,
            EARNED = total_earned
        )
    
    return feedback