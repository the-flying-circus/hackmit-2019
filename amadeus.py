import requests
from requests_oauthlib import OAuth2Session
import json
from pprint import pprint

TAG_BLACKLIST = {'pub', 'bar', 'liquor'}

keys = json.load(open('secrets/amadeus.json'))

from oauthlib.oauth2 import BackendApplicationClient

client = BackendApplicationClient(client_id=keys['client-id'])
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://test.api.amadeus.com/v1/security/oauth2/token', client_id=keys['client-id'], client_secret=keys['client-secret'])

def getPOIS(lat, long, num=5):
    pois = []
    p = 0
    while len(pois) < num:
        currentpoi = oauth.get('https://test.api.amadeus.com/v1/reference-data/locations/pois', params={'latitude': lat, 'longitude': long, 'radius': 2, "page[offset]": p}).json()
        pprint(currentpoi)
        for poi in currentpoi['data']:
            tags = set(poi['tags'])
            if len(tags & TAG_BLACKLIST) == 0:
                pois.append(poi)
        p += 1
    return pois

if __name__ == '__main__':
    pprint(getPOIS(13.4125, 103.8670))
