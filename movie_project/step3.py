import sqlite3
import pandas as pd

conn = sqlite3.connect("movies.db")

print("Top genres by average rating:")
q1 = """
SELECT g.genre, COUNT(*) AS movie_count, ROUND(AVG(m.vote_average), 2) AS avg_rating
FROM movies m
JOIN genres g ON m.id = g.movie_id
GROUP BY g.genre
ORDER BY avg_rating DESC
"""
print(pd.read_sql(q1, conn))

print("\nTop 10 movies (1000+ votes):")
q2 = """
SELECT title, year, vote_average, vote_count
FROM movies
WHERE vote_count >= 1000
ORDER BY vote_average DESC
LIMIT 10
"""
print(pd.read_sql(q2, conn))

conn.close()