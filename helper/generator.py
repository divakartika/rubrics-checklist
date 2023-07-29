# import streamlit as st
from datetime import datetime
from datetime import timedelta
import locale
import pandas as pd
from string import Template

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# cek
def final_txt(total_earned):
    if total_earned >= 28:
        text = "dan kami ucapkan selamat atas keberhasilannya dalam mengaplikasikan apa yang sudah dipelajari selama di kelas terhadap real-world data. Keep up your good work!"
    else:
        dt = datetime.now() + timedelta(days=7)
        deadline = dt.strftime("%A, %d %B %Y").replace(" 0", " ")
        text = f"Karena total skor Anda kurang dari 28, kami memberikan kesempatan untuk melakukan revisi terhadap capstone project Anda.  Harap mengumpulkan hasil revisi paling lambat pada {deadline}, pukul 23.59 WIB. Kami tunggu hasil revisinya!"
    
    return text
    
def generate_text(student, case, text_output, total_earned):
    # read text from template.txt
    with open('helper/template.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        temp = Template(content)
        # determine the final text based on score
        final_text = final_txt(total_earned)
        # Subtitute
        feedback = temp.substitute(
            NAME = student,
            CASE = case,
            POINTS = text_output,
            EARNED = total_earned,
            FINAL_TEXT = final_text
        )
    
    return feedback