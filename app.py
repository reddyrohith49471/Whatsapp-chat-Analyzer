import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("show Analysis wrt",user_list)

    st.title("Selected user Messages")
    user_message = helper.message_user(selected_user,df)
    st.dataframe(user_message)

    if st.sidebar.button("Show Analysis"):

        num_messages, words,media,links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media)
        with col4:
            st.header("Links Shared")
            st.title(links)

    if selected_user == 'Overall':
        st.title("Most Busy Users")
        x,new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    st.title("Word Cloud")
    df_wc = helper.create_wordcloud(selected_user, df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    st.title("Most Common Words")

    most_common_words_df = helper.most_common_words(selected_user, df)
    fig,ax = plt.subplots()
    ax.barh(most_common_words_df[0],most_common_words_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    emoji_df = helper.emoji_helper(selected_user, df)
    st.title("Most Emoji Used")
    col1,col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)

    st.title("Monthly Time")
    timeline = helper.timeline_helper(selected_user, df)
    fig,ax = plt.subplots()
    ax.bar(timeline['time'],timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    st.title("Weekly Time")
    col1,col2 = st.columns(2)
    with col1:
        st.header("Most Busy Day")
        busy_day = helper.week_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        st.pyplot(fig)
    with col2:
        st.header("Most Busy Month")
        busy_month = helper.monthly_activity_map(selected_user, df)
        fig,ax = plt.subplots()
        ax.bar(busy_month.index,busy_month.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Heat Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)