import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Midterm Streamlit App",
    page_icon="images/dali.png",
    layout="centered"
)

st.markdown(
    """
    <style>
    body {
        background-image: url('C:\\Users\\therese\\Desktop\\spotify.jpg'); /* Use the path to your image file or a URL */
        background-size: cover; /* Cover the entire background */
        background-position: center; /* Center the background image */
        color: #fff; /* Change text color for better visibility */
    }
    h1 {
        color: #ffd700;
        text-align: center;
    }
    h2, h3 {
        color: #0056b3;
        text-align: center;
    }
    
    .stDataframe {  
        background-color: red;
        border-collapse: collapse;
        width: 100%;
        border: 1px solid #ccc;
    }
    
    .dataframe th, .dataframe td {
        border: 1px solid #ccc;
        padding: 8px;
        text-align: left;
    }
    
    .matplotlib-figure {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

DATA_URL = "dataset/Spotify Most Streamed Songs.csv"
data = pd.read_csv(DATA_URL)

st.title("Data Exploration Report")
st.write("""
## Introduction
This report explores the dataset obtained from [Kaggle](https://www.kaggle.com/datasets/abdulszz/spotify-most-streamed-songs). The purpose of this exploration is to analyze the most streamed songs on Spotify examining factors such as their artist count, how many times they are in a Spotify playlist, and additional insights from other popular streaming platforms like Apple Music, Deezer, and Shazam.
""")


st.subheader('Raw Data')

def style_dataframe(df):
    return df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [
                ('background-color', '#00509E'),
                ('color', 'white'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '16px'),
                ('border', '1px solid #00509E'),
            ]
        }, 
        {
            'selector': 'td',
            'props': [
                ('border', '2px solid #00509E'),
                ('word-wrap', 'break-word'), 
                ('max-width', '150px'),
                ('overflow', 'hidden'),
                ('text-overflow', 'ellipsis'),
                ('white-space', 'nowrap')   
            ]
        },
        {
            'selector': 'table',
            'props': [
                ('table-layout', 'fixed'), 
                ('width', '100%')
            ]
        }]
    )

    
styled_df = style_dataframe(data)

st.markdown(
    f"<div style='max-height: 400px; overflow: auto;'>{styled_df.to_html(escape=False)}</div>",
    unsafe_allow_html=True
)


cleaned_data = data.drop(columns=['cover_url', 'key', 'bpm', 'mode', 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%', 'released_month', 'released_day', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts'])

cleaned_data['streams'] = pd.to_numeric(cleaned_data['streams'], errors='coerce').fillna(0)
cleaned_data['in_spotify_playlists'] = pd.to_numeric(cleaned_data['in_spotify_playlists'], errors='coerce').fillna(0)
cleaned_data['in_apple_playlists'] = pd.to_numeric(cleaned_data['in_apple_playlists'], errors='coerce').fillna(0)
cleaned_data['in_deezer_playlists'] = pd.to_numeric(cleaned_data['in_deezer_playlists'], errors='coerce').fillna(0)


st.subheader('Cleaned Data')

styled_df = style_dataframe(cleaned_data)

st.markdown(
    f"<div style='max-height: 400px; overflow: auto;'>{styled_df.to_html(escape=False)}</div>",
    unsafe_allow_html=True
)

st.header("Visualizations")

plt.figure(figsize=(10, 6))
top_tracks = cleaned_data[['track_name', 'streams']].nlargest(10, 'streams')
plt.title('Top 10 Tracks by Streams', fontsize=16)
blue_palette = sns.dark_palette("blue", as_cmap=False, n_colors=len(top_tracks))

sns.barplot(x='streams', y='track_name', data=top_tracks,  palette=blue_palette)

plt.xlabel('Total Streams', fontsize=14)
plt.ylabel('Tracks', fontsize=14)
plt.yticks(rotation=45)
st.pyplot(plt)
plt.clf()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=cleaned_data, x='artist_count', y='streams', alpha=0.6, color='blue')

plt.xlabel('Number of Artists', fontsize=14)
plt.ylabel('Number of Streams', fontsize=14)

plt.title('Artist Count vs. Streams', fontsize=16)
sns.regplot(data=cleaned_data, x='artist_count', y='streams', scatter_kws={'color': 'blue'}, line_kws={"color": "red", "alpha": 0.7, "linewidth": 2}
)
plt.xlabel('Artist Count', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
st.pyplot(plt)
plt.clf()

filtered_data = cleaned_data[cleaned_data['released_year'] >= 2000]

plt.figure(figsize=(12, 6))

yearly_data = filtered_data.groupby('released_year').agg(
    total_streams=('streams', 'sum')
).reset_index()

plt.title('Total Streams of Tracks Released by Year (2000 Onwards)', fontsize=16)
blue_palette = sns.dark_palette("blue", as_cmap=False, n_colors=len(yearly_data),reverse=True)
plt.bar(yearly_data['released_year'], yearly_data['total_streams'], color=blue_palette)


plt.xlabel('Years', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(yearly_data['released_year'], rotation=45)
plt.legend()

st.pyplot(plt)
plt.clf()

top_tracks = cleaned_data.nlargest(10, 'in_spotify_playlists')
top_tracks['track_label'] = top_tracks['track_name'] + ' (' + top_tracks['in_spotify_playlists'].astype(str) + ')'

plt.figure(figsize=(12, 6))
blue_palette = sns.dark_palette("blue", as_cmap=False, n_colors=len(top_tracks),reverse=True)
sns.barplot(x='track_label', y='streams', data=top_tracks, palette=blue_palette)
plt.title('Top 10 Tracks in Spotify Playlists and Their Streams', fontsize=16)
plt.xlabel('Tracks', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend().remove()
st.pyplot(plt)
plt.clf()

top_apple_tracks = cleaned_data.nlargest(10, 'in_apple_playlists')
top_apple_tracks['track_label'] = top_apple_tracks['track_name'] + ' (' + top_apple_tracks['in_apple_playlists'].astype(str) + ')'

plt.figure(figsize=(12, 6))
blue_palette = sns.dark_palette("blue", as_cmap=False, n_colors=len(top_apple_tracks),reverse=True)
sns.barplot(x='track_label', y='streams', data=top_apple_tracks, palette=blue_palette)
plt.title('Top 10 Tracks in Apple Playlists and Their Streams', fontsize=16)
plt.xlabel('Tracks', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend().remove()
st.pyplot(plt)
plt.clf()

top_deezer_tracks = cleaned_data.nlargest(10, 'in_deezer_playlists')
top_deezer_tracks['track_label'] = top_deezer_tracks['track_name'] + ' (' + top_deezer_tracks['in_deezer_playlists'].astype(str) + ')'

plt.figure(figsize=(12, 6))
blue_palette = sns.dark_palette("blue", as_cmap=False, n_colors=len(top_deezer_tracks),reverse=True)
sns.barplot(x='track_label', y='streams', data=top_deezer_tracks, palette=blue_palette)
plt.title('Top 10 Tracks in Deezer Playlists and Their Streams', fontsize=16)
plt.xlabel('Tracks', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(rotation=45, ha='right')

plt.legend().remove()
st.pyplot(plt)
plt.clf()

st.header("Conclusion")
st.write("""
In conclusion, the analysis of the dataset revealed several key insights:
- An increase in the number of artists does not necessarily lead to more streams.
- The most-streamed songs are not always the ones featured in the most playlists, and vice versa.
- More recent songs tend to have higher streaming numbers.

These findings highlight the complexities of streaming trends in the music industry. While collaboration among artists can enhance visibility, it does not guarantee higher streaming figures. Similarly, the relationship between playlist placements and streaming numbers is not straightforward, suggesting that other factors influence listener engagement. The trend of newer songs gaining more streams reflects changing listener preferences and the influence of contemporary music trends.
""")
