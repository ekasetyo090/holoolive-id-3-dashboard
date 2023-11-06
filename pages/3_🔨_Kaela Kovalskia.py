# Import necessary libraries: These are common libraries for data analysis, visualization, and web app development.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import statistics as stats

# Retrieve a DataFrame named 'df_kaela_zeta_st' from the Streamlit session state. This DataFrame is used for further analysis.
df_kaela = st.session_state.df_kaela_st
# Calculate various statistics related to video views, likes, comments, and favorites, including deltas and moving averages.
# calculate views widget
views = df_kaela['views'].iloc[-1]
views_delta = df_kaela['views'].iloc[-1] - df_kaela['views'].iloc[-2]

# calculate likes widget
likes = df_kaela['likes'].iloc[-1]
likes_delta = df_kaela['likes'].iloc[-1] - df_kaela['likes'].iloc[-2]

# calculate comments widget
comments = df_kaela['comments'].iloc[-1]
comments_delta = df_kaela['comments'].iloc[-1] - df_kaela['comments'].iloc[-2]

# calculate favorites widget
favorites = df_kaela['favorites'].iloc[-1]
favorites_delta = df_kaela['favorites'].iloc[-1] - df_kaela['favorites'].iloc[-2]


# Calculate average views, likes, comments, and favorites over the last 30 days, 
# along with their deltas and display these statistics. This is done for each metric.
average_views = round((df_kaela['views'].iloc[-30:-1].sum() / len(df_kaela['views'].iloc[-30:-1])),2)
average_views_last = df_kaela['views'].iloc[-31:-2].sum() / len(df_kaela['views'].iloc[-31:-2])
average_views_delta = round(average_views - average_views_last,2)
#-----------------------------------------
average_likes = round((df_kaela['likes'].iloc[-30:-1].sum() / len(df_kaela['likes'].iloc[-30:-1])),2)
average_likes_last = df_kaela['likes'].iloc[-31:-2].sum() / len(df_kaela['likes'].iloc[-31:-2])
average_likes_delta = round(average_likes - average_likes_last,2)
#-----------------------------------------
average_comments = round((df_kaela['comments'].iloc[-30:-1].sum() / len(df_kaela['comments'].iloc[-30:-1])), 2)
average_comments_last = df_kaela['comments'].iloc[-31:-2].sum() / len(df_kaela['comments'].iloc[-31:-2])
average_comments_delta = round(average_comments - average_comments_last,2)
#-----------------------------------------
average_favorites = round((df_kaela['favorites'].iloc[-30:-1].sum() / len(df_kaela['favorites'].iloc[-30:-1])), 2)
average_favorites_last = df_kaela['favorites'].iloc[-31:-2].sum() / len(df_kaela['favorites'].iloc[-31:-2])
average_favorites_delta = round(average_favorites - average_favorites_last,2)

st.set_page_config(
    page_title='🔨Kaela Kovalskia')

st.image("https://scontent.fbwx2-1.fna.fbcdn.net/v/t39.30808-6/276149749_111948848125111_5965407865403464817_n.jpg?stp=dst-jpg_p320x320&_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_ohc=B3jcxL3F_zUAX-MOFt0&_nc_ht=scontent.fbwx2-1.fna&oh=00_AfCoLFm2DJVKa-K2NFzcRgznyeLl6BSFIzFzBsIqS-yDzw&oe=654D93FE")

st.header('🔨Kaela Kovalskia')


# Create a tabbed interface
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Summary", "Over Range Statistic",
                                              "Correlation","Spread",
                                              "Top <N> Videos All Time", "Top Past <N> Videos"]
                                            )

# The following sections of code correspond to each of the tabs.
# summary tab
with tab1:
    st.subheader('Statistic Change From 2nd to Last Video')
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Views", value=f"{views}", delta=f"{views_delta}")
        st.metric(label="Comments", value=f"{comments}", delta=f"{comments_delta}")
        
    with col2:
        st.metric(label="Likes", value=f"{likes}", delta=f"{likes_delta}")
        st.metric(label="Favorites", value=f"{favorites}", delta=f"{favorites_delta}")
    
    st.subheader('Moving Average')
    col3, col4 = st.columns(2)
    #-----------------------------------------
    
    with col3:
        st.metric(label="Moving Average 30 Days (Views/Videos)", value=f"{average_views}", delta=f"{average_views_delta}")
        st.metric(label="Moving Average 30 Days (Comments/Videos)", value=f"{average_comments}", delta=f"{average_comments_delta}")
        
    #-----------------------------------------    
    with col4:
        st.metric(label="Moving Average 30 Days (Likes/Videos)", value=f"{average_likes}", delta=f"{average_likes_delta}")
        st.metric(label="Moving Average 30 Days (Favorites/Videos)", value=f"{average_favorites}", delta=f"{average_favorites_delta}")
        #-----------------------------------------        
    st.subheader('Metrics Statistics')    
    col5, col6 = st.columns(2)
    with col5:
        #-----------------------------------------
        fig = plt.figure(figsize=(7,4))
        ax = sns.lineplot(data=df_kaela[-30:],x='date', y='views',color='blue',label='Videos Views')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel('Views')
        plt.title("Videos Views Past 30 Days")
        st.pyplot(fig)
        #-----------------------------------------        
        fig = plt.figure(figsize=(7,4))
        ax = sns.lineplot(data=df_kaela[-30:],x='date', y='comments',color='blue',label='Videos Comments')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel('Comments')
        plt.title("Videos Comments Past 30 Days")
        st.pyplot(fig)
    with col6:
        fig = plt.figure(figsize=(7,4))
        ax = sns.lineplot(data=df_kaela[-30:],x='date', y='likes',color='blue',label='Videos Likes')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel('Likes')
        plt.title("Videos Likes Past 30 Days")
        st.pyplot(fig)
        #-----------------------------------------        
        fig = plt.figure(figsize=(7,4))
        ax = sns.lineplot(data=df_kaela[-30:],x='date', y='favorites',color='blue',label='Videos Favorites')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel('Favorites')
        plt.title("Videos Favorites Past 30 Days")
        st.pyplot(fig)

# Over Range Statistic tab
with tab2:
    st.subheader('Range Selection')
    value = st.slider(label='Select Range Of Videos (Start : End)',
                       min_value=0, max_value=len(df_kaela), value=(0, len(df_kaela)))
    st.write('Total Videos Selected:', value[1]-value[0])
    st.subheader('Tag Percentages')
    value_counts = df_kaela[value[0]:value[1]]['tag_used'].value_counts()
    total_count = len( df_kaela[value[0]:value[1]])
    
    if 'Yes' in value_counts:
        percentage_yes = round(((value_counts['Yes'] / total_count) * 100), 2)
    else:
        percentage_yes = 0  # Handle the case where 'Yes' is not present

    if 'No' in value_counts:
        percentage_no = round(((value_counts['No'] / total_count) * 100), 2)
    else:
        percentage_no = 0  # Handle the case where 'No' is not present

    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Percentage Videos Used Tag", value=f"{percentage_yes}%", delta=None)
        
    with col2:
        st.metric(label="Percentage Videos Not Used Tag", value=f"{percentage_no}%", delta=None)

    #----------------------------------------- 

    col3, col4 = st.columns(2)
    with col3:
        # draw line chart
        st.subheader('Line Chart')
        #----------------------------------------- 
        fig = plt.figure(figsize=(9,5))
        ax = sns.lineplot(data=df_kaela[value[0]:value[1]],x='date', y='views',color='blue')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel("Views")
        plt.title("Videos Views")
        st.pyplot(fig)
        #----------------------------------------- 
        
        fig = plt.figure(figsize=(9,5))
        ax = sns.lineplot(data=df_kaela[value[0]:value[1]],x='date', y='likes',color='blue')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel("Likes")
        plt.title("Videos Likes")
        st.pyplot(fig)
        #----------------------------------------- 
        fig = plt.figure(figsize=(9,5))
        ax = sns.lineplot(data=df_kaela[value[0]:value[1]],x='date', y='comments',color='blue')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel("Comments")
        plt.title("Videos Comments")
        st.pyplot(fig)
        #----------------------------------------- 
        fig = plt.figure(figsize=(9,5))
        ax = sns.lineplot(data=df_kaela[value[0]:value[1]],x='date', y='favorites',color='blue')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Date")
        plt.ylabel("Favorites")
        plt.title("Videos Favorites")
        st.pyplot(fig)
        #----------------------------------------- 
        

    with col4:
        # draw regression chart
        st.subheader('Regression Chart')
        #-----------------------------------------             
        x_scale = list(range(0, value[1]-value[0], 1))
        fig = plt.figure(figsize=(9,5))
        ax = sns.regplot(data=df_kaela[value[0]:value[1]],x=x_scale, y='views',color='blue',order=2)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Video index")
        plt.ylabel('Views')
        plt.title("Videos Views")
        st.pyplot(fig)
        #----------------------------------------- 
        x_scale = list(range(0, value[1]-value[0], 1))
        fig = plt.figure(figsize=(9,5))
        ax = sns.regplot(data=df_kaela[value[0]:value[1]],x=x_scale, y='likes',color='blue',order=2)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Video index")
        plt.ylabel("Likes")
        plt.title("Videos Likes")
        st.pyplot(fig)
        #----------------------------------------- 
        x_scale = list(range(0, value[1]-value[0], 1))
        fig = plt.figure(figsize=(9,5))
        ax = sns.regplot(data=df_kaela[value[0]:value[1]],x=x_scale, y='comments',color='blue',order=2)
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Video index")
        plt.ylabel('Comments')
        plt.title("Videos Comments")
        st.pyplot(fig)
        #-----------------------------------------
        x_scale = list(range(0, value[1]-value[0], 1))
        fig = plt.figure(figsize=(9,5))
        ax = sns.regplot(data=df_kaela[value[0]:value[1]],x=x_scale, y='favorites',color='blue')
        plt.ticklabel_format(style='plain', axis='y')
        plt.xlabel("Video index")
        plt.ylabel('Favorites')
        plt.title("Videos Favorites")
        st.pyplot(fig)
        #-----------------------------------------
        
# Correlation tab        
with tab3:
    corr_metrics = st.selectbox(label="Correlation Metrics",
                                options=('Views VS Likes', 'Views VS Comments',
                                         'Likes VS Comments','Duration VS Views',
                                         'Duration VS Likes','Duration VS Comments')
                               )
    x_axis_count_videos = list(range(len(df_kaela)))
    dict_axis = {'Views VS Likes':{'x':'views','y':'likes'},
                 'Views VS Comments':{'x':'views','y':'comments'},
                 'Likes VS Comments':{'x':'likes','y':'comments'},                 
                 'Duration VS Views':{'x':'duration','y':'views'},
                 'Duration VS Likes':{'x':'duration','y':'likes'},
                 'Duration VS Comments':{'x':'duration','y':'comments'},
                }
    x_axis = dict_axis[corr_metrics].get('x')
    y_axis = dict_axis[corr_metrics].get('y')
    if x_axis == 'duration':
        x_axis_labels = 'Duration In Seconds'
    else:
        x_axis_labels =x_axis
    fig = plt.figure(figsize=(9,5))
    ax = sns.regplot(data=df_kaela,x=x_axis, y=y_axis,color='blue',order=2,label='Corelation metrics')
    plt.ticklabel_format(style='plain', axis='y')
    plt.ticklabel_format(style='plain', axis='x')
    plt.xlabel(f"{x_axis_labels}")
    plt.ylabel(f"{y_axis}")
    plt.title(f"Metrics Correlation {corr_metrics}")
    st.pyplot(fig)
        
# Spread tab
with tab4:
    spread_metrics = st.selectbox(label="Spread Metrics",
                                  options=('Views', 'Likes',
                                           'Comments','Duration',
                                          )
                                 )
    spread_axis = {'Views':"views",
                   'Likes':"likes",
                   'Comments':"comments",                 
                   'Duration':"duration",
                  }
    #-----------------------------------------
    df_kaela_spread = df_kaela[spread_axis.get(spread_metrics)]
    mesage_median = f"Median = {round(df_kaela_spread.median(),2)}"
    mesage_mean = f"Mean = {round(df_kaela_spread.mean(),2)}"
    modes = df_kaela_spread.mode(dropna=True)
    mesage_mode = f"Mode = {modes[0]}"
    mesage_std = f"Standard Deviation (STD)= {round(df_kaela_spread.std(),2)}"
    if spread_metrics == "Duration":
        spread_title = f'Spread Of {spread_metrics} (Seconds)'
    else:
        spread_title = f'Spread Of {spread_metrics}'
    # draw spread histogram chart
    fig = plt.figure(figsize = (10, 5))
    line_sale_median = plt.axvline(x = df_kaela_spread.median(), color = 'Blue', ls = '--', lw = 1.5, label = "Median")
    line_sale_mean = plt.axvline(x = df_kaela_spread.mean(), color = 'green', ls = '--', lw = 1.5, label = "Mean")
    line_sale_STD = plt.axvline(x = df_kaela_spread.std(), color = 'red', ls = '--', lw = 1.5, label = "STD")
    ## legend
    legend = plt.legend(handles = [line_sale_STD, line_sale_mean, line_sale_median], loc = 1)
    sns.histplot(data = df_kaela_spread, common_norm = True, color = '#b3afb2', edgecolor = '#1f041e').set(title=spread_title)
    plt.ticklabel_format(style='plain', axis='x')
    st.pyplot(fig)
    
    # write mesage of central tendency
    st.write(mesage_median)
    st.write(mesage_mean)
    st.write(mesage_mode)
    st.write(mesage_std)
    st.dataframe(data=df_kaela_spread)

# Top 50 Videos All Time tab
with tab5:
    st.subheader('Top <N> Videos All Time')
    n_number_all = st.number_input(label="Input <N> Videos All Time then press (Enter)", 
                                   min_value=0, max_value=None, 
                                   value="min",label_visibility="visible")
    if n_number_all>0:
        st.subheader('Top <N> Videos All Time Tag Usages')

        df_kaela_all_time = df_kaela.sort_values(by=['views','likes','comments','favorites'],ascending=False).reset_index(drop=True)
        df_kaela_all_time = df_kaela_all_time[:n_number_all]
        value_counts = df_kaela_all_time['tag_used'].value_counts()
        total_count = len(df_kaela_all_time)

        # calculated percentages tag used videos
        if 'Yes' in value_counts:
            percentage_yes = round(((value_counts['Yes'] / total_count) * 100), 2)
        else:
            percentage_yes = 0  # Handle the case where 'Yes' is not present

        if 'No' in value_counts:
            percentage_no = round(((value_counts['No'] / total_count) * 100), 2)
        else:
            percentage_no = 0  # Handle the case where 'No' is not present

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Percentage Videos Used Tag", value=f"{percentage_yes}%", delta=None)

        with col2:
            st.metric(label="Percentage Videos Not Used Tag", value=f"{percentage_no}%", delta=None)

        st.subheader('Table Video Information')
        addon_collumns_all = st.multiselect(label="Additioan Collumn",
                               options=('video_tag', 'thumbnail', 'video_url')
                              )
        st.dataframe(data=df_kaela_all_time[['views','likes','comments','favorites']+addon_collumns_all])

with tab6:
    st.subheader('Top Past <N> Videos')
    n_number = st.number_input(label="Input Top Past <N> then press (Enter)", 
                               min_value=0, max_value=None, value="min",label_visibility="visible")
    if n_number>0:
        df_kaela_n = df_kaela[-n_number:].sort_values(by=['views','likes','comments','favorites'],ascending=False).reset_index(drop=True)
        value_counts = df_kaela_n['tag_used'].value_counts()
        total_count = len(df_kaela_n)

        if 'Yes' in value_counts:
            percentage_yes = round(((value_counts['Yes'] / total_count) * 100), 2)
        else:
            percentage_yes = 0  # Handle the case where 'Yes' is not present

        if 'No' in value_counts:
            percentage_no = round(((value_counts['No'] / total_count) * 100), 2)
        else:
            percentage_no = 0  # Handle the case where 'No' is not present


        st.subheader('Top Past <N> Videos Tag Usages')
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Percentage Videos Used Tag", value=f"{percentage_yes}%", delta=None)

        with col2:
            st.metric(label="Percentage Videos Not Used Tag", value=f"{percentage_no}%", delta=None)

        st.subheader('Table Video Information')
        addon_n = st.multiselect(label="Additioan Collumn For <N> Past",
                               options=('video_tag', 'thumbnail', 'video_url')
                              )
        st.dataframe(data=df_kaela_n[['views','likes','comments','favorites']+addon_n])
        