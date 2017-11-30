import json
import os 
import time
import csv
import io
import pickle
import proper_noun 
import os
import subprocess
import re
from stop_words import get_stop_words
from nltk.tokenize import TweetTokenizer
from collections import defaultdict
import pickle
from nltk.corpus import wordnet as wn
from itertools import product
import spacy
from spacy.symbols import *
from nltk import Tree
import nltk
import sys 
from nltk.stem import *
from nltk.stem import *
import spacy
import random

nlp=spacy.load('en')
tknzr=TweetTokenizer(strip_handles=True,reduce_len=True)
import CMUTweetTagger
stop_words=get_stop_words('en')
stop_words_2=['i','me','we','us','you','u','she','her','his','he','him','it','they','them','who','which','whom','whose','that','this','these','those','anyone','someone','some','all','most','himself','herself','myself','itself','hers','ours','yours','theirs','to','in','at','for','from','etc',' ',',']
for i in stop_words_2:
	if i not in stop_words:
		stop_words.append(i)

count=0
# need_text=[]
# offer_text=[]
# location_list=[]
# id_need_list={}
# global_need_resource_list=[]
# id_offer_list=[]
# global_offer_resource_list=[]

unique_tweet_id_dict={}

lower_india_lat=7.841615498
upper_india_lat=35.5679807149
lower_india_long=68.4228514144
upper_india_long=97.6904295394

def empty_json(orig):
	f=0
	modified_json = {}
	##print(f+1)
	f+=1
	modified_json["_id"] = str(orig["id_str"])
	#print(f+1)
	f+=1
	modified_json["lang"] = str(orig["lang"])
	#print(f+1)
	f+=1
	modified_json["acr"] = {}
	#print(f+1)
	f+=1
	modified_json["acr"]["$date"] = int(time.mktime(time.strptime(str(orig["user"]["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
	#print(f+1)
	f+=1
	modified_json["cr"] = {}
	#print(f+1)
	f+=1
	modified_json["cr"]["$date"] = int(time.mktime(time.strptime(str(orig["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
	#print(f+1)
	f+=1
	modified_json["t"] = str(orig["text"]).replace('"', '').replace("'","")
	#print(f+1)
	f+=1
	modified_json["uid"] = str(orig["user"]["id_str"])
	#print(f+1)
	f+=1
	modified_json["flrs"] = int(orig["user"]["followers_count"])
	#print(f+1)
	f+=1
	modified_json['loc']=''
	#print(f+1)
	f+=1
	modified_json['pln']=''
	#print(f+1)
	f+=1
	modified_json['plt']=''
	#print(f+1)
	f+=1
	modified_json['tln']=''
	#print(f+1)
	f+=1
	modified_json['tlt']=''
	#print(f+1)
	f+=1
	modified_json['cc']=''
	#print(f+1)
	f+=1
	modified_json['f']=''
	#print(f+1)
	f+=1
	modified_json['p']=''
	#print(f+1)
	f+=1
	# print(orig)
	#print(f+1)
	f+=1
	return modified_json


def modify_json(orig):
	modified_json = {}
	modified_json["_id"] = str(orig["id_str"])
	modified_json["lang"] = str(orig["lang"])
	modified_json["acr"] = {}
	modified_json["acr"]["$date"] = int(time.mktime(time.strptime(str(orig["user"]["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
	modified_json["cr"] = {}
	modified_json["cr"]["$date"] = int(time.mktime(time.strptime(str(orig["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
	modified_json["t"] = str(orig["text"]).replace('"', '').replace("'","")
	modified_json["uid"] = str(orig["user"]["id_str"])
	modified_json["flrs"] = int(orig["user"]["followers_count"])
	flag=False
	# modified_json['loc']=''
	# modified_json['pln']=''
	# modified_json['plt']=''
	# modified_json['tln']=''
	# modified_json['tlt']=''
	# modified_json['cc']=''
	# modified_json['f']=''
	# modified_json['p']=''


	if str(orig["place"]) != "None":
		modified_json["loc"] = str(orig["place"]["full_name"])
		box = orig["place"]["bounding_box"]["coordinates"][0]
		# print(box)
		modified_json["pln"] = (box[0][0]+box[2][0])/2.0
		modified_json["plt"] = (box[0][1]+box[1][1])/2.0

		# print("Location : "+ modified_json['loc'])
		# print('Latitude and longitude')
		# print(modified_json['plt'])	
		# print(modified_json['pln'])	

		if modified_json['plt'] <=upper_india_lat and modified_json['plt'] >=lower_india_lat and modified_json['pln']<= upper_india_long and modified_json['pln']>= lower_india_long:
			flag=True
			if modified_json['loc'] in overall_location_dict:
				overall_location_dict[modified_json['loc']]+=1
			else:
				overall_location_dict[modified_json['loc']]=1

		modified_json["tln"] = modified_json["pln"]
		modified_json["tlt"] = modified_json["plt"]
		modified_json["cc"] = str(orig["place"]["country_code"])
		modified_json["f"] = str(orig["place"]["id"])  # no idea
		modified_json["p"] = str(orig["place"]["id"])  # no idea
	
	if flag== True:
		return flag,modified_json
	else:
		return flag,{}

def modify_json_2(orig,lat,longi,name):
	modified_json = {}
	modified_json["_id"] = orig["id_str"]
	modified_json["lang"] = orig["lang"]
	modified_json["acr"] = {}
	modified_json["acr"]["$date"] = int(time.mktime(time.strptime(str(orig["user"]["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
	modified_json["cr"] = {}
	modified_json["cr"]["$date"] = int(time.mktime(time.strptime(str(orig["created_at"]), "%a %b %d %H:%M:%S +0000 %Y"))*1000)
	modified_json["t"] = str(orig["text"]).replace('"', '').replace("'","")
	modified_json["uid"] = str(orig["user"]["id_str"])
	modified_json["flrs"] = int(orig["user"]["followers_count"])
	modified_json["loc"] = name
	if name in overall_location_dict:
		overall_location_dict[name]+=1
	else:
		overall_location_dict[name]=1

	modified_json["plt"] = lat
	modified_json["pln"] = longi
	modified_json["tln"] = modified_json["pln"]
	modified_json["tlt"] = modified_json["plt"]
	modified_json["cc"] = "IN"
	modified_json["f"] = "1e222211"
	modified_json["p"] = "1wwwewewert"
	
	return modified_json	


web_url="http[s]?:[a-zA-Z._0-9/]+[a-zA-Z0-9]"
replacables="RT\s|-\s|\s-|#|@"
prop_name="([A-Z][a-z]+)"
num="([0-9]+)"
name="([A-Za-z]+)"
and_rate="([&][a][m][p][;])"
ellipses="([A-Za-z0-9]+[…])"
mentions="([a-zA-z\s0-9]+[:])"
entity_type_list=['NORP','ORG','GPE','PERSON']

def tweet_preprocess(text):
	#text=" ".join(tknzr.tokenize(text))
	text=re.sub(web_url,'',text)
	text=re.sub(mentions,'',text)
	text=re.sub(ellipses,'',text)
	text=re.sub(and_rate,'and',text)
	text=re.sub(str(num)+''+name,"\\1 \\2",text)
	text=re.sub(name+''+str(num),"\\1 \\2",text)
	text=re.sub(prop_name+''+prop_name,"\\1 \\2",text)
	return text.lstrip().rstrip()

def tweet_preprocess2(text):
	#text=" ".join(tknzr.tokenize(text))
	text=re.sub(web_url,'',text)
	text=re.sub(mentions,'',text)
	text=re.sub(ellipses,'',text)
	text=re.sub(and_rate,'and',text)
	text=re.sub(replacables,'',text)
	text=" ".join(tknzr.tokenize(text))
	text=re.sub(str(num)+''+name,"\\1 \\2",text)
	text=re.sub(name+''+str(num),"\\1 \\2",text)
	text=re.sub(prop_name+''+prop_name,"\\1 \\2",text)
	return text.lstrip().rstrip()	

loc_preposition_list=['in','from','at','on','to','from','for','near', 'nearby']
need_verb_list=['need','needs','require','requires','wants','want','lack','lacks']
send_verb_list=['send','give','donate','transfer']
after_place_list=['building','house','road','rd','street','hospital','park','town','lake','city','town','village','college','school','bank','nagar','gram','kund','beach','railway','building','river','hill','hosp']
of_place_list=['village','town','city','region','outskirts']
of_people_list=['people','victims','survivors']
location_proper_list=defaultdict(list)
need_location_subject_list=defaultdict(list)
send_location_subject_list=defaultdict(list)
false_names=['london','malaria','kenya','twitter','city','name','park','city','north','south','east','west','town','the','se','nw','ne','sw','korea','ma','beach']
overall_location_dict={}

def give_location_2(tags):
	return_name_list=[]
	old_j=0
	l=len(tags)
	for i in range(0,l):
		if i<old_j:
			continue
		if tags[i][1]=='PROPN':
			add_val=""
			place_flag=0
			j=i+1
			while j<(len(tags)-1):
				if tags[j][0]==' ' or tags[j][1]=='CONJ':
					j+=1
				elif tags[j][0].lower() in after_place_list:
					add_val=add_val+" "+tags[j][0]
					place_flag=1
					j+=1	
				elif tags[j][1]=='PROPN' or tags[j][0]==',' or tags[j][1]=='ADJ':
					add_val=add_val+" "+tags[j][0]
					j+=1						
				else:	
					break		
			old_j=j		
			loc_name=tags[i][0].replace('#','')+add_val
			if place_flag==1:
				return_name_list.append(loc_name)
				continue
			if tags[i-1][0].lower() in loc_preposition_list:
				return_name_list.append(loc_name)
				place_flag=1
			if tags[i-1][0].lower()=='of':
				try:
					prev_word=tags[i-2][0].lower()
					#print(prev_word)
					if prev_word in of_place_list: 
						return_name_list.append(prev_word+" of "+loc_name)
						continue
					if prev_word in of_people_list:
						return_name_list.append(prev_word+" of "+loc_name)
						continue

					prev_word_list=wn.synsets(prev_word)
					both_set=set(of_place_list)|set(of_people_list)
					for item in both_set:
						possible_items=wn.synsets(item)
						for a,b in product(possible_items,prev_word_list):
							d= wn.wup_similarity(a,b)
							try:
								if d>0.7:
									#print(a,b)
									place_flag=1
									return_name_list.append(prev_word+" of "+loc_name)
									break			
							except:
								continue
						if place_flag==1:
							break				
				except:	
					continue		
	for names in return_name_list:
		names=re.sub('#','',names)
	return return_name_list				


with open('./SOCIAL_COMPUTING/india_location_dict.p','rb') as handle:
	india_loc_dict=pickle.load(handle)

file_arr=os.listdir('./SOCIAL_COMPUTING/INPUT_FILES3/') # 30 day entire tweets
# all_stream_input_files
count1=0
count2=0

all_lines=0
exception_count=0
for file in file_arr:
	outfile_with_location=open('./SOCIAL_COMPUTING/OUTPUT_FILES/B/'+file,'w')
	outfile_without_location=open('./SOCIAL_COMPUTING/OUTPUT_FILES/B/'+'_NOT_'+file,'w')
	f=open('./SOCIAL_COMPUTING/INPUT_FILES3/'+file)	
	print(file+'\n')
	for line in f:
		all_lines+=1
		try:
			line = line.strip()
			if len(line) == 0:
				continue
			line = line.replace("\n","")
			obj = json.loads(line)
			id_text=obj['id']
			if id_text in unique_tweet_id_dict:
				continue

			tweet_text=obj['text']
			place_text=[]
			lat_long_str=""
			if str(obj["place"]) != "None":
				f3,modified_json=modify_json(obj)
				if f3==True:
					outfile_with_location.write(json.dumps(modified_json)+'\n')
					count1+=1
					print("Count 1= "+ str(count1))
					unique_tweet_id_dict[id_text]=(tweet_text, True)
				else:
					obj2=empty_json(obj)
					outfile_without_location.write(json.dumps(obj2)+'\n')
					unique_tweet_id_dict[id_text]=(tweet_text, False)		
				continue
			else:

				text=tweet_text.replace('\n',' ')
				text=tweet_preprocess2(text)
				loc_list_CMU=[]
				need_spacy_tags=[]
				doc=nlp(text)
				for word in doc:
					temp=(word.text,word.pos_)
					need_spacy_tags.append(temp)			
				loc_list_spacy=give_location_2(need_spacy_tags)
				#print(time.time()-starttime2)
				org_list=[]
				poss_places=[]
				prev_word=""
				prev_word_type=""
				for word in doc:
					if word.ent_type_ in entity_type_list:
						org_list.append(word.orth_+"<_>"+word.ent_type_)
					else:
						org_list.append("<_>")
				for i in org_list:
					index=i.index("<_>")
					if i[index+3:]=='GPE' or i[index+3:]=='FACILITY' or i[index+3:]=='LOC':
						poss_places.append(i[:index])
				poss_places.extend(loc_list_spacy)

				if len(poss_places)==0:
					obj2=empty_json(obj)
					outfile_without_location.write(json.dumps(obj2)+'\n')
				else:	
					poss_places=set([i.lower() for i in poss_places])

				refined_poss_place_list=[]	
				for i in poss_places:
					if i in india_loc_dict:
						refined_poss_place_list.append((i,india_loc_dict[i]))

				if len(refined_poss_place_list)==0:
					obj2=empty_json(obj)
					outfile_without_location.write(json.dumps(obj2)+'\n')
					unique_tweet_id_dict[id_text]=(tweet_text,False)

				else:
					flag=False
					refined_poss_place_list=[i for i in refined_poss_place_list if i[0] not in false_names]
					
					if len(refined_poss_place_list)==0:
						obj2=empty_json(obj)
						outfile_without_location.write(json.dumps(obj2)+'\n')
						unique_tweet_id_dict[id_text]=(tweet_text, False)

					else:
						random_elem=refined_poss_place_list[0]
						modified_json=modify_json_2(obj,random_elem[1][0],random_elem[1][1],random_elem[0])
						outfile_with_location.write(json.dumps(modified_json)+'\n')
						count2+=1
						unique_tweet_id_dict[id_text]=(tweet_text,True)
						print("Count 2= "+ str(count2))


		except Exception as e:
			print(e,id_text)
			print(obj,obj2)
			exception_count+=1
			continue		

print(count1,count2)
print(exception_count)

print(len(unique_tweet_id_dict))
for i in overall_location_dict:
	print(i,overall_location_dict[i])