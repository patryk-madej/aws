import json
import boto3

def DynamoDBStreamInsert(event, context):
    
    for record in event['Records']:
        
        if record['eventName'] == 'INSERT':
            newevent = record['dynamodb']['NewImage']['Event']['S']
            time = record['dynamodb']['NewImage']['Time']['S']
            date = record['dynamodb']['NewImage']['Date']['S']
            link = record['dynamodb']['NewImage']['Link']['S']
            
            message = str(newevent + ' | ' + time + ' | ' + date+ ' | ' + link)
            response = boto3.client('sns').publish(
                TopicArn='arn:aws:sns:eu-west-2:709303708159:dynamodb', 
                Message=f'{message}',
                MessageStructure='string'
            )
            return message
