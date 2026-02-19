import pandas as pd
import os

#creating output folder
os.makedirs('Outputs/Reports',exist_ok=True)

#reading all metrices
def load_metrics(filename):
    df=pd.read_csv(filename)
    return df

def analyze_user_metrics(user_metrics):
    output=[]
    output.append("USER ANALYSIS\n")
    output.append("")#new line in txt file
    
    #finding most active users
    df1=user_metrics.nlargest(10,'total_requests')
    print("The top active users are : ")
    print(df1[['user_id','total_requests']].to_string(index=False))
    print("\n")
    output.append("Top 10 Most Active Users : ")
    output.append(df1[['user_id','total_requests']].to_string(index=False))
    output.append("")
    
    #finding users with worst success rate
    df2=user_metrics.nsmallest(10,'success_rate')
    print("The top 10 users with worst success rate are : ")
    print(df2[['user_id','success_rate']].to_string(index=False))
    print("\n")
    output.append("Top 10 Users Having Worst Success Rate")
    output.append(df2[['user_id','success_rate']].to_string(index=False))
    output.append("")
    
    #finding avg response time
    avg_res_time=user_metrics['avg_response_time'].mean()
    print(f"The average response time is : {avg_res_time} ms")
    print("\n")
    output.append(f"The Average Response Time is {avg_res_time} ms")
    output.append("")
    
    #users consuming most bandwidth
    df3=user_metrics.nlargest(10,'total_bytes')
    print("The top 10 users according to bandwidth consumption are : ")
    print(df3[['user_id','total_bytes']].to_string(index=False))
    print("\n")
    output.append("Top 10 Users Consuming Maximum Bandwidth : ")
    output.append(df3[['user_id','total_bytes']].to_string(index=False))
    output.append("")
    
    #finding users experiencing zero error
    tot_zero_error=(user_metrics['error_count']==0).sum()
    print(f"Total users with zero errors are : {tot_zero_error}")
    print("\n")
    output.append(f"The Number of users with 0 error are {tot_zero_error}")
    output.append("")
    
    #Joinning all lines and writing to file
    report="\n".join(output)
    with open('Outputs/Reports/user_analysis.txt','w') as f:
        f.write(report)
        
def analyze_endpoint_metrics(endpoint_metrics):
    output=[]
    output.append("ENDPOINT METRICS\n")
    output.append("")
    
    #finding slowest endpoints
    df1=endpoint_metrics.nlargest(5,'avg_response_time')
    print("The slowest end-points are :-")
    print(df1[['endpoint','avg_response_time']].to_string(index=False))
    print("\n")
    output.append("The top 5 slowest endpoints are : ")
    output.append(df1[['endpoint','avg_response_time']].to_string(index=False))
    output.append("")
    
    #finding endpoints with maximum error rates
    df2=endpoint_metrics.nlargest(5,"error_count")
    print("The endpoints with maximum error rates are :- ")
    print(df2[['endpoint','error_count']].to_string(index=False))
    print("\n")
    output.append("The top 5 endpoints with maximum error count are :- ")
    output.append(df2[['endpoint','error_count']].to_string(index=False))
    output.append("")
    
    #finding total traffic distribution across endpoints
    df3 = endpoint_metrics[['endpoint', 'total_requests']].sort_values('total_requests', ascending=False)
    print(df3.to_string(index=False))
    output.append(df3.to_string(index=False))
    output.append("")
    
    #finding endpoint which consumes most bandwidth
    max_idx=endpoint_metrics['total_bytes'].idxmax()
    max_bandwidth=endpoint_metrics.loc[max_idx,'total_bytes']
    max_bw_endpoint=endpoint_metrics.loc[max_idx,'endpoint']
    print(f"The endpoint which consumes max_bandwidth is {max_bw_endpoint} consuming {max_bandwidth}")
    print("\n")
    output.append(f"The endpoint which consumes max_bandwidth is {max_bw_endpoint} consuming {max_bandwidth} bytes")
    output.append("")
    
    #finding percentage of requests which go to API and STATIC files
    total_requests=endpoint_metrics['total_requests'].sum()
    
    total_api_requests=endpoint_metrics.loc[endpoint_metrics['endpoint'].str.contains('/api/', na=False), 'total_requests'].sum()
    total_static_requests=endpoint_metrics.loc[endpoint_metrics['endpoint'].str.contains('/static', na=False), 'total_requests'].sum()
    
    api_percent=((total_api_requests/total_requests)*100).round(2)
    static_percent=((total_static_requests/total_requests)*100).round(2)
    
    print(f"Percentage API requets = {api_percent} %")
    print(f"Percentage STATIC requets = {static_percent} %")
    print("\n")
    
    output.append(f"Percentage API requets = {api_percent} %")
    output.append("")
    output.append(f"Percentage STATIC requets = {static_percent} %")
    output.append("")
    
    #Joining all lines and writing to file
    report="\n".join(output)
    with open('Outputs/Reports/endpoint_analysis.txt','w') as f:
        f.write(report)
        
def analyze_hourly_metrics(hourly_metrics):
    output=[]
    output.append("HOURLY METRICS\n")
    output.append("")
    
    #finding the hour with most traffic
    max_idx=hourly_metrics['total_requests'].idxmax()
    max_hours=hourly_metrics.loc[max_idx,'total_requests']
    max_traffic_hour=hourly_metrics.loc[max_idx,'hour']
    print(f"The hour which has maximum traffic is {max_traffic_hour}:00 (24 hr format)")
    print("\n")
    output.append(f"The hour which has maximum traffic is {max_traffic_hour}:00 (24 hr format)")
    output.append("")
    
    #finding peak on and peak off hours
    df1=hourly_metrics[hourly_metrics['total_requests']>=300]
    print("Peak hours are :- ")
    print(df1[['hour','total_requests']].to_string(index=False))
    print("\n")
    df2=hourly_metrics[hourly_metrics['total_requests']<300]
    print("Peak-off hours are :- ")
    print(df2[['hour','total_requests']].to_string(index=False))
    print("\n")
    output.append("Peak hours are :- ")
    output.append(df1[['hour','total_requests']].to_string(index=False))
    output.append("")
    output.append("Peak-off hours are :- ")
    output.append(df2[['hour','total_requests']].to_string(index=False))
    output.append("")
    
    #finding max of average response time
    max_rsp_time=hourly_metrics['avg_response_time'].max()
    print(f"The maximum of average response time is {max_rsp_time/1000} seconds")
    print("\n")
    output.append(f"The maximum of average response time is {max_rsp_time/1000} seconds")
    output.append("")
    
    #average success rate during peak hours and off-peak hours
    success_peak=(df1['success_rate'].mean()).round(2)
    success_peak_off=(df2['success_rate'].mean()).round(2)
    print(f"Average Success rate during peak hours is {success_peak} %")
    print("\n")
    print(f"Average Success rate during peak_off hours is {success_peak_off} %")
    print("\n")
    output.append(f"Average Success rate during peak hours is {success_peak} %")
    output.append(f"Average Success rate during peak-off hours is {success_peak_off} %")
    output.append("")
    
    #hour with unusually high error count
    error_sd=hourly_metrics['error_count'].std()
    df3=hourly_metrics[hourly_metrics['error_count']>=(2*error_sd)]
    print("Hours with unusally high errors are :- ")
    print(df3[['hour','error_count']].to_string(index=False))
    output.append(f"Hours with unusally high errors are :- ")
    output.append(df3[['hour','error_count']].to_string(index=False)if not df3.empty else "No anomalies detected.")
    output.append("")
    
    #Joining all lines and writing to file
    report="\n".join(output)
    with open('Outputs/Reports/hourly_analysis.txt','w') as f:
        f.write(report)
    
    

if __name__=="__main__":
    user_metrics=load_metrics("Data/Transformed/user_metrics.csv")
    analyze_user_metrics(user_metrics)
    
    endpoint_metrics=load_metrics("Data/Transformed/endpoint_metrics.csv")
    analyze_endpoint_metrics(endpoint_metrics)
    
    hourly_metrics=load_metrics("Data/Transformed/hourly_metrics.csv")
    analyze_hourly_metrics(hourly_metrics)
    
    