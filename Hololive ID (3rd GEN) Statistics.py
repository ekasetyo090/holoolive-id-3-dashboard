import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import re
from googleapiclient.discovery import build

api_key = "AIzaSyB3o1aYtHuqAioKQ_WAW4qGrVegolHtAJw"
youtube = build("youtube", "v3", developerKey = api_key)
channel_ids = ['UCjLEmnpCNeisMxy134KPwWw', 'UCTvHWSfBZgtxE4sILOaurIQ', 'UCZLZ8Jjx_RN2CXloOmgTHVg']

#-----------------------------------------
def convert_duration(duration_str):
    # Mencocokkan pola string durasi dengan ekspresi reguler
    pattern = r'P(\d+D)?T(\d+H)?(\d+M)?(\d+S)?'
    matches = re.findall(pattern, duration_str)

    # Menginisialisasi variabel untuk setiap bagian durasi
    days = hours = minutes = seconds = 0

    # Mengekstrak nilai-nilai dari string yang cocok dengan pola
    for match in matches:
        for part in match:
            if part:
                value = int(part[:-1])  # Mengambil angka dari potongan string
                if part[-1] == 'D':
                    days = value
                elif part[-1] == 'H':
                    hours = value
                elif part[-1] == 'M':
                    minutes = value
                elif part[-1] == 'S':
                    seconds = value

    # Menghitung total durasi dalam detik
    total_seconds = (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds
    return total_seconds

#-----------------------------------------
def get_channel_list_stats(youtube, channel_ids):
    request = youtube.channels().list(part="snippet,contentDetails,statistics,topicDetails,id",id=','.join(channel_ids))
    response = request.execute()
    data_channel = []    
    for i in range(len(response["items"])):
        data_dicts = dict(
            channel_name = response["items"][i]["snippet"].get('title'),
            total_views = response["items"][i]["statistics"].get("viewCount"),
            total_subs = response["items"][i]["statistics"].get("subscriberCount"),
            total_videos = response["items"][i]["statistics"].get('videoCount'),
            topics = response["items"][i]['topicDetails'].get('topicCategories'),
            channel_id = response["items"][i].get('id'),
            playlist_id = response["items"][i]["contentDetails"]["relatedPlaylists"].get("uploads")
            )   
        data_channel.append(data_dicts)
        
    temp_df = pd.DataFrame(data_channel)
    temp_df["total_views"] = pd.to_numeric(temp_df["total_views"])
    temp_df["total_subs"] = pd.to_numeric(temp_df["total_subs"])    
    temp_df["total_videos"] = pd.to_numeric(temp_df["total_videos"])
    temp_df['Average_views_per_videos'] = temp_df["total_views"] / temp_df["total_videos"]
    return temp_df

#-----------------------------------------
def get_video_id_from_playlist_id(youtube, dict_ch_playlist):
        temp_list = []
        request = youtube.playlistItems().list(part="contentDetails,id,snippet,status",
                                               playlistId=dict_ch_playlist,
                                               maxResults=50)
        response = request.execute()

        for i in range(len(response["items"])):
            video_Id = response["items"][i]["contentDetails"]["videoId"]
            temp_list.append(video_Id)
        more_pages = True
        next_pages_token = response.get("nextPageToken")
        while more_pages:
            if next_pages_token is None:
                more_pages = False
            else:
                request = youtube.playlistItems().list(part="contentDetails,id,snippet,status",
                                                       playlistId=dict_ch_playlist,
                                                       pageToken=next_pages_token,
                                                       maxResults=50)
                response = request.execute()
                for i in range(len(response["items"])):
                    video_Id = response["items"][i]["contentDetails"]["videoId"]
                    temp_list.append(video_Id)
                next_pages_token = response.get("nextPageToken")
        return temp_list


#-----------------------------------------
def get_video_detail(youtube, video_ids):
    temp_list = []
    for u in range(0,len(video_ids),50):
        request = youtube.videos().list(part="snippet,contentDetails,statistics",
                                        id=','.join(video_ids[u:u+50]))
        response = request.execute()
        for i in range(len(response["items"])):
            video_url = 'https://www.youtube.com/watch?v='+ response["items"][i].get("id")
            dict_data = dict(date = response["items"][i]["snippet"].get("publishedAt"),
                             views = response["items"][i]["statistics"].get("viewCount"),
                             likes= response["items"][i]["statistics"].get("likeCount"),
                             comments = response["items"][i]["statistics"].get("commentCount"),
                             favorites = response["items"][i]["statistics"].get("favoriteCount"),
                             duration =  response["items"][i]["contentDetails"].get('duration'),
                             video_url = video_url,
                             video_tag = response["items"][i]["snippet"].get("tags"),
                             thumbnail = response["items"][i]["snippet"]["thumbnails"]["medium"].get("url"),            
                        )
            temp_list.append(dict_data)
    temp_df = pd.DataFrame(temp_list)
    temp_df['duration'] = temp_df['duration'].apply(convert_duration)
    temp_df['duration'] = pd.to_numeric(temp_df['duration'])
    temp_df['tag_used'] = ['Yes' if x is not None else 'No' for x in temp_df['video_tag']]
    temp_df['date'] = pd.to_datetime(temp_df['date'])
    temp_df["views"] = pd.to_numeric(temp_df["views"])
    temp_df["likes"] = pd.to_numeric(temp_df["likes"])    
    temp_df["comments"] = pd.to_numeric(temp_df["comments"])
    temp_df["favorites"] = pd.to_numeric(temp_df["favorites"])
    temp_df = temp_df.sort_values(by='date',ascending=True).reset_index(drop=True)    
    return temp_df

#-----------------------------------------
all_channel_stats = get_channel_list_stats(youtube, channel_ids)
dicts_playlist = {}
for i in (range(len(all_channel_stats))):
    dicts_playlist[all_channel_stats.iloc[i,0]] = all_channel_stats.iloc[i,6]



video_id_kaela = get_video_id_from_playlist_id(youtube, dicts_playlist.get('Kaela Kovalskia Ch. hololive-ID'))
video_id_zeta = get_video_id_from_playlist_id(youtube, dicts_playlist.get('Vestia Zeta Ch. hololive-ID'))
video_id_kobo = get_video_id_from_playlist_id(youtube, dicts_playlist.get('Kobo Kanaeru Ch. hololive-ID'))

df_kaela = get_video_detail(youtube, video_ids=video_id_kaela)
df_zeta = get_video_detail(youtube, video_ids=video_id_zeta)
df_kobo = get_video_detail(youtube, video_ids=video_id_kobo)

st.session_state['df_kaela_st'] = df_kaela
st.session_state['df_zeta_st'] = df_zeta
st.session_state['df_kobo_st'] = df_kobo
#-----------------------------------------

st.set_page_config(
    page_title='Hololive ID 3rd Generation')

    
#st.sidebar.success('Pages Load Successfully')
st.image("https://hololive.hololivepro.com/wp-content/uploads/2022/03/holoID3gen_Press_W1920H1080-1-1440x810.png")
st.header('Hololive ID(3rd GEN) Statistics')

tab1, tab2 = st.tabs(["Overaall Statistics", "Comparison"])
#-----------------------------------------
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        #-------------------------------------------------------
        #sst.dataframe(all_channel_stats)
        st.subheader('Total Subscriber')
        fig = plt.figure(figsize=(6,4))
        ax = sns.barplot(data=all_channel_stats,x='channel_name', y='total_subs')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Channel Name")
        plt.ylabel("Total Subscribers")
        plt.title("Total Subscriber For YouTube Channel")
        st.pyplot(fig)
        
        #-------------------------------------------------------
        st.subheader('Total Views')
        fig = plt.figure(figsize=(7,4))
        ax = sns.barplot(data=all_channel_stats,x='channel_name', y='total_views')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Channel Name")
        plt.ylabel("Total Views")
        plt.title("Total Views For Each YouTube Channel")
        st.pyplot(fig)
        #-------------------------------------------------------

    with col2:
        #-------------------------------------------------------
        st.subheader('Total Videos')
        fig = plt.figure(figsize=(7,4))
        ax = sns.barplot(data=all_channel_stats,x='channel_name', y='total_videos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Channel Name")
        plt.ylabel("Total Videos")
        plt.title("Total Videos For Each YouTube Channel")
        st.pyplot(fig)
        #-------------------------------------------------------
        st.subheader('Average (Views/Videos)')

        fig = plt.figure(figsize=(7,4))
        ax = sns.barplot(data=all_channel_stats,x='channel_name', y='Average_views_per_videos')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Channel Name")
        plt.ylabel("Views/Videos")
        plt.title("(Views/Videos) For Each YouTube Channel")
        st.pyplot(fig)

#-----------------------------------------        
with tab2:
    col1, col2 = st.columns(2)
    n_num = 30
    with col1:
        #-------------------------------------------------------  
        st.subheader('Views')
        fig = plt.figure(figsize=(7,4))
        sns.lineplot(data=st.session_state.df_kaela_st[-n_num:],x=list(range(n_num)), y='views',color='red',label='Kaela')
        sns.lineplot(data=st.session_state.df_zeta_st[-n_num:],x=list(range(n_num)), y='views',color='grey',label='Zeta')
        sns.lineplot(data=st.session_state.df_kobo_st[-n_num:],x=list(range(n_num)), y='views',color='blue',label='Kobo')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Videos Number")
        plt.ylabel(f"{i}")
        plt.title(f"Past {n_num} Videos views")
        st.pyplot(fig)
        #-------------------------------------------------------
        st.subheader('Comments')
        fig = plt.figure(figsize=(7,4))
        sns.lineplot(data=st.session_state.df_kaela_st[-n_num:],x=list(range(n_num)), y='comments',color='red',label='Kaela')
        sns.lineplot(data=st.session_state.df_zeta_st[-n_num:],x=list(range(n_num)), y='comments',color='grey',label='Zeta')
        sns.lineplot(data=st.session_state.df_kobo_st[-n_num:],x=list(range(n_num)), y='comments',color='blue',label='Kobo')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Videos Number")
        plt.ylabel(f"{i}")
        plt.title(f"Past {n_num} Videos comments")
        st.pyplot(fig)
        #-------------------------------------------------------
        
        
    with col2:
        #-------------------------------------------------------   
        st.subheader('Likes')
        fig = plt.figure(figsize=(7,4))
        sns.lineplot(data=st.session_state.df_kaela_st[-n_num:],x=list(range(n_num)), y='likes',color='red',label='Kaela')
        sns.lineplot(data=st.session_state.df_zeta_st[-n_num:],x=list(range(n_num)), y='likes',color='grey',label='Zeta')
        sns.lineplot(data=st.session_state.df_kobo_st[-n_num:],x=list(range(n_num)), y='likes',color='blue',label='Kobo')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Videos Number")
        plt.ylabel(f"{i}")
        plt.title(f"Past {n_num} Videos likes")
        st.pyplot(fig)
        #-------------------------------------------------------
        st.subheader('Favorites')
        fig = plt.figure(figsize=(7,4))
        sns.lineplot(data=st.session_state.df_kaela_st[-n_num:],x=list(range(n_num)), y='favorites',color='red',label='Kaela')
        sns.lineplot(data=st.session_state.df_zeta_st[-n_num:],x=list(range(n_num)), y='favorites',color='grey',label='Zeta')
        sns.lineplot(data=st.session_state.df_kobo_st[-n_num:],x=list(range(n_num)), y='favorites',color='blue',label='Kobo')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Videos Number")
        plt.ylabel(f"{i}")
        plt.title(f"Past {n_num} Videos favorites")
        st.pyplot(fig)
        #-------------------------------------------------------
