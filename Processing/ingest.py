import sys
import numpy as np
import pandas as pd

#<Loading a file>
def load_data(filepath):
    #using filepath so that i can reuse this function
    df=pd.read_csv(filepath)
    print("File read")
    print(df.head())
    return df



#<Validating Data>
def validate_data(df):
    
    #Basic sturcture of data
    print("The Nature of Data is:")
    print(df.describe())
    df.info()
    print("The size of dataset is:")
    print(df.size)
    
    #Duplicate values
    m=df.duplicated().sum()
    if m>0:
        print(f"We have {m} duplicate values")
    
    #Empty Values
    print(f"We have {df['user_id'].isnull().sum()} empty user_ids")
    print(f"We have {df['ip_address'].isnull().sum()} empty uip_address")
    print(f"We have {df['endpoint'].isnull().sum()} empty endpoints")
    print(f"We have {df['method'].isnull().sum()} empty methods")
    print(f"We have {df['status_code'].isnull().sum()} empty status codes")
    print(f"We have {df['bytes_sent'].isnull().sum()} empty bytes_sents")
    print(f"We have {df['response_time_ms'].isnull().sum()} empty response times")
    print(f"We have {df['user_agent'].isnull().sum()} empty user agents")
    
    #negative response time values-->invalid
    n=(df['response_time_ms']<0).sum()
    print(f"We have {n} negative response times")
    
    m=(df['bytes_sent']>(10**6)).sum()
    print(f"We have {m} megabytes shared")
    


#<Cleaning Data>
def clean_data(df):
    #Filling the missing data with appropriate values
    df['user_id']=df['user_id'].fillna("Anonymous")
    df['endpoint']=df['endpoint'].fillna("Unknown")
    df['method']=df['method'].fillna("Unknown")
    df['bytes_sent']=df['bytes_sent'].fillna(0)
    df['user_agent']=df['user_agent'].fillna("Unknown")
    
    #Droping the rows which are empty as we cannot use it in analysis
    df = df.dropna(subset=['ip_address'])
    df = df.dropna(subset=['status_code'])
    df = df.dropna(subset=['response_time_ms'])
    
    #Droping the duplicates
    df = df.drop_duplicates()
    
    #Droping rows with negative response time
    df = df[df['response_time_ms'] >= 0]
    
    #Droping rows with data shared more than 1MB
    df = df[df['bytes_sent'] < (10**6)]
    
    print("Data Cleaned")
    print(df.size)
    print(df.head())
    return df


#<Main Function>
if __name__ == "__main__":
    df=load_data('Data/RAW/server_logs.csv')
    validate_data(df)
    df=clean_data(df)
    df.to_csv('Data/CLEANED/cleaned_server_logs.csv',index=None)
    
