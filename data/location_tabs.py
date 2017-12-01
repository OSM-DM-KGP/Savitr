import json

locations= json.load(open('location_counts.json'))

s, s1 = '', ''
for i in range(1, len(locations)):
	each = locations[i]
	# print str(each[u'_id'].encode('utf-8')) + '\t' + str(each[u'count'])
	s1 +=  str(each[u'_id'].encode('utf-8')) + '\t' + str(each[u'count']) + '\n'
	loc = str( each[u'_id'].encode('utf-8').split(',')[0] )
	if each[u'_id'] == '':
		continue
	for j in range(each[u'count']):
		s += loc.lower() + ' '

s+= '\n'
s1+= '\n'
with open("location_counts.txt", "w") as text_file:
    text_file.write(s1)

with open("locations_redundant.txt", "w") as text_file:
    text_file.write(s)