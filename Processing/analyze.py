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
    """
    Saves a text analysis report to the output directory.
    
    Combines report lines into a formatted text file.
    
    Args:
        output (list): List of report lines.
        filename (str): Name of the output text file.
    
    Returns:
        None: Writes the report to disk.
    """
    
    #Joining all lines and writing to file
    report="\n".join(output)
    filepath=f'Outputs/Reports/{filename}'
    with open(filepath,'w',encoding='utf-8') as f:
        f.write(report)

def analyze_user_metrics(user_metrics):
    """
    Generates a detailed user-level analysis report.
    
    Identifies active users, performance trends, bandwidth usage,
    and success rate insights.
    
    Args:
        user_metrics (pandas.DataFrame): User-level metrics dataset.
    
    Returns:
        None: Saves the user analysis report to file.
    """
    
    output=[]
    output.append("="*60)
    output.append("USER ANALYSIS\n".center(60))
    output.append("="*60)
    output.append("Source file : server_logs.csv")
    output.append(f"Total Users Analyzed: {len(user_metrics):,}")
    output.append("="*60)
    output.append("")#new line in txt file
    
    
    #finding most active users
    df1=user_metrics.nlargest(10,'total_requests')
    output.append("-"*60)
    output.append("📊TOP 10 MOST ACTIVE USERS")
    output.append("-"*60)
    output.append(df1[['user_id','total_requests']].to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    #finding users with worst success rate
    df2=user_metrics.nsmallest(10,'success_rate')
    output.append("-"*60)
    output.append("⚠️TOP 10 USERS WITH WORST SUCCESS RATES")
    output.append("-"*60)
    output.append(df2[['user_id','success_rate']].to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    #finding avg response time
    avg_res_time=user_metrics['avg_response_time'].mean()
    output.append("-"*60)
    output.append(f"⏱️The Average Response Time is {avg_res_time:.2f} ms")
    output.append("-"*60)
    output.append("")
    
    #finding users experiencing zero error
    tot_zero_error=(user_metrics['error_count']==0).sum()
    output.append("-"*60)
    output.append(f"👥The Number of users with 0 error are {tot_zero_error}")
    output.append("-"*60)
    output.append("")
    
    #users consuming most bandwidth
    df3=user_metrics.nlargest(10,'total_bytes')
    output.append("-"*60)
    output.append("💾TOP 10 BANDWIDTH CONSUMERS")
    output.append("-"*60)
    output.append(df3[['user_id','total_bytes']].to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    output.append("="*60)
    output.append("="*60)
    
    save_report(output,'user_analysis.txt')
        
def analyze_endpoint_metrics(endpoint_metrics):
    """
    Generates a detailed endpoint-level analysis report.
    
    Highlights traffic distribution, slow endpoints,
    bandwidth consumption, and error patterns.
    
    Args:
        endpoint_metrics (pandas.DataFrame): Endpoint-level metrics dataset.
    
    Returns:
        None: Saves the endpoint analysis report to file.
    """
    
    output=[]
    output.append("="*60)
    output.append("ENDPOINT ANALYSIS\n".center(60))
    output.append("="*60)
    output.append("Source file : server_logs.csv")
    output.append(f"Total Endpoints Analyzed: {len(endpoint_metrics):,}")
    output.append("="*60)
    output.append("")
    
    #finding slowest endpoints
    df1=endpoint_metrics.nlargest(5,'avg_response_time')
    output.append("-"*60)
    output.append("⏱️SLOWEST ENDPOINTS")
    output.append("-"*60)
    output.append(df1[['endpoint','avg_response_time']].to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    #finding endpoints with maximum error rates
    df2=endpoint_metrics.nlargest(5,"error_count")
    output.append("-"*60)
    output.append("⚠️ENDPOINTS WITH MAXIMUM ERROR COUNT")
    output.append("-"*60)
    output.append(df2[['endpoint','error_count']].to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    #finding total traffic distribution across endpoints
    df3 = endpoint_metrics[['endpoint', 'total_requests']].sort_values('total_requests', ascending=False)
    output.append("-"*60)
    output.append("📈TOTAL TRAFFIC DISTRIBUTION")
    output.append("-"*60)
    output.append(df3.to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    #finding endpoint which consumes most bandwidth
    max_idx=endpoint_metrics['total_bytes'].idxmax()
    max_bandwidth=endpoint_metrics.loc[max_idx,'total_bytes']
    max_bw_endpoint=endpoint_metrics.loc[max_idx,'endpoint']
    output.append("-"*120)
    output.append(f"📅The endpoint which consumes max_bandwidth is {max_bw_endpoint} consuming {max_bandwidth} bytes")
    output.append("-"*120)
    output.append("")
    
    #finding percentage of requests which go to API and STATIC files
    total_requests=endpoint_metrics['total_requests'].sum()
    
    total_api_requests=endpoint_metrics.loc[endpoint_metrics['endpoint'].str.contains('/api/', na=False), 'total_requests'].sum()
    total_static_requests=endpoint_metrics.loc[endpoint_metrics['endpoint'].str.contains('/static', na=False), 'total_requests'].sum()
    
    api_percent=((total_api_requests/total_requests)*100).round(2)
    static_percent=((total_static_requests/total_requests)*100).round(2)
    
    output.append("-"*60)
    output.append(f"📊Percentage API requests = {api_percent} %")
    output.append("")
    output.append(f"📊Percentage STATIC requests = {static_percent} %")
    output.append("-"*60)
    output.append("")
    
    output.append("="*60)
    output.append("="*60)
    
    save_report(output,'endpoint_analysis.txt')
        
def analyze_hourly_metrics(hourly_metrics):
    """
    Generates an hourly traffic and performance analysis report.
    
    Identifies peak hours, response time trends,
    success rates, and anomaly detection.
    
    Args:
        hourly_metrics (pandas.DataFrame): Hourly metrics dataset.
    
    Returns:
        None: Saves the hourly analysis report to file.
    """
    
    output=[]
    output.append("="*60)
    output.append("HOURLY ANALYSIS\n".center(60))
    output.append("="*60)
    output.append("Source file : server_logs.csv")
    output.append("="*60)
    output.append("")
    
    #finding the hour with most traffic
    max_idx=hourly_metrics['total_requests'].idxmax()
    max_hours=hourly_metrics.loc[max_idx,'total_requests']
    max_traffic_hour=hourly_metrics.loc[max_idx,'hour']
    output.append("-"*60)
    output.append(f"⏱️The Hour which has Maximum Traffic is {max_traffic_hour}:00 (24 hr format)")
    output.append("-"*60)
    output.append("")
    
    #finding peak on and peak off hours
    df1=hourly_metrics[hourly_metrics['total_requests']>=300]
    df2=hourly_metrics[hourly_metrics['total_requests']<300]
    output.append("-"*60)
    output.append("📈PEAK HOURS")
    output.append("-"*60)
    output.append(df1[['hour','total_requests']].to_string(index=False))
    output.append("")
    output.append("-"*60)
    output.append("📉OFF-PEAK HOURS")
    output.append("-"*60)
    output.append(df2[['hour','total_requests']].to_string(index=False))
    output.append("-"*60)
    output.append("")
    
    #finding max of average response time
    max_rsp_time=hourly_metrics['avg_response_time'].max()
    output.append("-"*60)
    output.append(f"⏱️The Maximum of Average Response Time is {(max_rsp_time/1000):.2f} seconds")
    output.append("-"*60)
    output.append("")
    
    #average success rate during peak hours and off-peak hours
    success_peak=(df1['success_rate'].mean()).round(2)
    success_peak_off=(df2['success_rate'].mean()).round(2)
    output.append("-"*60)
    output.append(f"📈Average Success Rate during Peak Hours is {success_peak} %")
    output.append(f"📈Average Success rate during Off-Peak Hours is {success_peak_off} %")
    output.append("-"*60)
    output.append("")
    
    #hour with unusually high error count
    error_sd=hourly_metrics['error_count'].std()
    df3=hourly_metrics[hourly_metrics['error_count']>=(2*error_sd)]
    output.append("-"*60)
    output.append(f"⚠️Hours with Unusally High Errors")
    output.append("-"*60)
    output.append(df3[['hour','error_count']].to_string(index=False)if not df3.empty else "No anomalies detected.")
    output.append("-"*60)
    output.append("")
    
    output.append("="*60)
    output.append("="*60)
    
    save_report(output,'hourly_analysis.txt')
        
def analyze_daily_metrics(daily_metrics):
    """
    Generates a daily traffic and performance analysis report.
    
    Identifies traffic trends, error patterns,
    best and worst days, and request volume insights.
    
    Args:
        daily_metrics (pandas.DataFrame): Daily metrics dataset.
    
    Returns:
        None: Saves the daily analysis report to file.
    """
    
    output=[]
    output.append("="*70)
    output.append("DAILY ANALYSIS\n".center(70))
    output.append("="*70)
    output.append("Source file : server_logs.csv")
    output.append("="*70)
    output.append("")
    
    #finding the day with most traffic
    max_idx=daily_metrics['total_requests'].idxmax()
    max_day_requests=daily_metrics.loc[max_idx,'total_requests']
    max_traffic_day=daily_metrics.loc[max_idx,'day']
    output.append("-"*70)
    output.append(f"📅The Day which has Maximum Traffic is DAY {max_traffic_day} with total requests = {max_day_requests}")
    output.append("-"*70)
    output.append("")
    
    #finding the day with most errors
    max_idx=daily_metrics['error_count'].idxmax()
    max_day_errors=daily_metrics.loc[max_idx,'error_count']
    max_error_day=daily_metrics.loc[max_idx,'day']
    output.append("-"*70)
    output.append(f"📅The Day which has Maximum Errors is DAY {max_error_day} with total errors = {max_day_errors}")
    output.append("-"*70)
    output.append("")
    
    #finding trend in traffic
    first_avg=daily_metrics['total_requests'].head(3).mean()
    last_avg=daily_metrics['total_requests'].tail(3).mean()
    
    percent_change=(((last_avg-first_avg)/first_avg)*100).round(2)
    if percent_change > 5:
        trend = "📈Increasing"
    elif percent_change < -5:
        trend = "📉Decreasing"
    else:
        trend = "—→Stable"
    output.append("-"*70)
    output.append(f"Traffic Trend: {trend} ({percent_change:+.2f}% CHANGE from Start to End of Month)")
    output.append("-"*70)
    output.append("")
    
    #best and worst day (in terms of success rate)
    max_idx=daily_metrics['success_rate'].idxmax()
    best_day_rate=daily_metrics.loc[max_idx,'success_rate']
    best_day=daily_metrics.loc[max_idx,'day']
    output.append("-"*70)
    output.append(f"📅The Best Day is DAY {best_day} with Success Rate = {best_day_rate} %")
    output.append("")
    
    min_idx=daily_metrics['success_rate'].idxmin()
    worst_day_rate=daily_metrics.loc[min_idx,'success_rate']
    worst_day=daily_metrics.loc[min_idx,'day']
    output.append(f"📅The Worst Day is DAY {worst_day} with Success Rate = {worst_day_rate} %")
    output.append("-"*70)
    output.append("")
    
    #finding average daily request value
    avg_requests=daily_metrics['total_requests'].mean().round()
    output.append("-"*70)
    output.append(f"📊The Average Request Volume is {avg_requests} Requests per DAY")
    output.append("-"*70)
    output.append("")
    
    output.append("="*70)
    output.append("="*70)
    
    save_report(output,'daily_analysis.txt')
        
        
def analyze_method_metrics(method_metrics):
    """
    Generates an HTTP method-level performance analysis report.
    
    Evaluates request distribution, response times,
    error patterns, and data sharing behavior across methods.
    
    Args:
        method_metrics (pandas.DataFrame): Method-level metrics dataset.
    
    Returns:
        None: Saves the method analysis report to file.
    """
    
    output=[]
    output.append("="*70)
    output.append("METHOD ANALYSIS\n".center(70))
    output.append("="*70)
    output.append("Source file : server_logs.csv")
    output.append(f"Total Methods Analyzed: {len(method_metrics):,}")
    output.append("="*70)
    output.append("")
    
    #finding the distribution among all HTTP methods
    tot_requests=method_metrics['total_requests'].sum()
    df1=method_metrics.assign(percent=((method_metrics['total_requests']/tot_requests)*100)).round(2)
    output.append("-"*70)
    output.append("📊PERCENTAGE DISTRIBUTION OF HTTP METHODS")
    output.append("-"*70)
    output.append(df1[['method', 'total_requests', 'percent']].to_string(index=False))
    output.append("-"*70)
    output.append("")
    
    #finding slowest method
    min_idx=method_metrics['avg_response_time'].idxmax()
    slowest_method_time=method_metrics.loc[min_idx,'avg_response_time']
    slowest_method=method_metrics.loc[min_idx,'method']
    output.append("-"*70)
    output.append(f"⏱️The Slowest Method is {slowest_method} with Average Response Time = {slowest_method_time:.2f} ms")
    output.append("-"*70)
    output.append("")
    
    #finding method with highest error rate
    max_idx=method_metrics['error_count'].idxmax()
    max_errors=method_metrics.loc[max_idx,'error_count']
    max_error_method=method_metrics.loc[max_idx,'method']
    output.append("-"*70)
    output.append(f"⚠️The Maximum Error Method is {max_error_method} with Error Count = {max_errors}")
    output.append("-"*70)
    output.append("")
    
    #finding the distribution of how much data each method shares
    tot_bytes=method_metrics['total_bytes_shared'].sum()
    df2=method_metrics.assign(percent=((method_metrics['total_bytes_shared']/tot_bytes)*100)).round(2)
    output.append("-"*70)
    output.append("📊DISTRIBUTION of DATA SHARED AMONG METHODS")
    output.append("-"*70)
    output.append(df2[['method', 'total_bytes_shared', 'percent']].to_string(index=False))
    output.append("-"*70)
    output.append("")
    
    #finding if POST methods are slower than GET methods
    temp_method_metrics=method_metrics.copy().set_index('method')
    post_time=(temp_method_metrics.loc['POST']['avg_response_time']).round(2)
    get_time=(temp_method_metrics.loc['GET']['avg_response_time']).round(2)
    result="Both are equal"
    
    if post_time<get_time:
        result="⏱️GET methods are slower"
    else:
        result="⏱️POST methods are slower"
    
    output.append("-"*70)
    output.append(f"Average response time of POST method is : {post_time} ms")
    output.append(f"Average response time of GET method is : {get_time} ms")
    output.append(f"CONCLUSION : {result}")
    output.append("-"*70)
    output.append("")
    
    output.append("="*70)
    output.append("="*70)
    
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
    
    print("\n" + "="*60)
    print("✓ ANALYSIS COMPLETE - All Reports Saved")
    print("="*60)
    
    
    
    