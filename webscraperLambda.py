import lxml
import requests
from bs4 import BeautifulSoup
#import fnmatch # not needed
import os
import boto3

def lambda_handler(events, context):
    website = os.environ['website'] #os.environ['website']
    result = requests.get(website)
    source = result.content
    soup = BeautifulSoup(source, 'lxml')

    event_divs = soup.find_all("div",{'class': 'event'}) # create list with the html objects

    events = []
    for a in event_divs:
        b=a.getText() # turn each complex html object into text
        c=b.split() # delete all whitespaces
        d=" ".join(c) # place single space between words
        if 'London' or 'Virtual' in d: # match only events that have 'London' or 'Virtual' in them
            events.append(d)
        #print(d)
    #print('-------------------------')
    #print(' P A R S E D  D A T A ')
    #print('-------------------------')        

    data = []
    for a in events:
        b=a.replace('Workshop at ', '') # replace the following phrases on each string
        c=b.replace(' access_time ', '_')
        d=c.replace(' calendar_today ', '_')
        e=d.split('_') # split into lists along '_'
        if e != '':
            data=data+e # add objects from 'e' list to the 'data' list
            #print(e)
        else:
            continue
    #print(data)
    #print('-------------------------')
    #print(' F I N A L  D A T A ')
    #print('-------------------------')

    event = data[0::3] # start with nth position, iterate every nth to extract every event
    date = data[1::3]
    time = data[2::3]

    table = boto3.resource('dynamodb').Table('LondonEventsLambda') #access this specific DynamoDB table

    for x in range(len(events)):
        inp = {
        "Event": event[x],
        "Time": time[x],
        "Date": date[x]
        }
        print(inp) #simulate DynamoDB
        response = table.put_item(Item=inp)


#lambda_handler(1, 2)
