import sys
import numpy as np
import pandas as pd
from pprint import pprint

#<Loading a file>
def load_data(filepath):
    """
    Loads a CSV file and returns it as a pandas DataFrame.
    
    Reads log data from the given file path for further processing.
    
    Args:
        filepath (str): Path to the CSV file.
    
    Returns:
        pandas.DataFrame: Loaded dataset.
    """
    #using filepath so that i can reuse this function
    try:
        df=pd.read_csv(filepath)
        print("File read")
    except FileNotFoundError:
        print("Error 404 : File Not Found !")
        exit(1)
        
    return df



#<Validating Data>
def validate_data(df):
    """
    Generates a validation summary of the dataset.
    
    Computes dataset size, duplicate rows, missing values, and basic data quality metrics.
    
    Args:
        df (pandas.DataFrame): Input dataset to validate.
    
    Returns:
        dict: Dictionary containing validation statistics.
    """
    report={}

    report["dataset_size"]=df.size
    report["duplicate_rows"]=df.duplicated().sum()
    report["missing_values"]=df.isnull().sum().to_dict()
    report["negative_response_time"]=(df['response_time_ms']<0).sum()
    report["large_bytes_sent"]=(df['bytes_sent']>10**6).sum()

    return report
    


#<Cleaning Data>
def clean_data(df):
    """
    Cleans the dataset by handling missing and invalid values.
    
    Removes duplicates and filters out unrealistic or incomplete records.
    
    Args:
        df (pandas.DataFrame): Raw dataset to clean.
    
    Returns:
        pandas.DataFrame: Cleaned dataset ready for analysis.
    """
    
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
    print("The size of Cleaned Dataset is:")
    print(df.size)
    return df


#<Main Function>
if __name__ == "__main__":
    df=load_data('Data/RAW/server_logs.csv')
    
    report = validate_data(df)
    print("Validation Report:")
    pprint(report)
    
    df=clean_data(df)
    
    filepath='Data/CLEANED/cleaned_server_logs.csv'
    try:
        df.to_csv(filepath, index=False)
        print(f"Saved: {filepath}")
    except FileNotFoundError:
        print(f"Directory does not exist for: {filepath}")
    exit(1)
    
