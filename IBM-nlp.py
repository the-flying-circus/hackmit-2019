from pprint import pprint
import requests

ibmKey = open('secrets/nlp-key.txt', 'r').read()

def getEmotions(text):
    sess = requests.Session()
    sess.auth = ("apikey", ibmKey)
    sess.params = {'version': '2019-07-12',
                  'features': 'emotion',
                  'text': text}
    sess.headers = {
        "accept": "application/json"
    }

    resp = sess.get('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze')

    return resp.json()['emotion']['document']['emotion']


if __name__ == '__main__':
    print(getEmotions("I'm really worried about HackMIT. I know that we're supposed to do well, but I'm afraid that we won't win any awards and then everything will be awful. I dread the awards ceremony and wish that I had never signed up to do this in the first place"))

    print(getEmotions("Man, I am so excited about HackMIT. I really enjoy seeing my friends from high school and this is a great excuse to see them even though they're scattered to the four winds. I know that every year we do a great job and even though we might not always win the most prestigious awards, we're always very proud of the work that we do."))
