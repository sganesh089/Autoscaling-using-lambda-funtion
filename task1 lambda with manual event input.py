import boto3
import json
false=None
true=None

autoscaling = boto3.client('autoscaling')

scale= ['blur','task1scalingnew']    #sample autoscaling group names


def lambda_handler(event, context):   

    event= {
            "eventVersion": "1.08",
            "userIdentity": {
                "type": "Root",
                "principalId": "878228182481",
                "arn": "arn:aws:iam::878228182481:root",
                "accountId": "878228182481",
                "accessKeyId": "ASIA4Y6T2SXISM3WD25T",
                "sessionContext": {
                    "sessionIssuer": {},
                    "webIdFederationData": {},
                    "attributes": {
                        "creationDate": "2022-04-02T06:40:53Z",
                        "mfaAuthenticated": "false"
                    }
                }
            },
            "eventTime": "2022-04-02T12:19:59Z",
            "eventSource": "elasticloadbalancing.amazonaws.com",
            "eventName": "DeleteLoadBalancer",
            "awsRegion": "us-east-1",
            "sourceIPAddress": "AWS Internal",
            "userAgent": "AWS Internal",
            "requestParameters": {
                "subnets": [],
                "securityGroups": ["sg-0979dfbd5c261b958"],
                "type": "application",
                "ipAddressType": "ipv4",
                "subnetMappings": [{
                        "subnetId": "subnet-08a8a4db8e985274f"
                    }, {
                        "subnetId": "subnet-04ff3c1d781d45591"
                    }
                ],
                "name": "trailtest",
                "tags": [{
                        "value": "2",
                        "key": "blur"
                    }, {
                        "value": "4",
                        "key": "task1scalingnew"
                    }
                ],
                "scheme": "internet-facing"
            },
            "responseElements": {
                "loadBalancers": [{
                        "loadBalancerName": "trailtest",
                        "securityGroups": ["sg-0979dfbd5c261b958"],
                        "state": {
                            "code": "provisioning"
                        },
                        "dNSName": "trailtest-379786080.us-east-1.elb.amazonaws.com",
                        "canonicalHostedZoneId": "Z35SXDOTRQ7X7K",
                        "loadBalancerArn": "arn:aws:elasticloadbalancing:us-east-1:878228182481:loadbalancer/app/trailtest/802548a8536de82b",
                        "type": "application",
                        "vpcId": "vpc-07e2d6b247b3729f5",
                        "availabilityZones": [{
                                "loadBalancerAddresses": [],
                                "subnetId": "subnet-04ff3c1d781d45591",
                                "zoneName": "us-east-1b"
                            }, {
                                "loadBalancerAddresses": [],
                                "subnetId": "subnet-08a8a4db8e985274f",
                                "zoneName": "us-east-1a"
                            }
                        ],
                        "ipAddressType": "ipv4",
                        "createdTime": "Apr 2, 2022 12:19:59 PM",
                        "scheme": "internet-facing"
                    }
                ]
            },
            "requestID": "f80b53f4-0397-4ec2-8162-546176c31b97",
            "eventID": "e6e87b56-b73b-4775-87b8-5f1af9a0f9ae",
            "readOnly": false,
            "eventType": "AwsApiCall",
            "apiVersion": "2015-12-01",
            "managementEvent": true,
            "recipientAccountId": "878228182481",
            "eventCategory": "Management",
            "sessionCredentialFromConsole": "true"
        }
    
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