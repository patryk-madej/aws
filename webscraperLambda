import lxml
import requests
from bs4 import BeautifulSoup
import fnmatch
import os
import boto3

def lambda_handler(events, context):
    website = os.environ['website']
    result = requests.get(website)
    source = result.content
    soup = BeautifulSoup(source, 'lxml')

    event_divs = soup.find_all("div",{'class': 'event'}) #create list with the html objects

    events = []
    for a in event_divs:
        b=a.getText() #turn each complex html object into text
        c=b.split() #delete all whitespaces
        d=" ".join(c) #place single space between words
        if fnmatch.fnmatch(d, '*London*'): #match only events that have 'London' in them
                events.append(d)

    data = []
    for a in events:
        b=a.replace('Workshop at ', '_') #replace the following phrases on each string
        c=b.replace(' access_time ', '_')
        d=c.replace(' calendar_today ', '_')
        e=d.split('_') #split into lists along '_'
        data=data+e #add objects from 'e' list to the 'data' list

    event = data[0::4] #start with first(second) position, iterate every 4th to extract every event
    time = data[1::4]
    date = data[2::4]

    table = boto3.resource('dynamodb').Table('LondonEventsLambda') #access this specific DynamoDB table

    for x in range(len(events)):
        input = {
        "Event": event[x],
        "Time": time[x],
        "Date": date[x]
        }
        #print(input) #simulate DynamoDB
        response = table.put_item(Item=input)
