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
    """
    Loads a pre-generated text analysis report.
    
    Reads a UTF-8 encoded report file for display
    within the Streamlit dashboard.
    
    Args:
        filename (str): Path to the text report file.
    
    Returns:
        str: Report content as a string.
    """
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
    
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("**Raw file**" , "server_logs.csv")
    with col2:
        st.metric("**Date Created**" , "1 Feb 2026")
    with col3:
        size_mb = os.path.getsize(file_path)/(1024*1024)
        st.metric(f"**File size** ", f"{size_mb:.2f} MB")
    with col4:
        st.metric(f"**Total Records** ",f"{len(df):,}")
    
    
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
    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown("### ⚙️ Engine")
        st.write("• Python")
        st.write("• NumPy")
        st.write("• Pandas")
    with col2:
        st.markdown("### 📊 Visuals")
        st.write("• Matplotlib")
    with col3:
        st.markdown("### 🌐 UI")
        st.write("• Streamlit")
    

    st.write("")

    st.info("👈 Use the sidebar to navigate between different analysis sections")

#User Metrics
if page=="User Metrics":
    st.title("👥User Behaviour Analysis")
    
    #Summary metrics
    user_metrics=load_data("Data/Transformed/user_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total Users",f"{len(user_metrics):,}")
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
        

#Endpoint Metrics
if page=="Endpoint Analysis":
    st.title("🔚Endpoint Analysis")
    
    #Summary metrics
    endpoint_metrics=load_data("Data/Transformed/endpoint_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total Endpoints",f"{len(endpoint_metrics):,}")
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
        
#Hourly Patterns
if page=="Hourly Patterns":
    st.title("⏱️Hourly Patterns")
    
    #Summary metrics
    hourly_metrics=load_data("Data/Transformed/hourly_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        max_idx=hourly_metrics['total_requests'].idxmax()
        max_traffic_hour=hourly_metrics.loc[max_idx,'hour']
        st.metric("Busiest Hour",f"{max_traffic_hour}:00")
    with col2:
        avg_time=hourly_metrics['avg_response_time'].mean()
        st.metric("Avg Response Time",f"{avg_time:.2f}ms")
    with col3:
        avg_success=hourly_metrics['success_rate'].mean()
        st.metric("Avg Success Rate", f"{avg_success:.1f}%")
    
    #Text Report
    st.header("Text Report : ",divider=True)
    with st.expander("📄View Detailed Text Report"):
        report = load_report("Outputs/Reports/hourly_analysis.txt")
        st.text(report)
        
    st.divider()
    
    #Charts
    st.subheader("📈Charts")
    col1,col2=st.columns(2)
    with col1:
        st.image("Outputs/Charts/hourly_traffic_pattern.png",caption="Hourly Traffic Pattern")
    with col2:
        st.image("Outputs/Charts/tot_requests and success_rate.png",caption="Success Rate Distribution with Total Requests")
    
    
#Daily Trends
if page=="Daily Trends":
    st.title("🗓️Daily Trends")
    
    #Summary metrics
    daily_metrics=load_data("Data/Transformed/daily_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        max_idx=daily_metrics['total_requests'].idxmax()
        max_traffic_day=daily_metrics.loc[max_idx,'day']
        st.metric("Busiest Day",f"{max_traffic_day}")
    with col2:
        max_idx=daily_metrics['error_count'].idxmax()
        max_error_day=daily_metrics.loc[max_idx,'day']
        st.metric("Worst Day",f"{max_error_day}")
    with col3:
        avg_success=daily_metrics['success_rate'].mean()
        st.metric("Avg Success Rate", f"{avg_success:.1f}%")
    
    #Text Report
    st.header("Text Report : ",divider=True)
    with st.expander("📄View Detailed Text Report"):
        report = load_report("Outputs/Reports/daily_analysis.txt")
        st.text(report)
        
    st.divider()
    
    #Charts
    st.subheader("📈Charts")
    st.image("Outputs/Charts/Daily Trend with Errors.png",caption="Daily Error Trend")


#HTTP Methods
if page=="HTTP Methods":
    st.title("🔀HTTP Methods")
    
    #Summary metrics
    method_metrics=load_data("Data/Transformed/method_metrics.csv")
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric("Total Methods",f"{len(method_metrics):,}")
    with col2:
        min_idx=method_metrics['avg_response_time'].idxmax()
        slowest_method=method_metrics.loc[min_idx,'method']
        st.metric("Slowest Method",f"{slowest_method}")
    with col3:
        min_idx=method_metrics['error_count'].idxmin()
        min_error_method=method_metrics.loc[min_idx,'method']
        st.metric("Best Method", f"{min_error_method}")
    
    #Text Report
    st.header("Text Report : ",divider=True)
    with st.expander("📄View Detailed Text Report"):
        report = load_report("Outputs/Reports/method_analysis.txt")
        st.text(report)
        
    st.divider()
    
    #Charts
    st.subheader("📈Charts")
    col1,col2=st.columns(2)
    with col1:
        st.image("Outputs/Charts/Method Distribution.png",caption="Distribution of Methods")
    with col2:
        st.image("Outputs/Charts/Method_Success_vs_Error_Count.png",caption="Error Count among Methods")