import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')

def save_chart(filename):
    """
    Saves the current matplotlib figure to the charts directory.
    
    Stores the generated visualization as a high-resolution image file.
    
    Args:
        filename (str): Name of the image file to save.
    
    Returns:
        None: Writes the chart image to disk.
    """
    
    filepath=f'Outputs/Charts/{filename}'
    plt.savefig(filepath,dpi=300,bbox_inches='tight')
    plt.close()

#Visualizing for user_metrics
def visualize_user_metrics(user_metrics) :
    """
    Generates visualizations for user-level performance metrics.
    
    Creates charts highlighting most active users and
    success rate distribution.
    
    Args:
        user_metrics (pandas.DataFrame): User-level metrics dataset.
    
    Returns:
        None: Saves generated charts to file.
    """
    
    #Making a Horizontal bar chart for the top 10 most active users
    df1=user_metrics.nlargest(10,'total_requests')
    x_axis=df1['total_requests']
    y_axis=df1['user_id']

    plt.barh(y_axis,x_axis,height=0.2,alpha=0.75,color='#2E86AB')
    plt.gca().invert_yaxis()
    plt.grid(axis='x',linestyle='--')

    plt.title("Top 10 most active users")
    plt.xlabel("Number of requests")
    plt.ylabel("User_IDs")
    plt.tight_layout()
    #plt.show()

    save_chart('top_users.png')
    
    #Making a histogram for success rate distribution
    success_rate=user_metrics['success_rate']
    bins=[0,10,20,30,40,50,60,70,80,90,100]

    plt.hist(success_rate,bins,color='#008000',edgecolor='#000000',alpha=0.75)
    plt.title("Success Rate Distribution")
    plt.ylabel("Users")
    plt.xlabel("Success Percentage")
    plt.tight_layout()
    #plt.show()

    save_chart('success_rate.png')

#Visualizing for endpoint_metrics
def visualize_endpoint_metrics(endpoint_metrics):
    """
    Generates visualizations for endpoint-level performance metrics.
    
    Creates charts showing response time trends,
    success rate relationship, and slowest endpoints.
    
    Args:
        endpoint_metrics (pandas.DataFrame): Endpoint-level metrics dataset.
    
    Returns:
        None: Saves generated charts to file.
    """
    
    #Making a scatter plot for response time V/S success rate
    x_axis=endpoint_metrics['avg_response_time']
    y_axis=endpoint_metrics['success_rate']
    
    plt.scatter(x_axis,y_axis,edgecolor='#000000',alpha=0.75)
    
    plt.title('Avg Response Time V/S Success Rate')
    plt.xlabel('Avg. Response Time(ms)')
    plt.ylabel('Success Rate(%)')
    plt.tight_layout()
    #plt.show()
    
    save_chart('avg_time_vs_success_rate.png')
    
    #Making a horizontal bar graph to show the slowest endpoints
    df1=endpoint_metrics.nlargest(10,'avg_response_time')
    x_axis=df1['avg_response_time']
    y_axis=df1['endpoint']

    plt.barh(y_axis,x_axis,height=0.5,alpha=0.75,color="#B81FE7")
    plt.gca().invert_yaxis()
    plt.grid(axis='x',linestyle='--')

    plt.title("Top 10 Slowest Endpoints")
    plt.xlabel("Avg Response Time(ms)")
    plt.ylabel("Endpoint")
    plt.tight_layout()
    #plt.show()
    
    save_chart('slowest_endpoints.png')
    
#Visualizing for hourly metrics
def visualize_hourly_metrics(hourly_metrics):
    """
    Generates visualizations for hourly traffic and performance metrics.
    
    Creates charts showing traffic patterns,
    success rate trends, and peak thresholds.
    
    Args:
        hourly_metrics (pandas.DataFrame): Hourly metrics dataset.
    
    Returns:
        None: Saves generated charts to file.
    """
    
    #Making line chart to show traffic pattern by hour
    plt.figure(figsize=(12,6))
    x_axis=hourly_metrics['hour']
    y_axis=hourly_metrics['total_requests']
    
    plt.plot(x_axis,y_axis,color="#52E626",linewidth='3',marker='o')
    plt.grid(True)
    plt.fill_between(x_axis, y_axis, alpha=0.3, color='#00FFFF', label='Traffic Volume')
    plt.axhline(y=300, color='#FF0000', linestyle='--',linewidth='2.0', label='Peak Threshold (300)')
    plt.legend(loc='upper left')
    
    plt.title('Traffic Pattern')
    plt.xlabel('Hour')
    plt.ylabel('Number of Requests')
    plt.tight_layout()
    #plt.show()
    
    save_chart('hourly_traffic_pattern.png')
    
    #Making a dual-axis line chart for total requests and success rate
    plt.figure(figsize=(14,6))
    hours=hourly_metrics['hour']
    tot_requests=hourly_metrics['total_requests']
    success_rate=hourly_metrics['success_rate']
    
    fig, ax1=plt.subplots()
    
    ax1.plot(hours,tot_requests,color='#2738F5',marker='o',label='Number of Requests')
    ax1.set_xlabel('Hours')
    ax1.set_ylabel('Number of Requests')
    ax1.tick_params(axis='y', labelcolor='#2738F5')
    
    ax2=ax1.twinx()
    ax2.plot(hours,success_rate,color='#3ED518',marker='s',label='Success Percentage')
    ax2.set_ylabel('Success Percentage(%)')
    ax2.tick_params(axis='y', labelcolor='#3ED518')
    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    plt.title('Total Requests and Success Rate')
    ax1.grid(True,alpha=1)
    plt.tight_layout()
    #plt.show()
    
    save_chart('tot_requests and success_rate.png')
    
#Visualizing for daily metrics
def visualize_daily_metrics(daily_metrics):
    """
    Generates visualizations for daily traffic trends.
    
    Highlights request volume patterns and
    days with unusually high error activity.
    
    Args:
        daily_metrics (pandas.DataFrame): Daily metrics dataset.
    
    Returns:
        None: Saves generated charts to file.
    """
    
    #Making a line + scatter plot for error highlightation
    x_axis=daily_metrics['day']
    y_axis=daily_metrics['total_requests']
    
    threshold=daily_metrics['error_count'].mean()
    high_errors=daily_metrics[daily_metrics['error_count']>threshold]
    
    plt.plot(x_axis,y_axis,color='#008000',linewidth=1,marker='s',label='total requests')
    plt.title('Daily Trend with Error Highlightation')
    plt.xlabel('Day')
    plt.ylabel('No. of Requests')
    plt.xticks(daily_metrics['day'])
    
    plt.scatter(high_errors['day'],high_errors['total_requests'],color='#FF0000',s=150,edgecolors='#000000',alpha=0.75,zorder=5,label='High Error Day')
    plt.legend(loc='upper right')
    plt.grid(True,alpha=0.5)
    
    plt.tight_layout()
    #plt.show()
    
    save_chart('Daily Trend with Errors.png')
    
#Visualizing for method metrics
def visualize_method_metrics(method_metrics):
    """
    Generates visualizations for HTTP method-level metrics.
    
    Creates charts showing method distribution
    and success versus error breakdown.
    
    Args:
        method_metrics (pandas.DataFrame): Method-level metrics dataset.
    
    Returns:
        None: Saves generated charts to file.
    """
    
    #Making a pie chart showing method distribution
    slices=method_metrics['total_requests']
    label_names=method_metrics['method']
    explode=[0, 0.01, 0, 0, 0]
    
    plt.pie(slices,labels=label_names,autopct='%1.1f%%',explode=explode)
    plt.title('Method Distribution')
    #plt.show()
    
    save_chart('Method Distribution.png')
    
    #Making a grouped bar chart to show success vs error breakdown
    methods=method_metrics['method']
    errors=method_metrics['error_count']
    success=method_metrics['total_requests']-method_metrics['error_count']
    x_indexes=np.arange(len(methods))
    width=0.2
    
    plt.bar(x_indexes-0.2,errors,width=width,color='#FF0000',label='Errors')
    plt.bar(x_indexes+0.2,success,width=width,color='#008000',label='Success')
    
    plt.legend()
    plt.grid(True,alpha=0.5)
    plt.xticks(ticks=x_indexes, labels=methods)
    plt.title('Success  Count V/S Error Count')
    plt.xlabel('Method')
    plt.ylabel('No. of Requests')
    plt.tight_layout()
    #plt.show()
    
    save_chart('Method_Success_vs_Error_Count.png')
    

    
    
if __name__=="__main__":
    user_metrics=pd.read_csv("Data/Transformed/user_metrics.csv")
    visualize_user_metrics(user_metrics)
    
    endpoint_metrics=pd.read_csv("Data/Transformed/endpoint_metrics.csv")
    visualize_endpoint_metrics(endpoint_metrics)
    
    hourly_metrics=pd.read_csv("Data/Transformed/hourly_metrics.csv")
    visualize_hourly_metrics(hourly_metrics)
    
    daily_metrics=pd.read_csv("Data/Transformed/daily_metrics.csv")
    visualize_daily_metrics(daily_metrics)
    
    method_metrics=pd.read_csv("Data/Transformed/method_metrics.csv")
    visualize_method_metrics(method_metrics)
    
    print("\n" + "="*60)
    print("✓ All Charts Created!!")
    print("="*60)



