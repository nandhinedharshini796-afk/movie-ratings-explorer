import pandas as pd
import json
import sqlite3

df = pd.read_csv("tmdb_5000_movies.csv")

# venum nu column mattum edukkalam
df = df[["id", "title", "genres", "release_date", "vote_average", "vote_count"]]

# kaali data remove
df = df.dropna(subset=["release_date"])
df = df[df["vote_count"] > 0]

# release date la irundhu year edukkalam
df["year"] = pd.to_datetime(df["release_date"]).dt.year

# genres la irundhu names mattum edukkalam
def get_genres(text):
    return [g["name"] for g in json.loads(text)]

df["genre_list"] = df["genres"].apply(get_genres)

# rendu table ready pannalam
movies = df[["id", "title", "year", "vote_average", "vote_count"]]
genres = df[["id", "genre_list"]].explode("genre_list").dropna()
genres.columns = ["movie_id", "genre"]

# SQL database la save
conn = sqlite3.connect("movies.db")
movies.to_sql("movies", conn, if_exists="replace", index=False)
genres.to_sql("genres", conn, if_exists="replace", index=False)
conn.close()

print("Done!", movies.shape, genres.shape)
