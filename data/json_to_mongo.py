'''
Converts a single JSON tweet to a MongoDB entry
'''

import pymongo
import json
import time
import sys
from django.utils.encoding import smart_str

'''
Modify the Twitter format to that used in the MongoDB
Args: 
    orig : The original JSON object
Returns:
    modified_json : The MongoDB compatible object
'''

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.test # change this if needed
records = db.tweets_collection


def modify_json(orig):
    modified_json = {}
    modified_json["_id"] = orig["id_str"].encode('utf-8')
    modified_json["lang"] = orig["lang"].encode('utf-8')
    modified_json["acr"] = {}
    modified_json["acr"]["$date"] = int(time.mktime(time.strptime(str(orig["user"]["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
    modified_json["cr"] = {}
    modified_json["cr"]["$date"] = int(time.mktime(time.strptime(str(orig["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
    modified_json["t"] = str(orig["text"]).encode('utf-8').replace('"', '').replace("'","")
    modified_json["uid"] = str(orig["user"]["id_str"])
    modified_json["flrs"] = int(orig["user"]["followers_count"])
    
    # print "Checking place"
    if str(orig["place"]) != "None":
        modified_json["loc"] = str(orig["place"]["full_name"]).encode('utf-8')
        box = orig["place"]["bounding_box"]["coordinates"][0]
        modified_json["pln"] = float( format( (box[0][0]+box[2][0])/2.0, '.3f') )
        modified_json["plt"] = float( format( (box[0][1]+box[1][1])/2.0, '.3f') )
        modified_json["tln"] = modified_json["pln"] - 0.1
        modified_json["tlt"] = modified_json["plt"] - 0.1
        modified_json["cc"] = str(orig["place"]["country_code"])
        modified_json["f"] = str(orig["place"]["id"])  # no idea
        modified_json["p"] = str(orig["place"]["id"])  # no idea
        ###
        ###
        ### Change time here from 1505193831000 to 2012-10-02 06:12:21.000Z
        ###
        ###
    print modified_json
    # if str(orig["place"]) != "None":
    #     time.sleep(1)
    return modified_json

'''
Insert a single JSON string to the MongoDB
Args:
	json_text : JSON string
'''
def insert_json_to_mongo(json_text):
	json_text = json_text.strip()
	s = ""
	ctr = 0
	if len(json_text) != 0:
		try:
			orig = json.loads(json_text)
			modified_json = modify_json(orig)
			# print modified_json
			if modified_json:
				# print 'Checking insert'
				s += str(modified_json).encode('utf-8').replace("'", "\"") + "\n"
				# records.insert(modified_json)
			# print "Done"
		except Exception as e:
			print str(e), json_text
			print "Failed"

	return s
		

# replace below to add as you get a streamed tweet
f = open(sys.argv[1])
# f = open("sample.txt")
st = ""
ctr = 0
for line in f:
	print ctr
	st += insert_json_to_mongo(line)
	ctr += 1

print 'Start writing'
with open('output.json','w') as outfile:
	outfile.write(st)
outfile.close()