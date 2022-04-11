# Autoscaling-using-lambda-funtion

Requirement for the project is explained in the below image: 

![image](https://user-images.githubusercontent.com/41573564/162847306-1fbb9c27-9055-4e3c-bae9-c2526674e918.png)



1. Created 2 auto scaling groups "blur" and "task1scalingnew"
2. Created cloud watch event rules to monitor and trigger lambda function for "CreateLoadBalancer" & "DeleteLoadBalancer" events.
3. Created lambda function to update the autoscaling groups capacity depending on the triggered cloud watch events. 



