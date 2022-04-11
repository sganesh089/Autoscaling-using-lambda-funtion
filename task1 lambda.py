import boto3
import json
false=None
true=None

autoscaling = boto3.client('autoscaling')

scale= ['blur','task1scalingnew']    #sample autoscaling group names


def lambda_handler(event, context):   
    
    name = (event["eventName"])
    
    #print(name)
    
    if name=="CreateLoadBalancer" :   
        
      
        tags=(event['requestParameters']['tags'])
        
        #getting the tags key value pair
        temp={tags[i]['key']: int(tags[i]['value']) for i in range(0, len(tags))}   
        
        #for looping the scaling groups
        for task in scale:  
        
            response = autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[
                    task,
                ],
            )
            
            original_min = (response['AutoScalingGroups'][0]['MinSize'])
    
            latest_min = original_min +( temp[task])
            
            original_max = (response['AutoScalingGroups'][0]['MaxSize'])
    
            latest_max = original_max +( temp[task])
            
            original_desired = (response['AutoScalingGroups'][0]['DesiredCapacity'])
    
            latest_desired = original_desired +( temp[task])
            
        
        #for testing updating scaling group max value only
        
            response1 = autoscaling.update_auto_scaling_group(   
                AutoScalingGroupName=task,
                MaxSize= latest_max,
                #MinSize= latest_min,
                #DesiredCapacity= latest_desired
            )
            
        #updating the tags
            response3 = autoscaling.create_or_update_tags(
                    Tags=[
                        {
                            'Key': 'clienta_nodes',
                            'PropagateAtLaunch': True,
                            'ResourceId': task,
                            'ResourceType': 'auto-scaling-group',
                            'Value': (str(temp[task])),
                        },
                    ],
                    )
            
         
        
    elif name=="DeleteLoadBalancer":
        
        #for looping the scaling groups
        for task in scale:
        
                response = autoscaling.describe_auto_scaling_groups(
                    AutoScalingGroupNames=[
                        task,
                    ],
                )
                
                
                original_tags =(response['AutoScalingGroups'][0]['Tags'])
                
                #getting the tagsd key value pair
                
                temp1={original_tags[i]['Key']: str(original_tags[i]['Value']) for i in range(0, len(original_tags))}
                
                tag1 = (temp1['clienta_nodes'])
                
                #updating the scaling group capacity
                original_max = (response['AutoScalingGroups'][0]['MaxSize'])
                
                latest_max = original_max -(int(tag1))
                
                original_min = (response['AutoScalingGroups'][0]['MinSize'])
                
                latest_min = original_min -(int(tag1))
                
                original_desired = (response['AutoScalingGroups'][0]['DesiredCapacity'])
    
                latest_desired = original_desired -(int(tag1))
                
                #updating max capacity alone for testing
                response1 = autoscaling.update_auto_scaling_group(
                            AutoScalingGroupName=task,
                            MaxSize= latest_max,
                            #MinSize= latest_min,
                            #DesiredCapacity= latest_desired
                        )
                #deleting the tags
                response3 = autoscaling.delete_tags(
                    Tags=[
                        {
                            'Key': 'clienta_nodes',
                            'PropagateAtLaunch': True,
                            'ResourceId': task,
                            'ResourceType': 'auto-scaling-group',
                            'Value': (str(tag1)),
                        },
                    ],
                    )