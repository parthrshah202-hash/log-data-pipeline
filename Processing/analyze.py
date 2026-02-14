import pandas as pd
import os

#creating output folder
os.makedirs('Outputs/Reports',exist_ok=True)

#reading all metrices
def load_metrics(filename):
    df=pd.read_csv(filename)
    return df

def analyze_user_metrice(user_metrics):
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
    

if __name__=="__main__":
    user_metrics=load_metrics("Data/Transformed/user_metrics.csv")
    analyze_user_metrice(user_metrics)
    
    