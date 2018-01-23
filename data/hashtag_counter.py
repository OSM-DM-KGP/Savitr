from collections import OrderedDict

with open('tweets_Jan22.txt','r') as f:
	txt = f.readlines()

print 'Read the file, now processing tweets'
hashtags = {}

print 'Total tweets', len(txt)
for i in range(len(txt)):
	# sample line
	# {"_id":"907538177992339456","t":"@RRTIndustries @brianmcarey They werent stealing shoes, they were rescuing them from the floods..."}
	tweet = txt[i][txt[i].index('t":"') + 4 : -2]
	hashes = [word.lower() for word in tweet.split() if word.startswith('#')]
	for each in hashes:
		if each not in hashtags:
			hashtags[each] = 0
		hashtags[each] += 1
	if i % 1000 == 0:
		print i,'tweets done'

# sort be frequency
sortedhashtags = OrderedDict()
for key, value in sorted(hashtags.iteritems(), key=lambda (k,v): (v,k), reverse=True):
    sortedhashtags[key] = value

print 'number of hashtags',len(sortedhashtags)
# print most frequent hashtags
for i in range(100):
	print i+1, sortedhashtags.items()[i]
