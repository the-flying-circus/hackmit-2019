import requests
from requests_oauthlib import OAuth2Session
import json
from pprint import pprint

keys = json.load(open('secrets/amadeus.json'))

from oauthlib.oauth2 import BackendApplicationClient

client = BackendApplicationClient(client_id=keys['client-id'])
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://test.api.amadeus.com/v1/security/oauth2/token', client_id=keys['client-id'], client_secret=keys['client-secret'])

pprint(oauth.get('https://test.api.amadeus.com/v1/reference-data/locations/pois', params={'latitude':41.397158,'longitude':2.160873,'radius':2}).json())
