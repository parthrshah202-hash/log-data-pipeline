import sys
import numpy as np
import pandas as pd

#<Loading a file>
def load_data(filepath):
    df=pd.read_csv(filepath)
    print("File read")
    print(df.head())
    return df



#<Validating Data>
def validate_data(df):
    print("The Nature of Data is:")
    print(df.describe())
    df.info()
    print("The size of dataset is:")
    print(df.size)
    n=df.isnull().sum().sum()
    if n>0:
        print(f"We have {n} null values")
    m=df.duplicated().sum()
    if m>0:
        print(f"We have {m} duplicate values")
    
    


#<Cleaning Data>
def clean_data(df):
    df=df.drop_duplicates()
    df=df.fillna("Anonymus")
    print("Data Cleaned")
    return df


#<Main Function>
if __name__ == "__main__":
    df=load_data('Data/RAW/server_logs.csv')
    validate_data(df)
    df=clean_data(df)
    df.to_csv('Data/CLEANED/cleaned_server_logs.csv',index=None)
    
