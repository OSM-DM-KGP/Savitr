import pandas as pd
import json
#data_valid.json stores all tweets
df = pd.read_json('all_tweets.json')

# with open('untagged_sample.json') as f:
#    data = json.load(f)
# df = pd.DataFrame(data)

df.to_csv('data.csv',
    index=False,
    columns=['_id', 'lang', 'tln', 'cc','loc','p','tlt','plt','t','cr','acr','pln','flrs','f','uid'],
    encoding='utf-8')
#_id lang    tln cc  loc p   tlt plt t   cr/$date    acr/$date   pln flrs    f   uid
