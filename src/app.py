import streamlit as st
import pandas as pd
import altair as alt

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Cinema Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Load & Process Data ---
DATA_PATH = "/home/hadoop/movie_results.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        # Create a 'Rating Category' for the Pie Chart
        bins = [0, 4.0, 4.5, 4.8, 5.0]
        labels = ['Good (4.0+)', 'Excellent (4.5+)', 'Superb (4.8+)', 'Perfect (5.0)']
        df['Rating_Category'] = pd.cut(df['avg_rating'], bins=bins, labels=labels, include_lowest=True)
        return df
    except FileNotFoundError:
        return None

df = load_data()

# --- 3. Sidebar Filters ---
st.sidebar.header("🎛️ Dashboard Settings")
st.sidebar.info("Big Data Project - Group 4")

if df is not None:
    # Get min and max reviews for slider
    min_rev = int(df['count_id'].min())
    max_rev = int(df['count_id'].max())
    
    # Slider to filter out movies with few reviews
    min_reviews = st.sidebar.slider("Minimum Reviews Filter", 
                                    min_value=min_rev, 
                                    max_value=max_rev, 
                                    value=min_rev)
    
    # Filter the dataframe based on slider
    filtered_df = df[df['count_id'] >= min_reviews]
else:
    filtered_df = None

# --- 4. Main Dashboard UI ---
st.title("🎬 Movie Rating Analytics")
st.markdown("Distributed analysis of **MovieLens 100k** using **Hadoop & Spark**.")
st.markdown("---")

if filtered_df is not None:
    
    # KPI Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Movies Loaded", len(filtered_df))
    with kpi2:
        st.metric("Top Rating", f"{filtered_df['avg_rating'].max()} ⭐")
    with kpi3:
        st.metric("Most Reviewed", f"{filtered_df['count_id'].max()} reviews")
    with kpi4:
        avg_score = round(filtered_df['avg_rating'].mean(), 2)
        st.metric("Average Score", f"{avg_score}")

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Top Charts", "🍩 Distribution & Analysis", "📂 Raw Data"])

    # --- TAB 1: Top Charts (Robust Version) ---
    with tab1:
        st.subheader("🏆 Top 10 Highest Rated Movies")
        
        # 1. Sort the data to get top 10
        top_movies = filtered_df.sort_values(by="avg_rating", ascending=False).head(10)
        
        # 2. Simple Horizontal Bar Chart (Native Streamlit - Works everywhere)
        st.bar_chart(
            top_movies.set_index("title")["avg_rating"],
            color="#FFA500"  # Gold/Orange color
        )
        
        # 3. Detailed Data View with Visual Progress Bars
        st.caption("Detailed Rating Data")
        st.dataframe(
            top_movies[['title', 'avg_rating', 'count_id']],
            column_config={
                "title": "Movie Title",
                "avg_rating": st.column_config.ProgressColumn(
                    "Rating", 
                    format="%.2f", 
                    min_value=0, 
                    max_value=5
                ),
                "count_id": st.column_config.NumberColumn("Reviews")
            },
            hide_index=True,
            use_container_width=True
        )

    # --- TAB 2: Pie Charts & Scatter Plots ---
    with tab2:
        col_pie, col_scatter = st.columns([1, 2])

        with col_pie:
            st.subheader("Rating Distribution")
            # Prepare data for Pie Chart
            pie_data = filtered_df['Rating_Category'].value_counts().reset_index()
            pie_data.columns = ['Category', 'Count']
            
            # Altair Donut Chart
            pie = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Category", type="nominal", scale=alt.Scale(scheme='category20b')),
                tooltip=['Category', 'Count']
            ).properties(height=350)
            st.altair_chart(pie, use_container_width=True)

        with col_scatter:
            st.subheader("🔍 Popularity vs. Quality")
            st.markdown("*Does having more reviews mean a better rating?*")
            
            # Scatter Plot
            scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
                x=alt.X('count_id', title='Number of Reviews'),
                y=alt.Y('avg_rating', title='Average Rating', scale=alt.Scale(domain=[3.5, 5.2])),
                color=alt.Color('Rating_Category', title='Category'),
                tooltip=['title', 'avg_rating', 'count_id']
            ).interactive().properties(height=350)
            
            st.altair_chart(scatter, use_container_width=True)

    # --- TAB 3: Data Table ---
    with tab3:
        st.subheader("Complete Dataset")
        st.dataframe(
            filtered_df,
            column_config={
                "title": "Movie Title",
                "avg_rating": st.column_config.NumberColumn("Rating", format="%.2f ⭐"),
                "count_id": st.column_config.NumberColumn("Reviews", format="%d 👤"),
                "Rating_Category": "Tier"
            },
            use_container_width=True,
            height=600
        )

else:
    st.error("⚠️ Spark Output Not Found!")
    st.info("Run: /usr/local/spark/bin/spark-submit --master yarn --deploy-mode client movie_analysis.py")
