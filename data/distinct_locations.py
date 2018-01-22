import pickle
import json
## python 3 !!!
## root out duplicate locations from location_counts.json, which is obtained from mongo

with open('./Tweets_Location/india_location_dict.p','rb') as handle:
	india_loc_dict=pickle.load(handle)

with open('./location_counts.json','r') as f:
	counts=json.load(f)

print('Converting different locations to coordinates')
distinct_counts = {} # key location coordinates, value occurences sum
for each in counts:
	# {'_id': 'india', 'count': 3792}
	if each['_id'] in india_loc_dict:
		coordinates = india_loc_dict[each['_id']]
		#
		if coordinates not in distinct_counts:
			distinct_counts[coordinates] = 0
		distinct_counts[coordinates] += each['count']

print('Converting coordinates into one location')
# distinct counts sample: ('11.91667', '79.75'): 177
distinct_locations = {}
for each in distinct_counts:
	main_location = list(india_loc_dict.keys())[list(india_loc_dict.values()).index(each)]
	#
	if main_location not in distinct_locations:
		distinct_locations[main_location] = 0
	distinct_locations[main_location] += distinct_counts[each]

# frequency stores number of times location appears 10 times
s, s1 = '', ''
print(distinct_locations)
maximum = max(distinct_locations, key=distinct_locations.get)
print(maximum, distinct_locations[maximum])
maximum = distinct_locations[maximum]
frequency = [0]*(maximum+1)

for each in distinct_locations:
	s1 += each + '\t' + str(distinct_locations[each]) + '\n'
	frequency[distinct_locations[each]] += 1
	if each == '':
		continue
	for j in range(distinct_locations[each]):
		s += each.lower() + ' '

s+= '\n'
s1+= '\n'
with open("distinct_location_counts.txt", "w") as text_file:
    text_file.write(s1)

with open("distinct_locations_redundant.txt", "w") as text_file:
    text_file.write(s)

with open('frequency-counts.txt', 'w') as f:
	for i in range(maximum+1):
		if frequency[i] != 0:
			f.write(str(i) + '\t' + str(frequency[i]) + '\n')