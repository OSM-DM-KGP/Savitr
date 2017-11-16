import json
import os
import glob
#f = open("file.txt")

file_arr=os.listdir('./')
for file in file_arr:
	print(file)

for line in f:
	line = line.strip()
	if len(line) == 0:
		continue
	line = line.replace("\n","")
	obj = json.loads(line)
	print(obj["text"].encode('utf-8'))
	print(obj["id"])

	 if str(obj["place"]) != "None":
		print(obj["place"]["bounding_box"]["coordinates"])


	if str(obj["geo"]) != "None":
		print(obj[""]["bounding_box"]["coordinates"])
