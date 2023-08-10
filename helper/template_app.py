import streamlit as st
from helper import functions as func

def app(case, caps):
    caps_final, topic_dict, list_df = func.data_prep(caps)

    # initiate empty list & counter
    list_editor = []
    count = 0

    # title & header
    st.title(f"Case: {case}")
    st.header('Rubrics Checklist')

    # configure reset button
    if 'button' not in st.session_state:
        st.session_state.button = False

    def click_button():
        st.session_state.button = not st.session_state.button

    st.sidebar.write('Click this button to Reset!')
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
    st.dataframe(caps_final)

    st.divider()
    st.header("Feedback")

    col1, col2, col3 = st.columns(3)
    student = col1.text_input('Input Student Name', placeholder='Student Name')
    honorific = col2.selectbox('Choose Honorific', ['Bapak', 'Ibu', 'Mas', 'Mbak', 'Kak'])
    is_late = col3.selectbox('Is Late?', ['No', '1 Day', '2 Day', '3 Day', '4 Day', '> 4 Day'])

    # generate feedback
    feedback = func.generate_text(case, student, honorific, topic_dict, caps_final, total_earned, is_late)
    st.write(feedback)

    # warning box
    st.warning("""To paste the text in Google Classroom, use **`CTRL+SHIFT+V`**
               
               \nUnless you want to make your text looks like a mess, don't use `CTRL+V` 
               because this Streamlit uses Markdown formatting and Google Classroom uses Rich Text Formatting""")