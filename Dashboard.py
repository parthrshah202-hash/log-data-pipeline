import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="📊Log Data Processing and Insight Pipeline",layout="wide")

#Function to load data
@st.cache_data
def load_data(filename):
    df=pd.read_csv(filename)
    return df

#Function to load report
@st.cache_data
def load_report(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
    
    
    
#Sidebar
with st.sidebar:
    st.title("🗒️Navigation")
    st.write("")
    page=st.selectbox("Choose a Metrics",["Overview","User Metrics","Endpoint Analysis","Hourly Patterns","Daily Trends","HTTP Methods"])

#OVERVIEW PAGE
if page=="Overview":
    st.title("📊Log Data Processing and Insight Pipeline")
    st.header("*Transforming raw server logs into structured insights through a modular Python data pipeline.*")
    st.subheader("Description : This project ingests raw server log data, cleans and transforms it, and generates analytical insights through a structured ETL pipeline.",divider=True)
    st.write("")


    st.subheader("📁 Source Details")
    file_path="Data/CLEANED/cleaned_server_logs.csv"
    df=load_data(file_path)
    
    st.markdown("**Raw file** : server_logs.csv")
    st.markdown("**Date Created** : 1 Feb 2026")
    size_mb = os.path.getsize(file_path)/(1024*1024)
    st.markdown(f"**File size** : {size_mb:.2f} MB")
    st.markdown(f"**Total Records** : {len(df)}")
    st.markdown("**Data Retained** : 97.5%")
    
    
    st.divider()


    st.subheader("🎯Project Flow")
    st.write("*Data Ingestion → Cleaning → Transformation → Analysis → Visualization*")
    st.write("Designed using modular Python scripts to simulate a real-world ETL pipeline architecture.")
 
    st.divider()

    st.subheader("📔Total Metrics Created : 5")
    st.write("• **User Metrics** - Behavior patterns and activity levels")
    st.write("• **Endpoint Analysis** - Performance and error rates")
    st.write("• **Hourly Patterns** - Traffic distribution by hour")
    st.write("• **Daily Trends** - Traffic changes over time")
    st.write("• **HTTP Methods** - Request distribution by method")

    st.divider()

    st.subheader("🛠️ TechStack:")
    st.markdown("""
    - Python
    - NumPy
    - Pandas
    - Matplotlib
    - Streamlit
    """)
    

    st.write("")

    st.info("👈 Use the sidebar to navigate between different analysis sections")

#User Metrics
if page=="User Metrics":
    st.title("👥User Behaviour Analysis")
    
    #Summary metrics
    user_metrics=load_data("Data/Transformed/user_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total Users : ",f"{len(user_metrics):,}")
    with col2:
        avg_time=user_metrics['avg_response_time'].mean()
        st.metric("Avg Response Time",f"{avg_time:.2f}ms")
    with col3:
        avg_success=user_metrics['success_rate'].mean()
        st.metric("Avg Success Rate", f"{avg_success:.1f}%")
    
    #Text Report
    st.header("Text Report : ",divider=True)
    with st.expander("📄View Detailed Text Report"):
        report = load_report("Outputs/Reports/user_analysis.txt")
        st.text(report)
        
    st.divider()
    
    #Charts
    st.subheader("📈Charts")
    col1,col2=st.columns(2)
    with col1:
        st.image("Outputs/Charts/top_users.png",caption="Top 10 Most Active Users")
    with col2:
        st.image("Outputs/Charts/success_rate.png",caption="Success Rate Distribution")
        

#Enpoint Metrics
if page=="Endpoint Analysis":
    st.title("🔚Endpoint Analysis")
    
    #Summary metrics
    endpoint_metrics=load_data("Data/Transformed/endpoint_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total Endpoints : ",f"{len(endpoint_metrics):,}")
    with col2:
        avg_time=endpoint_metrics['avg_response_time'].mean()
        st.metric("Avg Response Time",f"{avg_time:.2f}ms")
    with col3:
        avg_success=endpoint_metrics['success_rate'].mean()
        st.metric("Avg Success Rate", f"{avg_success:.1f}%")
    
    #Text Report
    st.header("Text Report : ",divider=True)
    with st.expander("📄View Detailed Text Report"):
        report = load_report("Outputs/Reports/endpoint_analysis.txt")
        st.text(report)
        
    st.divider()
    
    #Charts
    st.subheader("📈Charts")
    col1,col2=st.columns(2)
    with col1:
        st.image("Outputs/Charts/slowest_endpoints.png",caption="Top 10 Slowest Endpoints")
    with col2:
        st.image("Outputs/Charts/avg_time_vs_success_rate.png",caption="Success Rate Distribution with Average Response Time")
    


