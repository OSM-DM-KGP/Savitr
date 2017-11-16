import json
import os 

file_arr=os.listdir('./')
out_file=open('out_floods.txt','w')
count=0
exception_count=0
for file in file_arr:
	print(file)
	if 'floods' not in file:
		continue
	if 	'25' in file:
		continue
	f = open(file)
	for line in f:
		try:
			line = line.strip()
			if len(line) == 0:
				continue
			line = line.replace("\n","")
			obj = json.loads(line)
			id_text=obj['id']
			tweet_text=obj['text']
			place_text=[]
			lat_long_str=""
			if str(obj["geo"])!="None":
				count+=1
				continue
			if str(obj["place"]) != "None":
				continue
				# place_text=obj["place"]["bounding_box"]["coordinates"]
				# for i in place_text[0]:
				# 	for j in i:
				# 		lat_long_str=lat_long_str+"<||>"+str(j)	
			else:

				out_file.write(str(id_text)+'<||>'+tweet_text.replace('\n',' ')+'\n')		
				# out_file.write('ad')
		except Exception as e:
			print(e,id_text)
			exception_count+=1
			continue		

print(exception_count)
print(count)			