import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from pyspark import SparkContext

MASTER_URL = "spark://192.168.43.59:7077"
sc = SparkContext(MASTER_URL, "SimpleTestApp")

# -----------------------------
# Streamlit UI HEADER
# -----------------------------
st.set_page_config(page_title="Movie Ratings Dashboard", layout="wide")

st.title("🎬 Movie Ratings Analytics Dashboard")
st.write("Powered by **PySpark + Pandas + Streamlit**")

# -----------------------------
# FILE LOAD
# -----------------------------
movies_file = r"C:/Users/tanis/Desktop/movies.csv"
ratings_file = r"C:/Users/tanis/Desktop/ratings.csv"

movies_df = pd.read_csv(movies_file)
ratings_df = pd.read_csv(ratings_file)

st.subheader("📌 Raw Data Preview")

col1, col2 = st.columns(2)

with col1:
    st.write("🎞 Movies Data")
    st.dataframe(movies_df.head())

with col2:
    st.write("⭐ Ratings Data")
    st.dataframe(ratings_df.head())

# -----------------------------
# MISSING VALUES
# -----------------------------
st.subheader("🚨 Missing Values Check")
colA, colB = st.columns(2)

with colA:
    st.write("🎞 Movies Missing Values")
    st.dataframe(movies_df.isnull().sum().to_frame("Missing Count"))

with colB:
    st.write("⭐ Ratings Missing Values")
    st.dataframe(ratings_df.isnull().sum().to_frame("Missing Count"))


# -----------------------------
# DISTRIBUTION OF RATINGS
# -----------------------------
st.subheader("📊 Distribution of Ratings")

fig1 = plt.figure(figsize=(10,5))
sns.histplot(ratings_df["rating"], bins=30, kde=True, color="red")
plt.title("Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Count")
st.pyplot(fig1)


# -----------------------------
# GENRE POPULARITY
# -----------------------------
st.subheader("🔥 Top 10 Movie Genres")
genres_count = movies_df["genres"].value_counts().head(10)
st.bar_chart(genres_count)


# -----------------------------
# MERGING DATASETS
# -----------------------------
merged_df = pd.merge(ratings_df, movies_df, on="movieId")
merged_df = pd.get_dummies(merged_df, columns=["platform_Name", "genres"],
                           prefix=["platform", "genre"])

st.subheader("🔗 Merged Dataset Preview")
st.dataframe(merged_df.head())


# -----------------------------
# PLATFORM COMPARISON
# -----------------------------
st.subheader("🎭 Rating Distribution: Chorki Platform")

if "platform_Chorki" in merged_df.columns:
    fig2 = plt.figure(figsize=(10,5))
    sns.histplot(data=merged_df, x="rating", hue="platform_Chorki", kde=True)
    plt.title("Ratings by Platform (Chorki)")
    st.pyplot(fig2)
else:
    st.info("ℹ️ Column 'platform_Chorki' not found.")


# -----------------------------
# SUMMARY STATISTICS
# -----------------------------
st.subheader("📈 Ratings Summary Statistics")

rating_stats = merged_df["rating"].describe()
top_rated = merged_df.groupby("title")["rating"].mean().nlargest(5)
lowest_rated = merged_df.groupby("title")["rating"].mean().nsmallest(5)

col3, col4, col5 = st.columns(3)

with col3:
    st.write("📌 Summary Stats")
    st.dataframe(rating_stats.to_frame())

with col4:
    st.write("🏆 Top 5 Rated Movies")
    st.dataframe(top_rated)

with col5:
    st.write("💀 Lowest Rated Movies")
    st.dataframe(lowest_rated)


# -----------------------------
# USER ACTIVITY ANALYSIS
# -----------------------------
st.subheader("🧑‍🤝‍🧑 User Activity Analysis")

avg_per_user = merged_df.groupby("userId")["rating"].count().mean()
active_users = merged_df["userId"].value_counts().head(5)

st.write(f"**Average Ratings per User:** {avg_per_user:.2f}")
st.write("🔥 **Top 5 Most Active Users:**")
st.dataframe(active_users)


# -----------------------------
# CORRELATION HEATMAP
# -----------------------------
st.subheader("🌡 Correlation Between Ratings & Genres")

cols = [col for col in merged_df.columns if col.startswith("genre_")]
selected_cols = ["rating"] + cols[2:8]   # take first 2 genre columns only

corr = merged_df[selected_cols].corr()

fig3 = plt.figure(figsize=(8,5))
sns.heatmap(corr, annot=True, cmap="coolwarm")
st.pyplot(fig3)

st.success("✔ Dashboard Loaded Successfully!")

sc.stop()
