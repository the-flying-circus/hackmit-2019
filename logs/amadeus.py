import requests
import json
import os

from requests_oauthlib import OAuth2Session
from pprint import pprint

SECRETS_FILE = 'secrets/amadeus.json'
TAG_BLACKLIST = {'pub', 'bar', 'liquor', 'restaurant', 'nightclub'}
CATEGORY_BLACKLIST = {'nightlife', 'restaurant'}

if os.path.isfile(SECRETS_FILE):
    with open(SECRETS_FILE, 'r') as f:
        keys = json.load(f)
else:
    keys = {'client-id': None, 'client-secret': None}

from oauthlib.oauth2 import BackendApplicationClient

def getPOIS(lat, long, num=5):
    client = BackendApplicationClient(client_id=keys['client-id'])
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://api.amadeus.com/v1/security/oauth2/token', client_id=keys['client-id'], client_secret=keys['client-secret'])

    poiNames = set()
    pois = []
    p = 0
    rad = 2

    # give up after trying super extra hard
    bad = 0
    while len(pois) < num and bad < 5 and rad < 20:
        params = {'latitude': lat, 'longitude': long, 'radius': rad, "page[offset]": p}
        currentpoi = oauth.get('https://api.amadeus.com/v1/reference-data/locations/pois', params=params).json()
        if 'data' not in currentpoi:
            print(params)
            print(currentpoi)
            bad += 1
            p = 0
            rad *= 2
            continue
        if len(currentpoi['data']) < 1:
            p = 0
            rad *= 2
        pprint(currentpoi)
        for poi in currentpoi['data']:
            if poi['category'].lower() not in CATEGORY_BLACKLIST and poi['name'].lower() not in poiNames:
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
