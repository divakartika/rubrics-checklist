import streamlit as st
import pandas as pd
from string import Template

# read data & data wrangling
fnb = pd.read_csv('data-input/ml_fnb.csv')
fnb_clean = fnb.ffill()
fnb_cat = fnb_clean[['Category', 'Major Point']].drop_duplicates()
fnb_major = fnb_clean.groupby(['Major Point'], sort=False).max('Max Point').reset_index()

# make a list of unique values of Category & Major Point
categories = fnb_clean['Category'].unique()
major_points = fnb_clean['Major Point'].unique()
# make a dictionary of Category containing Major Point
cat_dict = fnb_cat.groupby(['Category'], sort=False)['Major Point'].apply(list).to_dict()

# initiate empty list & counter
case = 'FnB Time Series'
list_df = []
list_editor = []
count = 0

# split fnb_clean into smaller dataframes for each Major Point, and save the dataframes to list_df
for major in major_points:
    df = fnb_clean.loc[fnb_clean['Major Point'] == major, ['Subpoints', 'Checks']]
    list_df.append(df)

# title & header
st.title(f"Case: {case}")
st.header('Rubrics Checklist')

# sequentially shows: Category, Major Point, and dataframes (small dataframes made above)
for cat in cat_dict:
    st.subheader(cat)
    for value in cat_dict[cat]:
        st.write(value)
        #convert dataframe to data_editor
        fnb_editor = st.data_editor(list_df[count], key=f'df_{count}')
        # save all data_editor to list_editor
        list_editor.append(fnb_editor)
        # increase count to continue for loop of list_df
        count += 1

# change the content of fnb_major based on the data_editors
for i in range(len(list_editor)):
    if list_editor[i]['Checks'].all():
        fnb_major.loc[i, 'Checks'] = True
        fnb_major.loc[i, 'Earned'] = fnb_major.loc[i, 'Max Point']

# total points & total earned
total_points = int(fnb_major['Max Point'].sum())
total_earned = int(fnb_major['Earned'].sum())

st.divider()
st.header(f"Final Score: {total_earned}/{total_points}")

# shows final dataframe
fnb_major

# TODO: Reset button
# TODO: Text generator

st.divider()
st.header("Feedback")

student = st.text_input('Input Student Name', placeholder='Student Name')

text_output = ""
c = 0

for cat in cat_dict:
    text_output += cat + '\n'
    for value in cat_dict[cat]:
        earned = int(fnb_major.loc[c, 'Earned'])
        max_point = int(fnb_major.loc[c, 'Max Point'])
        icon = '✅' if earned == max_point else '❌'
        
        text_output += f"- {icon} [{earned}/{max_point}] {value}\n"
        c +=1
    text_output += '\n\n'

# read text from folder template_text, file example.txt
with open('template.txt', mode='r', encoding='utf-8') as f:
    content = f.read()
    temp = Template(content)
    feedback = temp.substitute(
        NAME = student,
        CASE = case,
        POINTS = text_output,
        EARNED = total_earned
        )

feedback