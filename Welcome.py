import locale
import streamlit as st

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

# page configuration
st.set_page_config(
    page_title="Rubrics Checklist",
    page_icon="https://algorit.ma/wp-content/uploads/2023/04/Algoritma-Logo.png",
)

# get text from README.md
with open('README.md', mode='r', encoding='utf-8') as f:
    next(f) # skip the first line (a streamlit badge icon)
    content = f.read()

content

# close the file
f.close()