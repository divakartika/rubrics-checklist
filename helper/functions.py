import locale
from string import Template
from datetime import datetime
from datetime import timedelta

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

def data_prep(caps):
    # data wrangling
    caps_clean = caps.ffill()
    caps_topic = caps_clean[['Topic', 'Category']].drop_duplicates()
    caps_final = caps_clean.groupby(['Category'], sort=False).max('Max Point').reset_index()

    # make a list of unique values of Topic & Category
    category = caps_clean['Category'].unique()
    # make a dictionary of Topic containing Category
    topic_dict = caps_topic.groupby(['Topic'], sort=False)['Category'].apply(list).to_dict()

    list_df = []
    # split caps_clean into smaller dataframes for each Category, and save the dataframes to list_df
    for cat in category:
        df = caps_clean.loc[caps_clean['Category'] == cat, ['Subcategory', 'Checks']]
        list_df.append(df)
    
    return caps_final, topic_dict, list_df

# check if score >= 28 (minimum score)
def final_txt(total_earned):
    if total_earned >= 28:
        text = "dan kami ucapkan selamat atas keberhasilannya dalam mengaplikasikan apa yang sudah dipelajari selama di kelas terhadap real-world data. Keep up your good work!"
    else:
        dt = datetime.now() + timedelta(days=7)
        deadline = dt.strftime("%A, %d %B %Y").replace(" 0", " ")
        text = f"Karena total skor Anda kurang dari 28, kami memberikan kesempatan untuk melakukan revisi terhadap capstone project Anda.  Harap mengumpulkan hasil revisi paling lambat pada {deadline}, pukul 23.59 WIB. Kami tunggu hasil revisinya!"
    
    return text
    
def generate_text(case, student, honorific, topic_dict, caps_final, total_earned):
    text_output = ""
    count = 0

    for topic in topic_dict:
        text_output += topic + '  \n'
        for value in topic_dict[topic]:
            earned = int(caps_final.loc[count, 'Earned'])
            max_point = int(caps_final.loc[count, 'Max Point'])
            icon = '✅' if earned == max_point else '❌'

            text_output += f"{icon} [{earned}/{max_point}] {value}  \n"
            count +=1
        text_output += '\n\n'

    # read text from template.txt
    with open('helper/template.txt', mode='r', encoding='utf-8') as f:
        content = f.read()
        temp = Template(content)
        # determine the final text based on score
        final_text = final_txt(total_earned)
        # Subtitute
        feedback = temp.substitute(
            HONORIFIC = honorific,
            NAME = student,
            CASE = case,
            POINTS = text_output,
            EARNED = total_earned,
            FINAL_TEXT = final_text
        )
    
    return feedback