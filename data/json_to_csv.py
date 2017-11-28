import pandas as pd

df = pd.read_json('tweets_collection.json')
df.to_csv('data.csv',
    index=False,
    columns=['_id', 'lang', 'tln', 'cc','loc','tlt','plt','t','cr','acr','pln','flrs','f','uid'],
    encoding='utf-8')
#_id lang    tln cc  loc p   tlt plt t   cr/$date    acr/$date   pln flrs    f   uid
