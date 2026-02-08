import numpy as np
import pandas as pd

#loading cleaned data
def load_data(filepath):
    df=pd.read_csv(filepath)
    print("Data Loaded")
    return df

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
    error_df=df[df['status_code']!=200].groupby('user_id').size()
    error_df=error_df.reset_index(name='error_count')
    
    #Merging & Cleaning
    user_metrics=user_metrics.merge(error_df,on='user_id',how='left')
    user_metrics['error_count']=user_metrics['error_count'].fillna(0)
    
    #Calculation
    user_metrics['success_rate']=((user_metrics['total_requests'] - user_metrics['error_count']) / user_metrics['total_requests'] * 100).round(2)
    
    #Summary
    print(f"Total User : {len(user_metrics)}")
    print(user_metrics.head(10))
    
    return user_metrics

#creating end-point metrics
def create_endpoint_metrics(df):
    endpoint_metrics=df.groupby('endpoint').agg({
        'response_time_ms':'mean',
        'status_code':'count',
        'bytes_sent':'sum'
    }).reset_index()
    endpoint_metrics.columns=['endpoint','avg_response_time','total_requests','total_bytes']
    
    
    #Finding Error Rate
    error_df=df[df['status_code']!=200].groupby('endpoint').size().reset_index(name='error_count')
    
    #Merging and Cleaning
    endpoint_metrics=endpoint_metrics.merge(error_df,on='endpoint',how='left')
    endpoint_metrics['error_count']=endpoint_metrics['error_count'].fillna(0)
    
    #Calculation
    endpoint_metrics['error_rate']=(endpoint_metrics['error_count']/endpoint_metrics['total_requests']*100).round(2)
      
      
    #Summary
    print(f"Total Endpoints : {len(endpoint_metrics)}")
    print(endpoint_metrics.head(10))
    
    return endpoint_metrics
    
    


if __name__=="__main__":
    df=pd.read_csv('Data/CLEANED/cleaned_server_logs.csv')
    
    user_metrics=create_user_metrics(df)
    user_metrics.to_csv('Data/Transformed/user_metrics.csv')
    
    endpont_metrics=create_endpoint_metrics(df)
    endpont_metrics.to_csv('Data/Transformed/endpoint_metrics.csv')
    
    
    
    
    