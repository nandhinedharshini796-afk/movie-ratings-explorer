import streamlit as st
import plotly.express as px
import sqlite3
import pandas as pd

st.title("Movie Ratings Explorer")

conn = sqlite3.connect("movies.db")
movies = pd.read_sql("SELECT * FROM movies", conn)
genres = pd.read_sql("SELECT * FROM genres", conn)
conn.close()

# left side filters
st.sidebar.header("Filters")
all_genres = sorted(genres["genre"].unique())
selected_genre = st.sidebar.selectbox("Genre", ["All"] + all_genres)

year_min = int(movies["year"].min())
year_max = int(movies["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (2000, year_max))

min_rating = st.sidebar.slider("Minimum rating", 0.0, 10.0, 6.0, 0.5)
min_votes = st.sidebar.slider("Minimum votes", 0, 5000, 100, 50)

# search box
search = st.text_input("Search movie title")

# filters apply
result = movies[
    (movies["year"] >= year_range[0])
    & (movies["year"] <= year_range[1])
    & (movies["vote_average"] >= min_rating)
        & (movies["vote_count"] >= min_votes)
]

if selected_genre != "All":
    ids = genres[genres["genre"] == selected_genre]["movie_id"]
    result = result[result["id"].isin(ids)]

if search:
    result = result[result["title"].str.contains(search, case=False)]

st.write(f"{len(result)} movies found")
st.dataframe(
    result[["title", "year", "vote_average", "vote_count"]]
    .sort_values("vote_average", ascending=False)
)
st.subheader("Charts")

# 1. Genre wise average rating
merged = genres.merge(movies, left_on="movie_id", right_on="id")
genre_stats = (
    merged.groupby("genre")["vote_average"]
    .mean()
    .round(2)
    .reset_index()
    .sort_values("vote_average", ascending=False)
)
fig1 = px.bar(genre_stats, x="genre", y="vote_average",
              title="Average Rating by Genre")
st.plotly_chart(fig1)

# 2. Year wise average rating (filters apply aagum)
year_stats = result.groupby("year")["vote_average"].mean().reset_index()
fig2 = px.line(year_stats, x="year", y="vote_average",
               title="Average Rating by Year")
st.plotly_chart(fig2)

# 3. Rating distribution
fig3 = px.histogram(result, x="vote_average", nbins=20,
                    title="Rating Distribution")
st.plotly_chart(fig3)