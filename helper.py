from urlextract import URLExtract
extractor = URLExtract()
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji


def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]


    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    #fetch number of media messages
    num_media_message = df[df['message'] == '<Media omitted>\n'].shape[0]

    #fetch numbers of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_messages, len(words), num_media_message, len(links)

def most_busy_user(df):
    new_df = round((df['user'].value_counts().head() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return df['user'].value_counts().head(), new_df


def create_wordcloud(selected_user, df):

    if selected_user!='Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate((df['message'].str.cat(sep=" ")))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group_notification message
    temp = df[df['message'] != 'group_notification']

    # remove media omitted messages
    temp = temp[temp['message'] != '<Media omitted>\n']

    # remove stop words
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()


    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    return_df = pd.DataFrame(Counter(words).most_common(20))

    return return_df

def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])


    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return  emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):

        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


