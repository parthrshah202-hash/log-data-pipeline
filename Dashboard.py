import os
import pandas as pd
import streamlit as st

st.title("📊Log Data Processing and Insight Pipeline")
st.divider()
st.header("Transforming raw server logs into structured insights through a modular Python data pipeline.",divider=True)
st.subheader("Description : This project ingests raw server log data, cleans and transforms it, and generates analytical insights through a structured ETL pipeline.",divider=True)



st.subheader("📁 Source Details",divider=True)
file_path="Data/CLEANED/cleaned_server_logs.csv"
df=pd.read_csv(file_path)   
st.markdown("**Raw file** : server_logs.csv")
st.markdown("**Date Created** : 1 Feb 2026")
st.markdown(f"**File size** : {os.path.getsize(file_path)/1024} KB")
 


st.subheader("🎯Project Flow",divider=True)
st.write("*Data Ingestion → Cleaning → Transformation → Analysis → Visualization*")
st.write("Designed using modular Python scripts to simulate a real-world ETL pipeline architecture.")
 


st.subheader("Total Metrics Created : 5",divider=True)
st.write("• **User Metrics** - Behavior patterns and activity levels")
st.write("• **Endpoint Analysis** - Performance and error rates")
st.write("• **Hourly Patterns** - Traffic distribution by hour")
st.write("• **Daily Trends** - Traffic changes over time")
st.write("• **HTTP Methods** - Request distribution by method")



st.subheader("🛠️ TechStack:", divider=True)
st.markdown("""
- Python
- NumPy
- Pandas
- Matplotlib
- Streamlit
""")
 

st.write("")

st.info("👈 Use the sidebar to navigate between different analysis sections")


