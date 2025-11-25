import streamlit as st
import pandas as pd
import os

st.title("🎬 Movie Rating Analysis")
st.markdown("### Big Data Analytics - Group Project")

# Path definition
output_path = "/home/user/project_output"

try:
    # Load Spark Output
    csv_file = [f for f in os.listdir(output_path) if f.endswith('.csv')][0]
    df = pd.read_csv(os.path.join(output_path, csv_file))
    
    st.metric("Total Movies Analyzed", len(df))
    st.dataframe(df.head(50))
    st.bar_chart(df['avg_rating'].value_counts())
except:
    st.warning("Awaiting Spark Job Execution...")