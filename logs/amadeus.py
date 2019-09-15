import requests
from requests_oauthlib import OAuth2Session
import json
from pprint import pprint

TAG_BLACKLIST = {'pub', 'bar', 'liquor', 'restaurant', 'nightclub'}
CATEGORY_BLACKLIST = {'nightlife', 'restaurant'}

keys = json.load(open('secrets/amadeus.json'))

from oauthlib.oauth2 import BackendApplicationClient

client = BackendApplicationClient(client_id=keys['client-id'])
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://api.amadeus.com/v1/security/oauth2/token', client_id=keys['client-id'], client_secret=keys['client-secret'])

def getPOIS(lat, long, num=5):
    poiNames = set()
    pois = []
    p = 0
    rad = 2
    while len(pois) < num:
        currentpoi = oauth.get('https://api.amadeus.com/v1/reference-data/locations/pois', params={'latitude': lat, 'longitude': long, 'radius': rad, "page[offset]": p}).json()
        if len(currentpoi['data']) < 1:
            p = 0
            rad *= 2
        pprint(currentpoi)
        for poi in currentpoi['data']:
            if poi['category'].lower not in CATEGORY_BLACKLIST and poi['name'].lower() not in poiNames:
                pois.append(poi)
                poiNames.add(poi['name'].lower())
        p += 1
    return pois

if __name__ == '__main__':
    locs = json.load(open('static/locations.json'))
    for loc in locs['locations']:
        long, lat = loc['location']
        pois = getPOIS(lat, long)
        loc['pois'] = []
        for poi in pois:
            loc['pois'].append({'location': [poi['geoCode']['latitude'], poi['geoCode']['longitude']],
                                 'name': poi['name']})

    json.dump(locs, open('static/locations.json', 'w'))
