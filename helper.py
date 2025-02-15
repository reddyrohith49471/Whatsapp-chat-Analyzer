from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extractor = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]

    num_messages = df.shape[0]
    media_df = df[df['message'] == '<Media omitted>\n']
    media = media_df.shape[0]
    links = []

    words = []
    for message in df['message']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
    return num_messages, len(words),media,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'user':'name','count':'percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'TThis message was deleted']



    wordx = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                wordx.append(word)
    most_common_words_df = pd.DataFrame(Counter(wordx).most_common(20))

    return most_common_words_df


def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([i for i in message if i in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def timeline_helper(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def message_user(selected_user,df):
    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    user_message = df

    return user_message
