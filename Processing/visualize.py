import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')

#Visualizing for user_metrics
def visualize_user_metrics(user_metrics) :
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

    plt.savefig('Outputs/Charts/top_users.png',dpi=300,bbox_inches='tight')
    plt.close()
    
    #Making a histogram for success rate distribution
    success_rate=user_metrics['success_rate']
    bins=[0,10,20,30,40,50,60,70,80,90,100]

    plt.hist(success_rate,bins,color='green',edgecolor='black',alpha=0.75)
    plt.title("Success Rate Distribution")
    plt.ylabel("Users")
    plt.xlabel("Success Percentage")
    plt.tight_layout()
    #plt.show()

    plt.savefig('Outputs/Charts/success_rate.png',dpi=300,bbox_inches='tight')
    plt.close()

#Visualizing for endpoint_metrics
def visualize_endpoint_metrics(endpoint_metrics):
    #Making a scatter plot for response time V/S success rate
    x_axis=endpoint_metrics['avg_response_time']
    y_axis=endpoint_metrics['success_rate']
    
    plt.scatter(x_axis,y_axis,edgecolor='black',alpha=0.75)
    
    plt.title('Avg Response Time V/S Success Rate')
    plt.xlabel('Avg. Response Time(ms)')
    plt.ylabel('Success Rate(%)')
    plt.tight_layout()
    #plt.show()
    
    plt.savefig('Outputs/Charts/avg_time_vs_success_rate.png',dpi=300,bbox_inches='tight')
    plt.close()
    
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
    
    plt.savefig('Outputs/Charts/slowest_endpoints.png',dpi=300,bbox_inches='tight')
    plt.close()
    
#Visualizing for hourly metrics
def visualize_hourly_metrics(hourly_metrics):
    #Making line chart to show traffic pattern by hour
    plt.figure(figsize=(12,6))
    x_axis=hourly_metrics['hour']
    y_axis=hourly_metrics['total_requests']
    
    plt.plot(x_axis,y_axis,color="#52E626",linewidth='3',marker='o')
    plt.grid(True)
    plt.fill_between(x_axis, y_axis, alpha=0.3, color='steelblue', label='Traffic Volume')
    plt.axhline(y=300, color='red', linestyle='--',linewidth='2.0', label='Peak Threshold (300)')
    plt.legend(loc='upper left')
    
    plt.title('Traffic Pattern')
    plt.xlabel('Hour')
    plt.ylabel('Number of Requests')
    plt.tight_layout()
    #plt.show()
    
    plt.savefig('Outputs/Charts/hourly_traffic_pattern.png',dpi=300,bbox_inches='tight')
    plt.close()
    
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
    
    plt.savefig('Outputs/Charts/tot_requests and success_rate.png',dpi=300,bbox_inches='tight')
    plt.close()
    
if __name__=="__main__":
    user_metrics=pd.read_csv("Data/Transformed/user_metrics.csv")
    visualize_user_metrics(user_metrics)
    
    endpoint_metrics=pd.read_csv("Data/Transformed/endpoint_metrics.csv")
    visualize_endpoint_metrics(endpoint_metrics)
    
    hourly_metrics=pd.read_csv("Data/Transformed/hourly_metrics.csv")
    visualize_hourly_metrics(hourly_metrics)



