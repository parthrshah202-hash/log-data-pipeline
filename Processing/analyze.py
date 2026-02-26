import pandas as pd
import os

#creating output folder
os.makedirs('Outputs/Reports',exist_ok=True)

#reading all metrices
def load_metrics(filename):
    df=pd.read_csv(filename)
    return df

#function to save tet report
def save_report(output,filename):
    #Joining all lines and writing to file
    report="\n".join(output)
    filepath=f'Outputs/Reports/{filename}'
    with open(filepath,'w') as f:
        f.write(report)

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
    
    save_report(output,'user_analysis.txt')
        
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
    
    print(f"Percentage API requests = {api_percent} %")
    print(f"Percentage STATIC requests = {static_percent} %")
    print("\n")
    
    output.append(f"Percentage API requests = {api_percent} %")
    output.append("")
    output.append(f"Percentage STATIC requests = {static_percent} %")
    output.append("")
    
    save_report(output,'endpoint_analysis.txt')
        
def analyze_hourly_metrics(hourly_metrics):
    output=[]
    output.append("HOURLY METRICS\n")
    output.append("")
    
    #finding the hour with most traffic
    max_idx=hourly_metrics['total_requests'].idxmax()
    max_hours=hourly_metrics.loc[max_idx,'total_requests']
    max_traffic_hour=hourly_metrics.loc[max_idx,'hour']
    print(f"The hour which has maximum traffic is {max_traffic_hour}:00 (24 hr format) with total requests = {max_hours}")
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
    print("\n")
    output.append(f"Hours with unusally high errors are :- ")
    output.append(df3[['hour','error_count']].to_string(index=False)if not df3.empty else "No anomalies detected.")
    output.append("")
    
    save_report(output,'hourly_analysis.txt')
        
def analyze_daily_metrics(daily_metrics):
    output=[]
    output.append("DAILY METRICS\n")
    output.append("")
    
    #finding the day with most traffic
    max_idx=daily_metrics['total_requests'].idxmax()
    max_day_requests=daily_metrics.loc[max_idx,'total_requests']
    max_traffic_day=daily_metrics.loc[max_idx,'day']
    print(f"The day which has maximum traffic is day {max_traffic_day} with total requests = {max_day_requests}")
    print("\n")
    output.append(f"The day which has maximum traffic is day {max_traffic_day} with total requests = {max_day_requests}")
    output.append("")
    
    #finding the day with most errors
    max_idx=daily_metrics['error_count'].idxmax()
    max_day_errors=daily_metrics.loc[max_idx,'error_count']
    max_error_day=daily_metrics.loc[max_idx,'day']
    print(f"The day which has maximum errors is day {max_error_day} with total errors = {max_day_errors}")
    print("\n")
    output.append(f"The day which has maximum errors is day {max_error_day} with total errors = {max_day_errors}")
    output.append("")
    
    #finding trend in traffic
    first_avg=daily_metrics['total_requests'].head(3).mean()
    last_avg=daily_metrics['total_requests'].tail(3).mean()
    
    percent_change=(((last_avg-first_avg)/first_avg)*100).round(2)
    if percent_change > 5:
        trend = "Increasing"
    elif percent_change < -5:
        trend = "Decreasing"
    else:
        trend = "Stable"
    print(f"Traffic Trend: {trend} ({percent_change:+.2f}% change from start to end of month)")
    print("\n")
    output.append(f"Traffic Trend: {trend} ({percent_change:+.2f}% change from start to end of month)")
    output.append("")
    
    #best and worst day (in terms of success rate)
    max_idx=daily_metrics['success_rate'].idxmax()
    best_day_rate=daily_metrics.loc[max_idx,'success_rate']
    best_day=daily_metrics.loc[max_idx,'day']
    print(f"The best day is day {best_day} with success rate = {best_day_rate} %")
    print("\n")
    output.append(f"The best day is day {best_day} with success rate = {best_day_rate} %")
    output.append("")
    
    min_idx=daily_metrics['success_rate'].idxmin()
    worst_day_rate=daily_metrics.loc[min_idx,'success_rate']
    worst_day=daily_metrics.loc[min_idx,'day']
    print(f"The worst day is day {worst_day} with success rate = {worst_day_rate} %")
    print("\n")
    output.append(f"The worst day is day {worst_day} with success rate = {worst_day_rate} %")
    output.append("")
    
    #finding average daily request value
    avg_requests=daily_metrics['total_requests'].mean().round()
    print(f"The average request volume is {avg_requests} requests per day")
    output.append(f"The average request volume is {avg_requests} requests per day")
    output.append("")
    
    save_report(output,'daily_analysis.txt')
        
        
def analyze_method_metrics(method_metrics):
    output=[]
    output.append("METHOD METRICS")
    output.append("")
    
    #finding the distribution among all HTTP methods
    tot_requests=method_metrics['total_requests'].sum()
    df1=method_metrics.assign(percent=((method_metrics['total_requests']/tot_requests)*100)).round(2)
    print("The percentage distribution of HTTP method is as follows :- ")
    print(df1[['method', 'total_requests', 'percent']].to_string(index=False))
    print("\n")
    output.append("The percentage distribution of HTTP method is as follows :- ")
    output.append(df1[['method', 'total_requests', 'percent']].to_string(index=False))
    
    #finding slowest method
    min_idx=method_metrics['avg_response_time'].idxmin()
    slowest_method_time=method_metrics.loc[min_idx,'avg_response_time']
    slowest_method=method_metrics.loc[min_idx,'method']
    print(f"The slowest method is {slowest_method} with average response time = {slowest_method_time} ms")
    print("\n")
    output.append(f"The slowest method is {slowest_method} with average response time = {slowest_method_time} ms")
    output.append("")
    
    #finding method with highest error rate
    max_idx=method_metrics['error_count'].idxmax()
    max_errors=method_metrics.loc[max_idx,'error_count']
    max_error_method=method_metrics.loc[max_idx,'method']
    print(f"The maximum error method is {max_error_method} with error count = {max_errors}")
    print("\n")
    output.append(f"The maximum error method is {max_error_method} with error count = {max_errors}")
    output.append("")
    
    #finding the distribution of how much data each method shares
    tot_bytes=method_metrics['total_bytes_shared'].sum()
    df2=method_metrics.assign(percent=((method_metrics['total_bytes_shared']/tot_bytes)*100)).round(2)
    print("The percentage distribution of how much data each method shares is as follows :- ")
    print(df2[['method', 'total_bytes_shared', 'percent']].to_string(index=False))
    print("\n")
    output.append("The percentage distribution of how much data each method shares is as follows :- ")
    output.append(df2[['method', 'total_bytes_shared', 'percent']].to_string(index=False))
    output.append("")
    
    #finding if POST methods are slower than GET methods
    temp_method_metrics=method_metrics.copy().set_index('method')
    post_time=(temp_method_metrics.loc['POST']['avg_response_time']).round(2)
    get_time=(temp_method_metrics.loc['GET']['avg_response_time']).round(2)
    result="Both are equal"
    print(f"Average response time of POST method is : {post_time} ms")
    print(f"Average response time of GET method is : {get_time} ms")
    
    if post_time<get_time:
        result="GET methods are slower"
    else:
        result="POST methods are slower"
    print(f"CONCLUSION : {result}")
    print("\n")
    
    output.append(f"Average response time of POST method is : {post_time} ms")
    output.append(f"Average response time of GET method is : {get_time} ms")
    output.append(f"CONCLUSION : {result}")
    output.append("")
    
    save_report(output,'method_analysis.txt')

if __name__=="__main__":
    user_metrics=load_metrics("Data/Transformed/user_metrics.csv")
    analyze_user_metrics(user_metrics)
    
    endpoint_metrics=load_metrics("Data/Transformed/endpoint_metrics.csv")
    analyze_endpoint_metrics(endpoint_metrics)
    
    hourly_metrics=load_metrics("Data/Transformed/hourly_metrics.csv")
    analyze_hourly_metrics(hourly_metrics)
    
    daily_metrics=load_metrics("Data/Transformed/daily_metrics.csv")
    analyze_daily_metrics(daily_metrics)
    
    method_metrics=load_metrics("Data/Transformed/method_metrics.csv")
    analyze_method_metrics(method_metrics)
    
    