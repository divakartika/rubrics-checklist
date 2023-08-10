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

def count_minus_score(is_late):
    minus_score = {'No': False,
                  '1 Day': 1,
                  '2 Day': 3,
                  '3 Day': 5,
                  '4 Day': 7,
                  '> 4 Day': 9
                  }
    # return minus score with late day in bahasa ("2 day" is not grammatically correct tho, it is on purpose for the sake of simplicity)
    return minus_score[is_late], is_late.replace('Day', 'hari')

# check if score >= 28 (minimum score)
def final_txt(total_earned, is_late):
    # get minus skor and late day in bahasa, just changing the day -> hari :(
    minus_score, late_day = count_minus_score(is_late)
    total = total_earned - minus_score
    # template text
    template = {'sukses': "Kami ucapkan selamat atas keberhasilannya dalam mengaplikasikan apa yang sudah dipelajari selama di kelas terhadap real-world data. Keep up your good work!",
                'terlambat': "Karena ada keterlambatan %s dalam pengumpulan maka skor akan dikurangi sebanyak %i poin sehingga skor akhir yang Anda dapatkan adalah %i/36.",
                'revisi': "Karena total skor rubrik Anda kurang dari 28, kami memberikan kesempatan untuk melakukan revisi terhadap capstone project Anda.  Harap mengumpulkan hasil revisi paling lambat pada %s, pukul 23.59 WIB. Kami tunggu hasil revisinya!"}
    # if >= 28 and not late
    if total_earned >= 28:
        text = template['sukses']
        # if >=28 and late
        if minus_score:
            # generate terlambat template and concat with "">= 28 and not late" text
            text = f"{template['terlambat'] % (late_day, minus_score, total)} {text}"
    # if < 28
    else:
        dt = datetime.now() + timedelta(days=7)
        deadline = dt.strftime("%A, %d %B %Y").replace(" 0", " ")
        # generate revisi text from tempalte
        text = template['revisi'] % deadline
        # if < 28 and late
        if minus_score:
            # generate from terlambat template and concat with revisi text
            text = f"{template['terlambat'] % (late_day, minus_score, total)} Dan {text}"
    
    return text
    
def generate_text(case, student, honorific, topic_dict, caps_final, total_earned, is_late):
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
        final_text = final_txt(total_earned, is_late)
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