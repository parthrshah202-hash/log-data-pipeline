import numpy as np
import pandas as pd

#loading cleaned data
def load_data(filepath):
    df=pd.read_csv(filepath)
    print("Data Loaded")
    return df

#helper function to calculate error and success
def add_error_success_metrics(df, metrics, group_column):
    
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
    user_metrics.to_csv('Data/Transformed/user_metrics.csv',index=False)
    
    endpoint_metrics=create_endpoint_metrics(df)
    endpoint_metrics.to_csv('Data/Transformed/endpoint_metrics.csv',index=False)
    
    hourly_metrics=create_hourly_metrics(df)
    hourly_metrics.to_csv('Data/Transformed/hourly_metrics.csv',index=False)
    
    daily_metrics=create_daily_metrics(df)
    daily_metrics.to_csv('Data/Transformed/daily_metrics.csv',index=False)
    
    method_metrics=create_method_metrics(df)
    method_metrics.to_csv('Data/Transformed/method_metrics.csv',index=False)
    
    print("All Metrics Created!!")
    
    
    
    
    