from gazpacho import get, Soup

url = "https://codebar.io/events"

html = get(url)
soup = Soup(html)
cards = soup.find('a', {'class': 'card'})

def parse_card(card):
    version_number = card.find('p', {'class': 'release__version'}, strict=True).text
    timestamp = card.find('time').attrs['datetime']
    return {'version': version_number, 'timestamp': timestamp}