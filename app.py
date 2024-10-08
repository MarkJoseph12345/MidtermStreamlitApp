import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config as the first Streamlit command
st.set_page_config(
    page_title="Midterm Streamlit App",
    page_icon="images/dali.png",
    layout="centered"
)

# Inject custom CSS into the app
st.markdown(
    """
    <style>
    /* Background color for the entire app */
    body {
        background-color: #f0f2f6;
    }

    /* Set custom font family and size for the whole app */
    .reportview-container {
        font-family: "Arial", sans-serif;
        font-size: 16px;
    }

    /* Title and headers styling */
    h1 {
        color: #2c3e50;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    h2 {
        color: #34495e;
        font-size: 30px;
        text-align: center;
        margin-bottom: 15px;
    }

    h3, h4 {
        color: #7f8c8d;
        text-align: center;
    }

    /* Styling the subheader */
    .stMarkdown > h2 {
        color: #3498db;
        font-weight: bold;
        text-align: left;
    }

    /* Styling for tables/dataframes */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        margin: 20px auto;
    }

    .dataframe th, .dataframe td {
        padding: 10px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }

    .dataframe tr:hover {
        background-color: #f1f1f1;
    }

    /* Customize button */
    button {
        background-color: #2ecc71;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
    }

    /* Customize input boxes */
    .stTextInput > div > input {
        border: 2px solid #bdc3c7;
        padding: 5px;
    }

    /* Customize select box */
    .stSelectbox > div > input {
        border: 2px solid #bdc3c7;
    }

    /* Footer styling */
    footer {
        visibility: hidden;
    }

    /* Custom Streamlit sidebar styling */
    .sidebar .sidebar-content {
        background-color: #ecf0f1;
        color: #2c3e50;
        font-family: "Arial", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the dataset
DATA_URL = "dataset/Spotify Most Streamed Songs.csv"
data = pd.read_csv(DATA_URL)

# Page Title and Introduction
st.title("Data Exploration Report")
st.write("""
## Introduction
This report explores the dataset obtained from [Kaggle](https://www.kaggle.com/datasets/abdulszz/spotify-most-streamed-songs). The purpose of this exploration is to analyze the most streamed songs on Spotify examining factors such as their artist count, how many times they are in a Spotify playlist, and additional insights from other popular streaming platforms like Apple Music, Deezer, and Shazam.
""")

# Display raw data
st.subheader('Raw Data')
st.write(data)

# Clean the data
cleaned_data = data.drop(columns=['cover_url', 'key', 'bpm', 'mode', 'danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%', 'released_month', 'released_day', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts'])
cleaned_data['streams'] = pd.to_numeric(cleaned_data['streams'], errors='coerce').fillna(0)
cleaned_data['in_spotify_playlists'] = pd.to_numeric(cleaned_data['in_spotify_playlists'], errors='coerce').fillna(0)
cleaned_data['in_apple_playlists'] = pd.to_numeric(cleaned_data['in_apple_playlists'], errors='coerce').fillna(0)
cleaned_data['in_deezer_playlists'] = pd.to_numeric(cleaned_data['in_deezer_playlists'], errors='coerce').fillna(0)

# Display cleaned data
st.subheader('Cleaned Data')
st.write(cleaned_data)

# Visualizations
st.header("Visualizations")

# Top 10 Tracks by Streams
plt.figure(figsize=(10, 6))
top_tracks = cleaned_data[['track_name', 'streams']].nlargest(10, 'streams')
plt.title('Top 10 Tracks by Streams', fontsize=16)
sns.barplot(x='streams', y='track_name', data=top_tracks)
plt.xlabel('Total Streams', fontsize=14)
plt.ylabel('Tracks', fontsize=14)
plt.yticks(rotation=45)
st.pyplot(plt)
plt.clf()

# Artist Count vs. Streams
plt.figure(figsize=(10, 6))
sns.scatterplot(data=cleaned_data, x='artist_count', y='streams', alpha=0.6, color='blue')
plt.xlabel('Number of Artists', fontsize=14)
plt.ylabel('Number of Streams', fontsize=14)
plt.title('Artist Count vs. Streams', fontsize=16)
sns.regplot(data=cleaned_data, x='artist_count', y='streams', scatter=False, color='red', line_kws={"alpha":0.7, "linewidth":2})
st.pyplot(plt)
plt.clf()

# Total Streams by Year (2000 onwards)
filtered_data = cleaned_data[cleaned_data['released_year'] >= 2000]
plt.figure(figsize=(12, 6))
yearly_data = filtered_data.groupby('released_year').agg(total_streams=('streams', 'sum')).reset_index()
plt.title('Total Streams of Tracks Released by Year (2000 Onwards)', fontsize=16)
plt.bar(yearly_data['released_year'], yearly_data['total_streams'], label='Total Streams')
plt.xlabel('Years', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(yearly_data['released_year'], rotation=45)
plt.legend()
st.pyplot(plt)
plt.clf()

# Top 10 Tracks in Spotify Playlists
top_tracks = cleaned_data.nlargest(10, 'in_spotify_playlists')
top_tracks['track_label'] = top_tracks['track_name'] + ' (' + top_tracks['in_spotify_playlists'].astype(str) + ')'
plt.figure(figsize=(12, 6))
sns.barplot(x='track_label', y='streams', data=top_tracks)
plt.title('Top 10 Tracks in Spotify Playlists and Their Streams', fontsize=16)
plt.xlabel('Tracks', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend().remove()
st.pyplot(plt)
plt.clf()

# Top 10 Tracks in Apple Playlists
top_apple_tracks = cleaned_data.nlargest(10, 'in_apple_playlists')
top_apple_tracks['track_label'] = top_apple_tracks['track_name'] + ' (' + top_apple_tracks['in_apple_playlists'].astype(str) + ')'
plt.figure(figsize=(12, 6))
sns.barplot(x='track_label', y='streams', data=top_apple_tracks)
plt.title('Top 10 Tracks in Apple Playlists and Their Streams', fontsize=16)
plt.xlabel('Tracks', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend().remove()
st.pyplot(plt)
plt.clf()

# Top 10 Tracks in Deezer Playlists
top_deezer_tracks = cleaned_data.nlargest(10, 'in_deezer_playlists')
top_deezer_tracks['track_label'] = top_deezer_tracks['track_name'] + ' (' + top_deezer_tracks['in_deezer_playlists'].astype(str) + ')'
plt.figure(figsize=(12, 6))
sns.barplot(x='track_label', y='streams', data=top_deezer_tracks)
plt.title('Top 10 Tracks in Deezer Playlists and Their Streams', fontsize=16)
plt.xlabel('Tracks', fontsize=14)
plt.ylabel('Total Streams', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend().remove()
st.pyplot(plt)
plt.clf()

# Conclusion
st.header("Conclusion")
st.write("""
In conclusion, the analysis of the dataset revealed several key insights:
- An increase in the number of artists does not necessarily lead to more streams.
- The most-streamed songs are not always the ones featured in the most playlists, and vice versa.
- More recent songs tend to have higher streaming numbers.

These findings highlight the complexities of streaming trends in the music industry. While collaboration among artists can enhance visibility, it does not guarantee higher streaming figures. Similarly, the relationship between playlist placements and streaming numbers is not straightforward, suggesting that other factors influence listener engagement. The trend of newer songs gaining more streams reflects changing listener preferences and the influence of contemporary music trends.
""")  # Properly close the triple-quoted string here

