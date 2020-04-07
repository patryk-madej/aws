![](diagram.png)

Finished my first functional personal project in AWS. 

It's a serverless webscraper, which sends me an email each time a new event is published on a particular website. I've made it because the website was missing email subscription and their events were getting fully booked very quickly. Now I've got an edge over manually booking folks.

Very proud of this, given I knew nothing about any of the components merely few months ago. Before, I was mostly image oriented (still can be, see the diagram below!). 

**Technical details.** 
I've written two Lambda functions in Python with custom IAM roles and settings (timeouts mostly, one environmental variable). First Lambda is deployed from Cloud9, as it was the easiest way to include several 3rd party libraries it required - that's the webscraper itself using libraries such as BeautifulSoup, lxml and requests. Triggered by CloudWatch every 6hrs, the function searches the website against a pattern. Once scraped, the data is then published to DynamoDB table, which in turn triggers the second Lambda through Streams (DB updates tracker). Output is then sent to my email via SNS topic.

Please share any comments on how to improve it! At the moment probably the weakest part is the first Lambda, the webscraper. The pattern is hard-coded, so the smallest change in formatting on the website will break the app, as it already did once. 

Also, looking for suggestions on how to move forward, maybe make something similar into a customer friendly product?



Would like to thank my Generation tutor Andy and my colleagues Dan, Patrick and Natasha, all of whom contributed.
