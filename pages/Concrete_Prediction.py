import streamlit as st
import pandas as pd
from string import Template
from helper import generator as gen

case = 'Concrete Prediction'

# read data & data wrangling
caps = pd.read_csv('data-input/ml_concrete_pred.csv')
caps_clean = caps.ffill()
caps_topic = caps_clean[['Topic', 'Category']].drop_duplicates()
caps_final = caps_clean.groupby(['Category'], sort=False).max('Max Point').reset_index()

# make a list of unique values of Topic & Category
topic = caps_clean['Topic'].unique()
category = caps_clean['Category'].unique()
# make a dictionary of Topic containing Category
topic_dict = caps_topic.groupby(['Topic'], sort=False)['Category'].apply(list).to_dict()

# initiate empty list & counter
list_df = []
list_editor = []
count = 0

# split caps_clean into smaller dataframes for each Category, and save the dataframes to list_df
for cat in category:
    df = caps_clean.loc[caps_clean['Category'] == cat, ['Subcategory', 'Checks']]
    list_df.append(df)

# title & header
st.title(f"Case: {case}")
st.header('Rubrics Checklist')

# configure reset button
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

st.sidebar.button('Reset', on_click=click_button)

# sequentially shows: Topic, Category, and dataframes (small dataframes made above)
for topic in topic_dict:
    st.subheader(topic)
    for value in topic_dict[topic]:
        st.write(value)

        #convert dataframe to data_editor
        if st.session_state.button:
            caps_editor = st.data_editor(list_df[count], disabled=['Subcategory'], key=f'df_{count}{count}', hide_index=True)
        else:
            caps_editor = st.data_editor(list_df[count], disabled=['Subcategory'], key=f'df_{count}', hide_index=True)
            
        # save all data_editor to list_editor
        list_editor.append(caps_editor)
        # increase count to continue for loop of list_df
        count += 1

# change the content of caps_final based on the data_editors
for i in range(len(list_editor)):
    if list_editor[i]['Checks'].all():
        caps_final.loc[i, 'Checks'] = True
        caps_final.loc[i, 'Earned'] = caps_final.loc[i, 'Max Point']

# total points & total earned
total_points = int(caps_final['Max Point'].sum())
total_earned = int(caps_final['Earned'].sum())

st.divider()
st.header(f"Final Score: {total_earned}/{total_points}")

# shows final dataframe
caps_final

st.divider()
st.header("Feedback")

col1, col2 = st.columns(2)
student = col1.text_input('Input Student Name', placeholder='Student Name')

text_output = ""
count_2 = 0

for topic in topic_dict:
    text_output += topic + '\n'
    for value in topic_dict[topic]:
        earned = int(caps_final.loc[count_2, 'Earned'])
        max_point = int(caps_final.loc[count_2, 'Max Point'])
        icon = '✅' if earned == max_point else '❌'

        text_output += f"- {icon} [{earned}/{max_point}] {value}\n"
        count_2 +=1
    text_output += '\n\n'


feedback = gen.generate_text(student,
                            case,
                            text_output,
                            total_earned)
feedback
# # read text from template.txt
# with open('template.txt', mode='r', encoding='utf-8') as f:
#     content = f.read()
#     temp = Template(content)
#     feedback = temp.substitute(
#         NAME = student,
#         CASE = case,
#         POINTS = text_output,
#         EARNED = total_earned
#         )
