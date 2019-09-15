from pprint import pprint
import requests

with open('secrets/nlp-key.txt', 'r') as f:
    ibmKey = f.read()


def getIBMEmotions(text):
    sess = requests.Session()
    sess.auth = ("apikey", ibmKey)
    sess.params = {'version': '2019-07-12',
                   'features': 'emotion',
                   'text': text}
    sess.headers = {
        "accept": "application/json"
    }

    resp = sess.get('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze')

    try:
        return resp.json()['emotion']['document']['emotion']
    except KeyError:
        return {'joy': 0, 'sadness': 0, 'fear': 0, 'anger': 0, 'disgust': 0}


def getEntityEmotions(text):
    p = {'version': '2019-07-12',
         "features": {
             "emotion": {
                 "document": True
             },
             "entities": {
                 "emotion": True,
                 "limit": 10
             },
         },
         'text': text.replace('.', ',')}

    resp = requests.post('https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze', auth=("apikey", ibmKey), json=p)
    resp.raise_for_status()

    try:
        return resp.json()['entities'], resp.json()['emotion']['document']['emotion']
    except KeyError:
        return [], {'joy': 0, 'sadness': 0, 'fear': 0, 'anger': 0, 'disgust': 0}


def getMoodScores(emotions):
    mood = min(1, max(0, (emotions['joy'] - emotions['sadness']) / 2.0 + 0.5))
    anxiety = min(1, max(0, emotions['fear']))
    cynicism = min(1, max(0, (12 * emotions['anger'] * emotions['disgust'])))

    return {'mood': mood, 'anxiety': anxiety, 'cynicism': cynicism}


def parseEntityEmotions(entities, bigEmotions, blacklistedObj=None, blacklistedEmotion=None):
    maxEnt = -1
    gb = 'negative'
    for ind, entity in enumerate(entities):
        if entity['relevance'] < 0.75 or entity['text'] == blacklistedObj:
            continue
        score = getMoodScores(entity['emotion'])
        if score['mood'] < 0.3 or score['anxiety'] > 0.7 or score['cynicism'] > 0.7:
            if entities[maxEnt]['relevance'] <= entity['relevance']:
                maxEnt = ind
                gb = 'negative'
        elif score['mood'] > 0.7:
            if entities[maxEnt]['relevance'] <= entity['relevance']:
                maxEnt = ind
                gb = 'positive'
        else:
            if entities[maxEnt]['relevance'] <= entity['relevance']:
                maxEnt = ind
                gb = 'neutral'

    if maxEnt < 0:
        score = getMoodScores(bigEmotions)
        if score['mood'] < 0.3 or score['anxiety'] > 0.7 or score['cynicism'] > 0.7:
            gb = 'negative'
        elif score['mood'] > 0.7:
            gb = 'positive'
        else:
            gb = 'neutral'

        if blacklistedObj is None and gb == blacklistedEmotion:
            gb = 'neutral'

        return None, gb

    return entities[maxEnt]['text'], gb


if __name__ == '__main__':
    # anxious = getIBMEmotions("I'm really worried about HackMIT. I know that we're supposed to do well, but I'm afraid that we won't win any awards and then everything will be awful. I dread the awards ceremony and wish that I had never signed up to do this in the first place")
    #
    # happy = getIBMEmotions("Man, I am so excited about HackMIT. I really enjoy seeing my friends from high school and this is a great excuse to see them even though they're scattered to the four winds. I know that every year we do a great job and even though we might not always win the most prestigious awards, we're always very proud of the work that we do.")
    #
    # cynical = getIBMEmotions("God, everything sucks. What's even the point of doing a fucking hackathon if I can't even make a thousand dollars in prize money? This stupid thing is such a waste of time and it's going to cause me to fail two of my classes, not that it matters anyways.")
    #
    # cynicalandhappy = getIBMEmotions("God, everything sucks. What's even the point of doing a fucking hackathon if I can't even make a thousand dollars in prize money? This stupid thing is such a waste of time and it's going to cause me to fail two of my classes, not that it matters anyways. Anyway, Man, I am so excited about HackMIT. I really enjoy seeing my friends from high school and this is a great excuse to see them even though they're scattered to the four winds. I know that every year we do a great job and even though we might not always win the most prestigious awards, we're always very proud of the work that we do.")

    anxious = {'sadness': 0.129612, 'joy': 0.009714, 'fear': 0.872409, 'disgust': 0.16942, 'anger': 0.073921}
    happy = {'sadness': 0.040826, 'joy': 0.906656, 'fear': 0.035624, 'disgust': 0.012171, 'anger': 0.012046}
    cynical = {'sadness': 0.35241, 'joy': 0.007784, 'fear': 0.149868, 'disgust': 0.111196, 'anger': 0.713472}
    cynicalandhappy = {'sadness': 0.204797, 'joy': 0.654447, 'fear': 0.113967, 'disgust': 0.075324, 'anger': 0.599406}

    print('anxious sample:', anxious, getMoodScores(anxious))
    print('happy sample:', happy, getMoodScores(happy))
    print('cynical sample:', cynical, getMoodScores(cynical))
    print('cynical + happy sample:', cynicalandhappy, getMoodScores(cynicalandhappy))

    entities, emotes = getEntityEmotions(
        " Today was a pretty good day, That's a great time at work, Eric came in and complimented me, which never happens, That felt really nice, Even though Squidward was pretty mean to me, I actually got shit done, which again, doesn't actually happen that often.")
    pprint(entities)
    pprint(emotes)
    pprint(parseEntityEmotions(entities, emotes))

