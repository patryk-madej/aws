from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import boto3

def lambda_handler(events, context):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = Request(url="https://codebar.io/events", headers=headers) 
    source = urlopen(request).read() 

    soup = BeautifulSoup(source, 'html.parser')

    event_divs = soup.find_all("div",{'class': 'event'})

    table = boto3.resource('dynamodb').Table('LondonEventsLambda')
    
    def timeChanger(time):
        gmt=int(time[-6:-4]) #|01|:00
        fromTime=int(time[:2]) #|18|:30 - 21:00
        toTime=int(time[8:10]) #18:30 - |21|:00
        if time[-7]=='+':
            gmtTime=f"{fromTime+gmt}:00-{toTime+gmt}:00 GMT"
        else: #if '-'
            gmtTime=f"{fromTime-gmt}:00-{toTime-gmt}:00 GMT"
        return(gmtTime)
    
    
    for i in range(len(event_divs)):

        event=soup.find_all("h3",{'class': 'title'})[i].text.replace('\n',' ').replace('Workshop at ','').strip()
        date=soup.find_all("div",{'class': 'date'})[i].text.replace('\n',' ').replace('calendar_today','').strip()
        time=soup.find_all("div",{'class': 'time'})[i].text.replace('\n',' ').replace('access_time','').strip()
        linkEnd=soup.find_all("h3",{'class': 'title'})[i].find('a')['href'].strip()
        link=f"https://codebar.io{linkEnd}"

        inp = {
        "Event": event,
        "Time": timeChanger(time),
        "Date": date,
        "Link": link
        }

        print(inp) #simulate DynamoDB input
        response = table.put_item(Item=inp)
