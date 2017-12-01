import pandas as pd
import json
#data_valid.json stores all tweets
df = pd.read_json('all_tweets.json')

# with open('untagged_sample.json') as f:
#    data = json.load(f)
# df = pd.DataFrame(data)

df['cr'], df['acr'] = df['cr'].astype(str), df['acr'].astype(str)

cr_new, acr_new = [], []
# convert {u'$date': u'actual'} to actual
for i, row in df.iterrows():
	cr1,acr1 = row.cr[13:-2], row.acr[13:-2]
	# df.set_value(i,'cr',cr1)
	# df.set_value(i,'acr',acr1)
	cr_new.append(cr1)
	acr_new.append(acr1)
	print i
	if i %10000 == 0:
		print 'out of', str(len(df))

crname, acrname = df.columns[3], df.columns[1]
df.drop(crname, axis = 1, inplace = True)
df.drop(acrname, axis = 1, inplace = True)
df[crname] = cr_new
df[acrname] = acr_new

df.to_csv('data.csv',
    index=False,
    columns=['_id', 'lang', 'tln', 'cc','loc','p','tlt','plt','t','cr','acr','pln','flrs','f','uid'],
    encoding='utf-8')
#_id lang    tln cc  loc p   tlt plt t   cr/$date    acr/$date   pln flrs    f   uid
