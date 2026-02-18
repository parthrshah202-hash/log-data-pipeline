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
    
    output.append(f"Percentage API requets = {api_percent} %")
    output.append("")
    output.append(f"Percentage STATIC requets = {static_percent} %")
    output.append("")
    
    #Joining all lines and writing to file
    report="\n".join(output)
    with open('Outputs/Reports/endpoint_analysis.txt','w') as f:
        f.write(report)

if __name__=="__main__":
    user_metrics=load_metrics("Data/Transformed/user_metrics.csv")
    analyze_user_metrics(user_metrics)
    
    endpoint_metrics=load_metrics("Data/Transformed/endpoint_metrics.csv")
    analyze_endpoint_metrics(endpoint_metrics)
    
    