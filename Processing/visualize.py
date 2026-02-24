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
    
    
    
if __name__=="__main__":
    user_metrics=pd.read_csv("Data/Transformed/user_metrics.csv")
    visualize_user_metrics(user_metrics)
    
    endpoint_metrics=pd.read_csv("Data/Transformed/endpoint_metrics.csv")
    visualize_endpoint_metrics(endpoint_metrics)



