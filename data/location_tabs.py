import json

locations= json.load(open('location_counts.json'))

s = ''
for i in range(1, len(locations)):
	each = locations[i]
	# print str(each[u'_id'].encode('utf-8')) + '\t' + str(each[u'count'])
	# s +=  str(each[u'count']) + '\t' + str(each[u'_id'].encode('utf-8')) + '\n'
	loc = str( each[u'_id'].encode('utf-8').split(',')[0] )
	if each[u'_id'] == '':
		continue
	for j in range(each[u'count']):
		s += loc.lower() + ' '

s+= '\n'
# with open("location_counts.txt", "w") as text_file:
    # text_file.write(s)

with open("locations_redundant.txt", "w") as text_file:
    text_file.write(s)