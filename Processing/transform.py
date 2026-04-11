import numpy as np
import pandas as pd
import logging

logging.basicConfig(filename="logs/log_test.log",format='%(asctime)s %(levelname)s: %(message)s',filemode='a')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

#loading cleaned data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        logger.info(f"File loaded: {filepath}")
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        exit(1)
    
    return df

def save_metrics(df,filepath):
    try:
        df.to_csv(filepath, index=False)
        logger.info(f"Saved: {filepath}")
    except FileNotFoundError:
        logger.error(f"Directory does not exist for: {filepath}")
        exit(1)
    

#helper function to calculate error and success
def add_error_success_metrics(df, metrics, group_column):
    """
    Adds error count and success rate metrics to a grouped dataset.
    
    Calculates failed requests and computes success percentage for each group.
    
    Args:
        df (pandas.DataFrame): Original dataset containing status codes.
        metrics (pandas.DataFrame): Grouped metrics dataset.
        group_column (str): Column name used for grouping.
    
    Returns:
        pandas.DataFrame: Updated metrics with error count and success rate.
    """
    
    #create error column
    error_df=df[df['status_code']!=200].groupby(group_column).size().reset_index(name='error_count')
    
    #merging and cleaning
    metrics=metrics.merge(error_df,on=group_column,how='left')
    metrics['error_count']=metrics['error_count'].fillna(0)
    
    #calculate success rate
    metrics['success_rate']=((metrics['total_requests']-metrics['error_count'])/metrics['total_requests']*100).round(2)
    
    return metrics
    

#creating user metrics
def create_user_metrics(df):
    """
    Generates aggregated performance metrics for each user.
    
    Computes average response time, total requests, total bytes, and success rate per user.
    
    Args:
        df (pandas.DataFrame): Cleaned dataset.
    
    Returns:
        pandas.DataFrame: User-level metrics dataset.
    """
    
    #finding average response time, total user requests and bytes sent using agg()
    user_metrics=df.groupby('user_id').agg({
        'response_time_ms':'mean',
        'status_code':'count',
        'bytes_sent':'sum'
    }).reset_index()
    user_metrics.columns=['user_id','avg_response_time','total_requests','total_bytes']
    
    #Finding success rate
    user_metrics=add_error_success_metrics(df,user_metrics,'user_id')
    
    
    return user_metrics

#creating end-point metrics
def create_endpoint_metrics(df):
    """
    Generates aggregated performance metrics for each endpoint.
    
    Computes average response time, total requests, total bytes, and success rate per endpoint.
    
    Args:
        df (pandas.DataFrame): Cleaned dataset.
    
    Returns:
        pandas.DataFrame: Endpoint-level metrics dataset.
    """
    
    endpoint_metrics=df.groupby('endpoint').agg({
        'response_time_ms':'mean',
        'status_code':'count',
        'bytes_sent':'sum'
    }).reset_index()
    endpoint_metrics.columns=['endpoint','avg_response_time','total_requests','total_bytes']
    
    #Finding Success rate
    endpoint_metrics=add_error_success_metrics(df,endpoint_metrics,'endpoint')
    
    
    return endpoint_metrics
    
    
#creating hourly metrics
def create_hourly_metrics(df):
    """
    Generates aggregated performance metrics grouped by hour.
    
    Computes hourly average response time, total requests, and success rate.
    
    Args:
        df (pandas.DataFrame): Cleaned dataset.
    
    Returns:
        pandas.DataFrame: Hourly metrics dataset.
    """
    
    df = df.copy()
    df['hour']=pd.to_datetime(df['timestamp'],dayfirst=True).dt.hour
    
    #grouping
    hourly_metrics=df.groupby('hour').agg({
        'response_time_ms':'mean',
        'status_code':'count',
    }).reset_index()
    hourly_metrics.columns=['hour','avg_response_time','total_requests']
    
    #Finding Success rate
    hourly_metrics=add_error_success_metrics(df,hourly_metrics,'hour')
    
    
    return hourly_metrics

#creating daily metrics
def create_daily_metrics(df):
    """
    Generates aggregated performance metrics grouped by day.
    
    Computes daily average response time, total requests, and success rate.
    
    Args:
        df (pandas.DataFrame): Cleaned dataset.
    
    Returns:
        pandas.DataFrame: Daily metrics dataset.
    """
    
    df = df.copy()
    df['day']=pd.to_datetime(df['timestamp'],dayfirst=True).dt.day
    
    #grouping
    daily_metrics=df.groupby('day').agg({
        'response_time_ms':'mean',
        'status_code':'count',
    }).reset_index()
    daily_metrics.columns=['day','avg_response_time','total_requests']
    
    #Finding Success rate
    daily_metrics=add_error_success_metrics(df,daily_metrics,'day')
    
    
    return daily_metrics
    
#creating method metrics
def create_method_metrics(df):
    """
    Generates aggregated performance metrics for each HTTP method.
    
    Computes average response time, request count, total and average bytes shared, and success rate.
    
    Args:
        df (pandas.DataFrame): Cleaned dataset.
    
    Returns:
        pandas.DataFrame: Method-level metrics dataset.
    """
    
    #grouping
    method_metrics=df.groupby('method').agg({
        'response_time_ms':'mean',
        'status_code':'count',
        'bytes_sent':['sum','mean']
    }).reset_index()
    method_metrics.columns=['method','avg_response_time','total_requests','total_bytes_shared','avg_bytes']
    
    #Finding Success rate
    method_metrics=add_error_success_metrics(df,method_metrics,'method')
    
    
    return method_metrics
    
    
    

if __name__=="__main__":
    df=load_data('Data/CLEANED/cleaned_server_logs.csv')
    
    user_metrics=create_user_metrics(df)
    save_metrics(user_metrics,'Data/Transformed/user_metrics.csv')
    
    
    endpoint_metrics=create_endpoint_metrics(df)
    save_metrics(endpoint_metrics,'Data/Transformed/endpoint_metrics.csv')
    
    hourly_metrics=create_hourly_metrics(df)
    save_metrics(hourly_metrics,'Data/Transformed/hourly_metrics.csv')
   
    
    daily_metrics=create_daily_metrics(df)
    save_metrics(daily_metrics,'Data/Transformed/daily_metrics.csv')
    
    
    method_metrics=create_method_metrics(df)
    save_metrics(method_metrics,'Data/Transformed/method_metrics.csv')
    
    
    logger.info("="*60)
    logger.info("✓ All Metrics Created!!")
    logger.info("="*60)
    
    
    
    
    