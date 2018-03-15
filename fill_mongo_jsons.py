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
import sys

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
	
	return flag,modified_json
	# if flag== True:
	# 	return flag,modified_json
	# else:
	# 	return flag,modified_json

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
dir_list=['north','south','east','west','upper','lower','greater','lesser']
need_verb_list=['need','needs','require','requires','wants','want','lack','lacks']
send_verb_list=['send','give','donate','transfer']
after_place_list=['building','house','road','rd','street','hospital','park','town','lake','city','town','village','college','school','bank','nagar','gram','kund','beach','railway','building','river','hill','hosp']
of_place_list=['village','town','city','region','outskirts']
of_people_list=['people','victims','survivors']
location_proper_list=defaultdict(list)
need_location_subject_list=defaultdict(list)
send_location_subject_list=defaultdict(list)

verbs = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

common_words= ['dialogue','language', 'rhythm', 'a', 'diamond', 'lap', 'abandon', 'diary', 'large', 'rib', 'ability', 'dictate', 'largely', 'ribbon', 'able', 'die', 'laser', 'rice', 'abortion', 'diet', 'last', 'rich', 'about', 'differ', 'late', 'rid', 'above', 'difference', 'lately', 'ride', 'abroad', 'different', 'later', 'rider', 'absence', 'differently', 'Latin', 'ridge', 'absolute', 'difficult', 'latter', 'ridiculous', 'absolutely', 'difficulty', 'laugh', 'rifle', 'absorb', 'dig', 'laughter', 'right', 'abstract', 'digital', 'launch', 'rim', 'abuse', 'dignity', 'law', 'ring', 'academic', 'dilemma', 'lawmaker', 'riot', 'accelerate', 'dimension', 'lawn', 'rip', 'accent', 'diminish', 'lawsuit', 'rise', 'accept', 'dining', 'lawyer', 'risk', 'acceptable', 'dinner', 'lay', 'risky', 'acceptance', 'dip', 'layer', 'ritual', 'access', 'diplomat', 'lead', 'rival', 'accessible', 'diplomatic', 'leader', 'river', 'accident', 'direct', 'leadership', 'road', 'accommodate', 'direction', 'leading', 'robot', 'accompany', 'directly', 'leaf', 'rock', 'accomplish', 'director', 'league', 'rocket', 'accomplishment', 'dirt', 'lean', 'rod', 'according', 'dirty', 'leap', 'role', 'account', 'disability', 'learn', 'roll', 'accountability', 'disabled', 'learning', 'rolling', 'accounting', 'disagree', 'least', 'Roman', 'accuracy', 'disappear', 'leather', 'romance', 'accurate', 'disappointed', 'leave', 'romantic', 'accurately', 'disappointment', 'lecture', 'roof', 'accusation', 'disaster', 'left', 'room', 'accuse', 'disc', 'leg', 'root', 'achieve', 'discipline', 'legacy', 'rope', 'achievement', 'disclose', 'legal', 'rose', 'acid', 'discount', 'legally', 'rough', 'acknowledge', 'discourage', 'legend', 'roughly', 'acquire', 'discourse', 'legislation', 'round', 'acquisition', 'discover', 'legislative', 'route', 'across', 'discovery', 'legislator', 'routine', 'act', 'discrimination', 'legislature', 'routinely', 'action', 'discuss', 'legitimate', 'row', 'active', 'discussion', 'lemon', 'royal', 'actively', 'disease', 'lend', 'rub', 'activist', 'dish', 'length', 'rubber', 'activity', 'disk', 'lens', 'ruin', 'actor', 'dismiss', 'less', 'rule', 'actress', 'disorder', 'lesson', 'ruling', 'actual', 'display', 'let', 'rumor', 'actually', 'dispute', 'letter', 'run', 'ad', 'dissolve', 'level', 'runner', 'adapt', 'distance', 'liability', 'running', 'add', 'distant', 'liberal', 'rural', 'added', 'distinct', 'liberty', 'rush', 'addition', 'distinction', 'library', 'Russian', 'additional', 'distinctive', 'license', 'sack', 'address', 'distinguish', 'lid', 'sacred', 'adequate', 'distract', 'lie', 'sacrifice', 'adjust', 'distribute', 'life', 'sad', 'adjustment', 'distribution', 'lifestyle', 'safe', 'administer', 'district', 'lifetime', 'safely', 'administration', 'disturb', 'lift', 'safety', 'administrative', 'disturbing', 'light', 'sail', 'administrator', 'diverse', 'lighting', 'sake', 'admire', 'diversity', 'lightly', 'salad', 'admission', 'divide', 'lightning', 'salary', 'admit', 'divine', 'like', 'sale', 'adolescent', 'division', 'likelihood', 'sales', 'adopt', 'divorce', 'likely', 'salmon', 'adoption', 'DNA', 'likewise', 'salt', 'adult', 'do', 'limb', 'same', 'advance', 'dock', 'limit', 'sample', 'advanced', 'doctor', 'limitation', 'sanction', 'advantage', 'doctrine', 'limited', 'sand', 'adventure', 'document', 'line', 'sandwich', 'advertising', 'documentary', 'link', 'satellite', 'advice', 'dog', 'lion', 'satisfaction', 'advise', 'doll', 'lip', 'satisfy', 'adviser', 'domain', 'liquid', 'sauce', 'advocate', 'domestic', 'list', 'save', 'aesthetic', 'dominant', 'listen', 'saving', 'affair', 'dominate', 'listener', 'say', 'affect', 'donate', 'literally', 'scale', 'afford', 'donation', 'literary', 'scan', 'afraid', 'donor', 'literature', 'scandal', 'African', 'door', 'little', 'scare', 'African-American', 'doorway', 'live', 'scared', 'after', 'dose', 'liver', 'scary', 'afternoon', 'dot', 'living', 'scatter', 'afterward', 'double', 'load', 'scenario', 'again', 'doubt', 'loan', 'scene', 'against', 'dough', 'lobby', 'scent', 'age', 'down', 'local', 'schedule', 'agency', 'downtown', 'locate', 'scheme', 'agenda', 'dozen', 'location', 'scholar', 'agent', 'draft', 'lock', 'scholarship', 'aggression', 'drag', 'log', 'school', 'aggressive', 'drain', 'logic', 'science', 'ago', 'drama', 'logical', 'scientific', 'agree', 'dramatic', 'lonely', 'scientist', 'agreement', 'dramatically', 'long', 'scope', 'agricultural', 'draw', 'long-term', 'score', 'agriculture', 'drawer', 'longtime', 'scramble', 'ah', 'drawing', 'look', 'scratch', 'ahead', 'dream', 'loop', 'scream', 'aid', 'dress', 'loose', 'screen', 'aide', 'dried', 'lose', 'screening', 'AIDS', 'drift', 'loss', 'screw', 'aim', 'drill', 'lost', 'script', 'air', 'drink', 'lot', 'sculpture', 'aircraft', 'drinking', 'lots', 'sea', 'airline', 'drive', 'loud', 'seal', 'airplane', 'driver', 'love', 'search', 'airport', 'driveway', 'lovely', 'season', 'aisle', 'driving', 'lover', 'seat', 'alarm', 'drop', 'low', 'second', 'album', 'drown', 'lower', 'secondary', 'alcohol', 'drug', 'loyal', 'secret', 'alien', 'drum', 'loyalty', 'secretary', 'alike', 'drunk', 'luck', 'section', 'alive', 'dry', 'lucky', 'sector', 'all', 'duck', 'lunch', 'secular', 'allegation', 'due', 'lung', 'secure', 'alleged', 'dumb', 'machine', 'security', 'allegedly', 'dump', 'mad', 'see', 'alley', 'during', 'magazine', 'seed', 'alliance', 'dust', 'magic', 'seek', 'allow', 'Dutch', 'magnetic', 'seem', 'ally', 'duty', 'magnitude', 'seemingly', 'almost', 'dying', 'mail', 'segment', 'alone', 'dynamic', 'main', 'seize', 'along', 'dynamics', 'mainly', 'seldom', 'alongside', 'each', 'mainstream', 'select', 'already', 'eager', 'maintain', 'selected', 'also', 'ear', 'maintenance', 'selection', 'alter', 'early', 'major', 'self', 'alternative', 'earn', 'majority', 'self-esteem', 'although', 'earnings', 'make', 'sell', 'altogether', 'earth', 'maker', 'seller', 'aluminum', 'earthquake', 'makeup', 'seminar', 'always', 'ease', 'male', 'Senate', 'AM', 'easily', 'mall', 'senator', 'amazing', 'east', 'man', 'send', 'ambassador', 'eastern', 'manage', 'senior', 'ambition', 'easy', 'management', 'sensation', 'ambitious', 'eat', 'manager', 'sense', 'amendment', 'eating', 'managing', 'sensitive', 'American', 'echo', 'mandate', 'sensitivity', 'amid', 'ecological', 'manipulate', 'sentence', 'among', 'economic', 'manner', 'sentiment', 'amount', 'economically', 'mansion', 'separate', 'analysis', 'economics', 'manufacturer', 'separation', 'analyst', 'economist', 'manufacturing', 'sequence', 'analyze', 'economy', 'many', 'series', 'ancestor', 'ecosystem', 'map', 'serious', 'ancient', 'edge', 'marble', 'seriously', 'and', 'edit', 'march', 'servant', 'and/or', 'edition', 'margin', 'serve', 'angel', 'editor', 'marine', 'service', 'anger', 'educate', 'mark', 'serving', 'angle', 'education', 'marker', 'session', 'angry', 'educational', 'market', 'set', 'animal', 'educator', 'marketing', 'setting', 'ankle', 'effect', 'marketplace', 'settle', 'anniversary', 'effective', 'marriage', 'settlement', 'announce', 'effectively', 'married', 'seven', 'announcement', 'effectiveness', 'marry', 'seventh', 'annual', 'efficiency', 'mask', 'several', 'annually', 'efficient', 'mass', 'severe', 'anonymous', 'effort', 'massive', 'severely', 'another', 'egg', 'master', 'sex', 'answer', 'ego', 'match', 'sexual', 'anticipate', 'eight', 'mate', 'sexuality', '', 'anxiety', 'eighth', 'material', 'sexually', 'anxious', 'either', 'math', 'sexy', 'any', 'elaborate', 'mathematics', 'shade', 'anybody', 'elbow', 'matter', 'shadow', 'anymore', 'elder', 'maximum', 'shake', 'anyone', 'elderly', 'may', 'shall', 'anything', 'elect', 'maybe', 'shallow', 'anyway', 'election', 'mayor', 'shame', 'anywhere', 'electric', 'me', 'shape', 'apart', 'electrical', 'meal', 'share', 'apartment', 'electricity', 'mean', 'shared', 'apologize', 'electronic', 'meaning', 'shareholder', 'apparent', 'electronics', 'meaningful', 'shark', 'apparently', 'elegant', 'meantime', 'sharp', 'appeal', 'element', 'meanwhile', 'sharply', 'appear', 'elementary', 'measure', 'she', 'appearance', 'elephant', 'measurement', 'shed', 'apple', 'elevator', 'meat', 'sheep', 'application', 'eleven', 'mechanic', 'sheer', 'apply', 'eligible', 'mechanical', 'sheet', 'appoint', 'eliminate', 'mechanism', 'shelf', 'appointment', 'elite', 'medal', 'shell', 'appreciate', 'else', 'media', 'shelter', 'appreciation', 'elsewhere', 'medical', 'shift', 'approach', 'e-mail', 'medication', 'shine', 'appropriate', 'embarrassed', 'medicine', 'ship', 'approval', 'embrace', 'medium', 'shirt', 'approve', 'emerge', 'meet', 'shit', 'approximately', 'emergency', 'meeting', 'shock', 'Arab', 'emerging', 'melt', 'shoe', 'architect', 'emission', 'member', 'shoot', 'architecture', 'emotion', 'membership', 'shooting', 'area', 'emotional', 'memory', 'shop', 'arena', 'emotionally', 'mental', 'shopping', 'argue', 'emphasis', 'mentally', 'shore', 'argument', 'emphasize', 'mention', 'short', 'arise', 'empire', 'mentor', 'shortage', 'arm', 'employ', 'menu', 'shortly', 'armed', 'employee', 'merchant', 'shorts', 'army', 'employer', 'mere', 'short-term', 'around', 'employment', 'merely', 'shot', 'arrange', 'empty', 'merit', 'should', 'arrangement', 'enable', 'mess', 'shoulder', 'array', 'enact', 'message', 'shout', 'arrest', 'encounter', 'metal', 'shove', 'arrival', 'encourage', 'metaphor', 'show', 'arrive', 'encouraging', 'meter', 'shower', 'arrow', 'end', 'method', 'shrimp', 'art', 'endless', 'metropolitan', 'shrink', 'article', 'endorse', 'Mexican', 'shrug', 'articulate', 'endure', 'middle', 'shut', 'artifact', 'enemy', 'midnight', 'shuttle', 'artificial', 'energy', 'midst', 'shy', 'artist', 'enforce', 'might', 'sibling', 'artistic', 'enforcement', 'migration', 'sick', 'as', 'engage', 'mild', 'side', 'ash', 'engagement', 'military', 'sidewalk', 'Asian', 'engine', 'milk', 'sigh', 'aside', 'engineer', 'mill', 'sight', 'ask', 'engineering', 'million', 'sign', 'asleep', 'English', 'mind', 'signal', 'aspect', 'enhance', 'mine', 'signature', 'ass', 'enjoy', 'mineral', 'significance', 'assault', 'enormous', 'minimal', 'significant', 'assemble', 'enough', 'minimize', 'significantly', 'assembly', 'enroll', 'minimum', 'silence', 'assert', 'ensure', 'minister', 'silent', 'assess', 'enter', 'ministry', 'silk', 'assessment', 'enterprise', 'minor', 'silly', 'asset', 'entertainment', 'minority', 'silver', 'assign', 'enthusiasm', 'minute', 'similar', 'assignment', 'entire', 'miracle', 'similarity', 'assist', 'entirely', 'mirror', 'similarly', 'assistance', 'entitle', 'miss', 'simple', 'assistant', 'entity', 'missile', 'simply', 'associate', 'entrance', 'missing', 'simultaneously', 'associated', 'entrepreneur', 'mission', 'sin', 'association', 'entry', 'missionary', 'since', 'assume', 'envelope', 'mistake', 'sing', 'assumption', 'environment', 'mix', 'singer', 'assure', 'environmental', 'mixed', 'single', 'astronomer', 'envision', 'mixture', 'sink', 'at', 'epidemic', 'mm-hmm', 'sir', 'athlete', 'episode', 'mobile', 'sister', 'athletic', 'equal', 'mode', 'sit', 'atmosphere', 'equality', 'model', 'site', 'atop', 'equally', 'moderate', 'situation', 'attach', 'equation', 'modern', 'six', 'attack', 'equip', 'modest', 'sixth', 'attempt', 'equipment', 'modify', 'size', 'attend', 'equity', 'molecule', 'ski', 'attendance', 'equivalent', 'mom', 'skill', 'attention', 'era', 'moment', 'skilled', 'attitude', 'error', 'momentum', 'skin', 'attorney', 'escape', 'money', 'skip', 'attract', 'especially', 'monitor', 'skirt', 'attraction', 'essay', 'monkey', 'skull', 'attractive', 'essence', 'monster', 'sky', 'attribute', 'essential', 'month', 'slam', 'auction', 'essentially', 'monthly', 'slap', 'audience', 'establish', 'monument', 'slave', 'aunt', 'establishment', 'mood', 'slavery', 'author', 'estate', 'moon', 'sleep', 'authority', 'estimate', 'moral', 'sleeve', 'authorize', 'estimated', 'more', 'slice', 'auto', 'etc', 'moreover', 'slide', 'automatic', 'ethical', 'morning', 'slight', 'automatically', 'ethics', 'mortality', 'slightly', 'automobile', 'ethnic', 'mortgage', 'slip', 'autonomy', 'European', 'most', 'slope', 'availability', 'evaluate', 'mostly', 'slot', 'available', 'evaluation', 'mother', 'slow', 'average', 'even', 'motion', 'slowly', 'avoid', 'evening', 'motivate', 'small', 'await', 'event', 'motivation', 'smart', 'awake', 'eventually', 'motive', 'smell', 'award', 'ever', 'motor', 'smile', 'aware', 'every', 'mount', 'smoke', 'awareness', 'everybody', 'mountain', 'smooth', 'away', 'everyday', 'mouse', 'snake', 'awful', 'everyone', 'mouth', 'snap', 'baby', 'everything', 'move', 'sneak', 'back', 'everywhere', 'movement', 'snow', 'background', 'evidence', 'movie', 'so', 'backyard', 'evident', 'Mr', 'soak', 'bacteria', 'evil', 'Mrs', 'soap', 'bad', 'evolution', 'Ms', 'soar', 'badly', 'evolve', 'much', 'so-called', 'bag', 'exact', 'mud', 'soccer', 'bake', 'exactly', 'multiple', 'social', 'balance', 'exam', 'municipal', 'socially', 'balanced', 'examination', 'murder', 'society', 'ball', 'examine', 'muscle', 'sock', 'balloon', 'example', 'museum', 'sodium', 'ballot', 'exceed', 'mushroom', 'sofa', 'ban', 'excellent', 'music', 'soft', 'banana', 'except', 'musical', 'soften', 'band', 'exception', 'musician', 'softly', 'bank', 'excessive', 'Muslim', 'software', 'banker', 'exchange', 'must', 'soil', 'banking', 'excited', 'mutter', 'solar', 'bankruptcy', 'excitement', 'mutual', 'soldier', 'bar', 'exciting', 'my', 'sole', 'bare', 'exclude', 'myself', 'solely', 'barely', 'exclusive', 'mysterious', 'solid', 'barn', 'exclusively', 'mystery', 'solution', 'barrel', 'excuse', 'myth', 'solve', 'barrier', 'execute', 'nail', 'some', 'base', 'execution', 'naked', 'somebody', 'baseball', 'executive', 'name', 'someday', 'basement', 'exercise', 'narrative', 'somehow', 'basic', 'exhaust', 'narrow', 'someone', 'basically', 'exhibit', 'nasty', 'something', 'basis', 'exhibition', 'nation', 'sometime', 'basket', 'exist', 'national', 'sometimes', 'basketball', 'existence', 'nationwide', 'somewhat', 'bat', 'existing', 'native', 'somewhere', 'bath', 'exit', 'natural', 'son', 'bathroom', 'exotic', 'naturally', 'song', 'battery', 'expand', 'nature', 'soon', 'battle', 'expansion', 'near', 'sophisticated', 'bay', 'expect', 'nearby', 'sorry', 'be', 'expectation', 'nearly', 'sort', 'beach', 'expected', 'neat', 'soul', 'beam', 'expedition', 'necessarily', 'sound', 'bean', 'expense', 'necessary', 'soup', 'bear', 'expensive', 'necessity', 'source', 'beard', 'experience', 'neck', 'south', 'beast', 'experienced', 'need', 'southeast', 'beat', 'experiment', 'needle', 'southern', 'beautiful', 'experimental', 'negative', 'southwest', 'beauty', 'expert', 'negotiate', 'sovereignty', 'because', 'expertise', 'negotiation', 'Soviet', 'become', 'explain', 'neighbor', 'space', 'bed', 'explanation', 'neighborhood', 'Spanish', 'bedroom', 'explicit', 'neighboring', 'spare', 'bee', 'explode', 'neither', 'spark', 'beef', 'exploit', 'nerve', 'speak', 'beer', 'exploration', 'nervous', 'speaker', 'before', 'explore', 'nest', 'special', 'beg', 'explosion', 'net', 'specialist', 'begin', 'export', 'network', 'specialize', 'beginning', 'expose', 'neutral', 'specialty', 'behalf', 'exposure', 'never', 'species', 'behave', 'express', 'nevertheless', 'specific', 'behavior', 'expression', 'new', 'specifically', 'behavioral', 'extend', 'newly', 'specify', 'behind', 'extended', 'news', 'spectacular', 'being', 'extension', 'newspaper', 'spectrum', 'belief', 'extensive', 'next', 'speculate', 'believe', 'extent', 'nice', 'speculation', 'bell', 'external', 'night', 'speech', 'belly', 'extra', 'nightmare', 'speed', 'belong', 'extraordinary', 'nine', 'spell', 'below', 'extreme', 'no', 'spend', 'belt', 'extremely', 'nobody', 'spending', 'bench', 'eye', 'nod', 'sphere', 'bend', 'eyebrow', 'noise', 'spill', 'beneath', 'fabric', 'nomination', 'spin', 'benefit', 'face', 'nominee', 'spine', 'beside', 'facilitate', 'none', 'spirit', 'besides', 'facility', 'nonetheless', 'spiritual', 'best', 'fact', 'nonprofit', 'spit', 'bet', 'factor', 'noon', 'spite', 'better', 'factory', 'nor', 'split', 'between', 'faculty', 'norm', 'spokesman', 'beyond', 'fade', 'normal', 'sponsor', 'bias', 'fail', 'normally', 'spoon', 'Bible', 'failure', 'north', 'sport', 'bicycle', 'faint', 'northeast', 'spot', 'bid', 'fair', 'northern', 'spouse', 'big', 'fairly', 'northwest', 'spray', 'bike', 'faith', 'nose', 'spread', 'bill', 'fall', 'not', 'spring', 'billion', 'false', 'note', 'sprinkle', 'bind', 'fame', 'notebook', 'spy', 'biography', 'familiar', 'nothing', 'squad', 'biological', 'family', 'notice', 'square', 'biology', 'famous', 'notion', 'squeeze', 'bird', 'fan', 'novel', 'stability', 'birth', 'fantastic', 'now', 'stable', 'birthday', 'fantasy', 'nowhere', 'stack', 'bishop', 'far', 'nuclear', 'stadium', 'bit', 'fare', 'number', 'staff', 'bite', 'farm', 'numerous', 'stage', 'bitter', 'farmer', 'nurse', 'stair', 'black', 'fascinating', 'nut', 'stake', 'blade', 'fashion', 'nutrient', 'stance', 'blame', 'fast', 'oak', 'stand', 'blank', 'faster', 'object', 'standard', 'blanket', 'fat', 'objection', 'standing', 'blast', 'fatal', 'objective', 'star', 'blend', 'fate', 'obligation', 'stare', 'bless', 'father', 'observation', 'start', 'blessing', 'fatigue', 'observe', 'starter', 'blind', 'fault', 'observer', 'starting', 'blink', 'favor', 'obstacle', 'state', 'block', 'favorable', 'obtain', 'statement', 'blond', 'favorite', 'obvious', 'station', 'blood', 'fear', 'obviously', 'statistical', 'bloody', 'feather', 'occasion', 'statistics', 'blow', 'feature', 'occasional', 'statue', 'blue', 'federal', 'occasionally', 'status', 'board', 'fee', 'occupation', 'statute', 'boast', 'feed', 'occupy', 'stay', 'boat', 'feedback', 'occur', 'steadily', 'body', 'feel', 'ocean', 'steady', 'boil', 'feeling', "o'clock", 'steak', 'bold', 'fellow', 'odd', 'steal', 'bolt', 'female', 'odds', 'steam', 'bomb', 'feminist', 'of', 'steel', 'bombing', 'fence', 'off', 'steep', 'bond', 'festival', 'offender', 'steer', 'bone', 'fever', 'offense', 'stem', 'bonus', 'few', 'offensive', 'step', 'book', 'fewer', 'offer', 'stick', 'boom', 'fiber', 'offering', 'stiff', 'boost', 'fiction', 'office', 'still', 'boot', 'field', 'officer', 'stimulate', 'booth', 'fierce', 'official', 'stimulus', 'border', 'fifteen', 'officially', 'stir', 'boring', 'fifth', 'often', 'stock', 'born', 'fifty', 'oh', 'stomach', 'borrow', 'fight', 'oil', 'stone', 'boss', 'fighter', 'ok', 'stop', 'both', 'fighting', 'okay', 'storage', 'bother', 'figure', 'old', 'store', 'bottle', 'file', 'old-fashioned', 'storm', 'bottom', 'fill', 'Olympic', 'story', 'bounce', 'film', 'Olympics', 'stove', 'boundary', 'filter', 'on', 'straight', 'bow', 'final', 'once', 'straighten', 'bowl', 'finally', 'one', 'strain', 'box', 'finance', 'one-third', 'strange', 'boy', 'financial', 'ongoing', 'stranger', 'boyfriend', 'find', 'onion', 'strategic', 'brain', 'finding', 'online', 'strategy', 'brake', 'fine', 'only', 'straw', 'branch', 'finger', 'onto', 'streak', 'brand', 'finish', 'open', 'stream', 'brave', 'fire', 'opening', 'street', 'bread', 'firm', 'openly', 'strength', 'break', 'firmly', 'opera', 'strengthen', 'breakfast', 'first', 'operate', 'stress', 'breast', 'fiscal', 'operating', 'stretch', 'breath', 'fish', 'operation', 'strict', 'breathe', 'fisherman', 'operator', 'strictly', 'breathing', 'fishing', 'opinion', 'strike', 'breeze', 'fist', 'opponent', 'striking', 'brick', 'fit', 'opportunity', 'string', 'bride', 'fitness', 'oppose', 'strip', 'bridge', 'five', 'opposed', 'stroke', 'brief', 'fix', 'opposite', 'strong', 'briefly', 'fixed', 'opposition', 'strongly', 'bright', 'flag', 'opt', 'structural', 'brilliant', 'flame', 'optimistic', 'structure', 'bring', 'flash', 'option', 'struggle', 'British', 'flat', 'or', 'student', 'broad', 'flavor', 'oral', 'studio', 'broadcast', 'flee', 'orange', 'study', 'broken', 'fleet', 'orbit', 'stuff', 'broker', 'flesh', 'order', 'stumble', 'bronze', 'flexibility', 'ordinary', 'stupid', 'brother', 'flexible', 'organ', 'style', 'brown', 'flight', 'organic', 'subject', 'brush', 'flip', 'organism', 'submit', 'brutal', 'float', 'organization', 'subsequent', 'bubble', 'flood', 'organizational', 'subsidy', 'buck', 'floor', 'organize', 'substance', 'bucket', 'flour', 'organized', 'substantial', 'buddy', 'flow', 'orientation', 'substantially', 'budget', 'flower', 'origin', 'subtle', 'bug', 'fluid', 'original', 'suburb', 'build', 'fly', 'originally', 'suburban', 'builder', 'flying', 'other', 'succeed', 'building', 'focus', 'others', 'success', 'bulb', 'fog', 'otherwise', 'successful', 'bulk', 'fold', 'ought', 'successfully', 'bull', 'folk', 'our', 'such', 'bullet', 'follow', 'ours', 'suck', 'bunch', 'following', 'ourselves', 'sudden', 'burden', 'food', 'out', 'suddenly', 'bureau', 'fool', 'outcome', 'sue', 'burn', 'foot', 'outdoor', 'suffer', 'burning', 'football', 'outer', 'suffering', 'bury', 'for', 'outfit', 'sufficient', 'bus', 'forbid', 'outlet', 'sugar', 'bush', 'force', 'outline', 'suggest', 'business', 'forehead', 'output', 'suggestion', 'businessman', 'foreign', 'outside', 'suicide', 'busy', 'foreigner', 'outsider', 'suit', 'but', 'forest', 'outstanding', 'suitable', 'butt', 'forever', 'oven', 'suite', 'butter', 'forget', 'over', 'sum', 'butterfly', 'forgive', 'overall', 'summary', 'button', 'fork', 'overcome', 'summer', 'buy', 'form', 'overlook', 'summit', 'buyer', 'formal', 'overnight', 'sun', 'by', 'format', 'oversee', 'sunlight', 'cab', 'formation', 'overwhelm', 'sunny', 'cabin', 'former', 'overwhelming', 'super', 'cabinet', 'formerly', 'owe', 'superior', 'cable', 'formula', 'own', 'supermarket', 'cage', 'forth', 'owner', 'supervisor', 'cake', 'fortunately', 'ownership', 'supplier', 'calculate', 'fortune', 'oxygen', 'supply', 'calculation', 'forty', 'pace', 'support', 'calendar', 'forum', 'pack', 'supporter', 'call', 'forward', 'package', 'supportive', 'calm', 'foster', 'pad', 'suppose', 'camera', 'found', 'page', 'supposed', 'camp', 'foundation', 'pain', 'supposedly', 'campaign', 'founder', 'painful', 'Supreme', 'campus', 'four', 'paint', 'sure', 'can', 'fourth', 'painter', 'surely', 'Canadian', 'fraction', 'painting', 'surface', 'cancel', 'fragile', 'pair', 'surgeon', 'cancer', 'fragment', 'palace', 'surgery', 'candidate', 'frame', 'pale', 'surprise', 'candle', 'framework', 'Palestinian', 'surprised', 'candy', 'franchise', 'palm', 'surprising', 'canvas', 'frankly', 'pan', 'surprisingly', 'cap', 'fraud', 'panel', 'surround', 'capability', 'free', 'panic', 'surrounding', 'capable', 'freedom', 'pant', 'surveillance', 'capacity', 'freely', 'paper', 'survey', 'capital', 'freeze', 'parade', 'survival', 'captain', 'French', 'parent', 'survive', 'capture', 'frequency', 'parental', 'survivor', 'car', 'frequent', 'parish', 'suspect', 'carbohydrate', 'frequently', 'park', 'suspend', 'carbon', 'fresh', 'parking', 'suspicion', 'card', 'freshman', 'part', 'suspicious', 'care', 'friend', 'partial', 'sustain', 'career', 'friendly', 'partially', 'sustainable', 'careful', 'friendship', 'participant', 'swallow', 'carefully', 'from', 'participate', 'swear', 'cargo', 'front', 'participation', 'sweat', 'carpet', 'frontier', 'particle', 'sweater', 'carrier', 'frown', 'particular', 'sweep', 'carrot', 'frozen', 'particularly', 'sweet', 'carry', 'fruit', 'partly', 'swell', 'cart', 'frustrate', 'partner', 'swim', 'cartoon', 'frustration', 'partnership', 'swimming', 'carve', 'fucking', 'party', 'swing', 'case', 'fuel', 'pass', 'switch', 'cash', 'full', 'passage', 'sword', 'casino', 'full-time', 'passenger', 'symbol', 'cast', 'fully', 'passing', 'symbolic', 'casual', 'fun', 'passion', 'sympathy', 'casualty', 'function', 'past', 'symptom', 'cat', 'functional', 'pasta', 'syndrome', 'catalog', 'fund', 'pastor', 'system', 'catch', 'fundamental', 'pat', 'table', 'category', 'funding', 'patch', 'tablespoon', 'Catholic', 'funeral', 'patent', 'tackle', 'cattle', 'funny', 'path', 'tactic', 'cause', 'fur', 'patience', 'tag', 'cave', 'furniture', 'patient', 'tail', 'cease', 'furthermore', 'patrol', 'take', 'ceiling', 'future', 'patron', 'tale', 'celebrate', 'gain', 'pattern', 'talent', 'celebration', 'galaxy', 'pause', 'talented', 'celebrity', 'gallery', 'pay', 'talk', 'cell', 'game', 'payment', 'tall', 'cemetery', 'gang', 'PC', 'tank', 'center', 'gap', 'peace', 'tap', 'central', 'garage', 'peaceful', 'tape', 'century', 'garbage', 'peak', 'target', 'CEO', 'garden', 'peanut', 'task', 'ceremony', 'garlic', 'peasant', 'taste', 'certain', 'gas', 'peel', 'tax', 'certainly', 'gasoline', 'peer', 'taxpayer', 'chain', 'gate', 'pen', 'tea', 'chair', 'gather', 'penalty', 'teach', 'chairman', 'gathering', 'pencil', 'teacher', 'challenge', 'gay', 'pension', 'teaching', 'chamber', 'gaze', 'people', 'team', 'champion', 'gear', 'pepper', 'teammate', 'championship', 'gender', 'per', 'tear', 'chance', 'gene', 'perceive', 'teaspoon', 'change', 'general', 'perceived', 'technical', 'changing', 'generally', 'percentage', 'technician', 'channel', 'generate', 'perception', 'technique', 'chaos', 'generation', 'perfect', 'technological', 'chapter', 'generous', 'perfectly', 'technology', 'character', 'genetic', 'perform', 'teen', 'characteristic', 'genius', 'performance', 'teenage', 'characterize', 'genre', 'performer', 'teenager', 'charge', 'gentle', 'perhaps', 'telephone', 'charity', 'gentleman', 'period', 'telescope', 'charm', 'gently', 'permanent', 'television', 'chart', 'genuine', 'permission', 'tell', 'charter', 'German', 'permit', 'temperature', 'chase', 'gesture', 'Persian', 'temple', 'cheap', 'get', 'persist', 'temporary', 'cheat', 'ghost', 'person', 'ten', 'check', 'giant', 'personal', 'tend', 'cheek', 'gift', 'personality', 'tendency', 'cheer', 'gifted', 'personally', 'tender', 'cheese', 'girl', 'personnel', 'tennis', 'chef', 'girlfriend', 'perspective', 'tension', 'chemical', 'give', 'persuade', 'tent', 'chemistry', 'given', 'pet', 'term', 'chest', 'glad', 'phase', 'terms', 'chew', 'glance', 'phenomenon', 'terrain', 'chicken', 'glass', 'philosophical', 'terrible', 'chief', 'glimpse', 'philosophy', 'terribly', 'child', 'global', 'phone', 'terrific', 'childhood', 'globe', 'photo', 'territory', 'chill', 'glory', 'photograph', 'terror', 'chin', 'glove', 'photographer', 'terrorism', 'Chinese', 'go', 'photography', 'terrorist', 'chip', 'goal', 'phrase', 'test', 'chocolate', 'goat', 'physical', 'testify', 'choice', 'God', 'physically', 'testimony', 'cholesterol', 'gold', 'physician', 'testing', 'choose', 'golden', 'physics', 'text', 'chop', 'golf', 'piano', 'textbook', 'Christian', 'good', 'pick', 'texture', 'Christianity', 'govern', 'pickup', 'than', 'Christmas', 'government', 'picture', 'thank', 'chronic', 'governor', 'pie', 'thanks', 'chunk', 'grab', 'piece', 'Thanksgiving', 'church', 'grace', 'pig', 'that', 'cigarette', 'grade', 'pile', 'the', 'circle', 'gradually', 'pill', 'theater', 'circuit', 'graduate', 'pillow', 'their', 'circumstance', 'graduation', 'pilot', 'them', 'cite', 'grain', 'pin', 'theme', 'citizen', 'grand', 'pine', 'themselves', 'citizenship', 'grandchild', 'pink', 'then', 'city', 'grandfather', 'pioneer', 'theological', 'civic', 'grandmother', 'pipe', 'theology', 'civil', 'grandparent', 'pit', 'theoretical', 'civilian', 'grant', 'pitch', 'theory', 'civilization', 'grape', 'pitcher', 'therapist', 'claim', 'grasp', 'pizza', 'therapy', 'class', 'grass', 'place', 'there', 'classic', 'grateful', 'placement', 'thereby', 'classical', 'grave', 'plain', 'therefore', 'classify', 'gravity', 'plan', 'these', 'classroom', 'gray', 'plane', 'they', 'clay', 'great', 'planet', 'thick', 'clean', 'greatest', 'planner', 'thigh', 'clear', 'greatly', 'planning', 'thin', 'clearly', 'Greek', 'plant', 'thing', 'clerk', 'green', 'plastic', 'think', 'click', 'greet', 'plate', 'thinking', 'client', 'grief', 'platform', 'third', 'cliff', 'grin', 'play', 'thirty', 'climate', 'grip', 'player', 'this', 'climb', 'grocery', 'playoff', 'thoroughly', 'cling', 'gross', 'plea', 'those', 'clinic', 'ground', 'plead', 'though', 'clinical', 'group', 'pleasant', 'thought', 'clip', 'grow', 'please', 'thousand', 'clock', 'growing', 'pleased', 'thread', 'close', 'growth', 'pleasure', 'threat', 'closed', 'guarantee', 'plenty', 'threaten', 'closely', 'guard', 'plot', 'three', 'closer', 'guess', 'plunge', 'threshold', 'closest', 'guest', 'plus', 'thrive', 'closet', 'guidance', 'PM', 'throat', 'cloth', 'guide', 'pocket', 'through', 'clothes', 'guideline', 'poem', 'throughout', 'clothing', 'guilt', 'poet', 'throw', 'cloud', 'guilty', 'poetry', 'thumb', 'club', 'guitar', 'point', 'thus', 'clue', 'gun', 'poke', 'ticket', 'cluster', 'gut', 'pole', 'tide', 'coach', 'guy', 'police', 'tie', 'coal', 'gym', 'policeman', 'tight', 'coalition', 'ha', 'policy', 'tighten', 'coast', 'habit', 'political', 'tightly', 'coastal', 'habitat', 'politically', 'tile', 'coat', 'hair', 'politician', 'till', 'cocaine', 'half', 'politics', 'timber', 'code', 'halfway', 'poll', 'time', 'coffee', 'hall', 'pollution', 'timing', 'cognitive', 'hallway', 'pond', 'tiny', 'coin', 'hand', 'pool', 'tip', 'cold', 'handful', 'poor', 'tire', 'collaboration', 'handle', 'pop', 'tired', 'collapse', 'handsome', 'popular', 'tissue', 'collar', 'hang', 'popularity', 'title', 'colleague', 'happen', 'population', 'to', 'collect', 'happily', 'porch', 'tobacco', 'collection', 'happiness', 'pork', 'today', 'collective', 'happy', 'port', 'toe', 'collector', 'harassment', 'portfolio', 'together', 'college', 'hard', 'portion', 'toilet', 'colonial', 'hardly', 'portrait', 'tolerance', 'colony', 'hardware', 'portray', 'tolerate', 'color', 'harm', 'pose', 'toll', 'colorful', 'harmony', 'position', 'tomato', 'column', 'harsh', 'positive', 'tomorrow', 'columnist', 'harvest', 'possess', 'tone', 'combat', 'hat', 'possession', 'tongue', 'combination', 'hate', 'possibility', 'tonight', 'combine', 'haul', 'possible', 'too', 'combined', 'have', 'possibly', 'tool', 'come', 'hay', 'post', 'tooth', 'comedy', 'hazard', 'poster', 'top', 'comfort', 'he', 'pot', 'topic', 'comfortable', 'head', 'potato', 'toss', 'coming', 'headache', 'potential', 'total', 'command', 'headline', 'potentially', 'totally', 'commander', 'headquarters', 'pound', 'touch', 'comment', 'heal', 'pour', 'touchdown', 'commercial', 'health', 'poverty', 'tough', 'commission', 'health-care', 'powder', 'tour', 'commissioner', 'healthy', 'power', 'tourism', 'commit', 'hear', 'powerful', 'tourist', 'commitment', 'hearing', 'practical', 'tournament', 'committee', 'heart', 'practically', 'toward', 'commodity', 'heat', 'practice', 'towards', 'common', 'heaven', 'practitioner', 'towel', 'commonly', 'heavily', 'praise', 'tower', 'communicate', 'heavy', 'pray', 'town', 'communication', 'heel', 'prayer', 'toxic', 'community', 'height', 'preach', 'toy', 'companion', 'helicopter', 'precious', 'trace', 'company', 'hell', 'precise', 'track', 'comparable', 'hello', 'precisely', 'trade', 'compare', 'helmet', 'predator', 'trading', 'comparison', 'help', 'predict', 'tradition', 'compel', 'helpful', 'prediction', 'traditional', 'compelling', 'hence', 'prefer', 'traditionally', 'compensation', 'her', 'preference', 'traffic', 'compete', 'herb', 'pregnancy', 'tragedy', 'competition', 'here', 'pregnant', 'tragic', 'competitive', 'heritage', 'preliminary', 'trail', 'competitor', 'hero', 'premise', 'trailer', 'complain', 'hers', 'premium', 'train', 'complaint', 'herself', 'preparation', 'trainer', 'complete', 'hesitate', 'prepare', 'training', 'completely', 'hey', 'prescription', 'trait', 'complex', 'hi', 'presence', 'transaction', 'complexity', 'hidden', 'present', 'transfer', 'compliance', 'hide', 'presentation', 'transform', 'complicated', 'high', 'preserve', 'transformation', 'comply', 'highlight', 'presidency', 'transit', 'component', 'highly', 'president', 'transition', 'compose', 'high-tech', 'presidential', 'translate', 'composition', 'highway', 'press', 'translation', 'compound', 'hike', 'pressure', 'transmission', 'comprehensive', 'hill', 'presumably', 'transmit', 'comprise', 'him', 'pretend', 'transport', 'compromise', 'himself', 'pretty', 'transportation', 'computer', 'hint', 'prevail', 'trap', 'concede', 'hip', 'prevent', 'trash', 'conceive', 'hire', 'prevention', 'trauma', 'concentrate', 'his', 'previous', 'travel', 'concentration', 'Hispanic', 'previously', 'traveler', 'concept', 'historian', 'price', 'tray', 'conception', 'historic', 'pride', 'treasure', 'concern', 'historical', 'priest', 'treat', 'concerned', 'historically', 'primarily', 'treatment', 'concerning', 'history', 'primary', 'treaty', 'concert', 'hit', 'prime', 'tree', 'conclude', 'hockey', 'principal', 'tremendous', 'conclusion', 'hold', 'principle', 'trend', 'concrete', 'hole', 'print', 'trial', 'condemn', 'holiday', 'prior', 'tribal', 'condition', 'holy', 'priority', 'tribe', 'conduct', 'home', 'prison', 'trick', 'conference', 'homeland', 'prisoner', 'trigger', 'confess', 'homeless', 'privacy', 'trim', 'confession', 'homework', 'private', 'trip', 'confidence', 'honest', 'privately', 'triumph', 'confident', 'honestly', 'privilege', 'troop', 'confirm', 'honey', 'prize', 'tropical', 'conflict', 'honor', 'pro', 'trouble', 'confront', 'hook', 'probably', 'troubled', 'confrontation', 'hope', 'problem', 'truck', 'confuse', 'hopefully', 'procedure', 'truly', 'confusion', 'horizon', 'proceed', 'trunk', 'Congress', 'hormone', 'process', 'trust', 'congressional', 'horn', 'processing', 'true', 'connect', 'horrible', 'processor', 'truth', 'connection', 'horror', 'proclaim', 'try', 'conscience', 'horse', 'produce', 'T-shirt', 'conscious', 'hospital', 'producer', 'tube', 'consciousness', 'host', 'product', 'tuck', 'consecutive', 'hostage', 'production', 'tumor', 'consensus', 'hostile', 'productive', 'tune', 'consent', 'hot', 'productivity', 'tunnel', 'consequence', 'hotel', 'profession', 'turkey', 'consequently', 'hour', 'professional', 'turn', 'conservation', 'house', 'professor', 'TV', 'conservative', 'household', 'profile', 'twelve', 'consider', 'housing', 'profit', 'twentieth', 'considerable', 'how', 'profound', 'twenty', 'considerably', 'however', 'program', 'twice', 'consideration', 'hug', 'programming', 'twin', 'consist', 'huge', 'progress', 'twist', 'consistent', 'huh', 'progressive', 'two', 'consistently', 'human', 'prohibit', 'two-thirds', 'conspiracy', 'humanity', 'project', 'type', 'constant', 'humor', 'projection', 'typical', 'constantly', 'hundred', 'prominent', 'typically', 'constitute', 'hunger', 'promise', 'ugly', 'constitution', 'hungry', 'promising', 'uh', 'constitutional', 'hunt', 'promote', 'ultimate', 'constraint', 'hunter', 'promotion', 'ultimately', 'construct', 'hunting', 'prompt', 'unable', 'construction', 'hurricane', 'proof', 'uncertain', 'consult', 'hurry', 'proper', 'uncertainty', 'consultant', 'hurt', 'properly', 'uncle', 'consume', 'husband', 'property', 'uncomfortable', 'consumer', 'hypothesis', 'proportion', 'uncover', 'consumption', 'I', 'proposal', 'under', 'contact', 'ice', 'propose', 'undergo', 'contain', 'icon', 'proposed', 'undergraduate', 'container', 'idea', 'prosecution', 'underlying', 'contemplate', 'ideal', 'prosecutor', 'undermine', 'contemporary', 'identical', 'prospect', 'understand', 'contend', 'identification', 'protect', 'understanding', 'content', 'identify', 'protection', 'undertake', 'contest', 'identity', 'protective', 'unemployment', 'context', 'ideological', 'protein', 'unexpected', 'continent', 'ideology', 'protest', 'unfair', 'continue', 'ie', 'protocol', 'unfold', 'continued', 'if', 'proud', 'unfortunately', 'continuing', 'ignore', 'prove', 'unhappy', 'continuous', 'ill', 'provide', 'uniform', 'contract', 'illegal', 'provided', 'union', 'contractor', 'illness', 'provider', 'unique', 'contrast', 'illusion', 'province', 'unit', 'contribute', 'illustrate', 'provision', 'unite', 'contribution', 'image', 'provoke', 'United', 'contributor', 'imagination', 'psychological', 'unity', 'control', 'imagine', 'psychologist', 'universal', 'controversial', 'immediate', 'psychology', 'universe', 'controversy', 'immediately', 'public', 'university', 'convenience', 'immigrant', 'publication', 'unknown', 'convention', 'immigration', 'publicity', 'unless', 'conventional', 'immune', 'publicly', 'unlike', 'conversation', 'impact', 'publish', 'unlikely', 'conversion', 'implement', 'publisher', 'unprecedented', 'convert', 'implementation', 'pull', 'until', 'convey', 'implication', 'pulse', 'unusual', 'convict', 'imply', 'pump', 'up', 'conviction', 'import', 'punch', 'update', 'convince', 'importance', 'punish', 'upon', 'convinced', 'important', 'punishment', 'upper', 'cook', 'importantly', 'purchase', 'upset', 'cookie', 'impose', 'pure', 'upstairs', 'cooking', 'impossible', 'purple', 'urban', 'cool', 'impress', 'purpose', 'urge', 'cooperate', 'impression', 'purse', 'us', 'cooperation', 'impressive', 'pursue', 'use', 'cooperative', 'improve', 'pursuit', 'used', 'coordinate', 'improved', 'push', 'useful', 'coordinator', 'improvement', 'put', 'user', 'cop', 'impulse', 'puzzle', 'usual', 'cope', 'in', 'qualify', 'usually', 'copy', 'incentive', 'quality', 'utility', 'cord', 'incident', 'quantity', 'utilize', 'core', 'include', 'quarter', 'vacation', 'corn', 'including', 'quarterback', 'vaccine', 'corner', 'income', 'queen', 'vacuum', 'corporate', 'incorporate', 'quest', 'valid', 'corporation', 'increase', 'question', 'validity', 'correct', 'increased', 'questionnaire', 'valley', 'correctly', 'increasing', 'quick', 'valuable', 'correlation', 'increasingly', 'quickly', 'value', 'correspondent', 'incredible', 'quiet', 'van', 'corridor', 'incredibly', 'quietly', 'vanish', 'corruption', 'indeed', 'quit', 'variable', 'cost', 'independence', 'quite', 'variation', 'costly', 'independent', 'quote', 'variety', 'costume', 'index', 'rabbit', 'various', 'cottage', 'Indian', 'race', 'vary', 'cotton', 'indicate', 'racial', 'vast', 'couch', 'indication', 'racism', 'vegetable', 'could', 'indicator', 'rack', 'vehicle', 'council', 'indigenous', 'radar', 'vendor', 'counsel', 'individual', 'radiation', 'venture', 'counseling', 'industrial', 'radical', 'verbal', 'counselor', 'industry', 'radio', 'verdict', 'count', 'inevitable', 'rage', 'version', 'counter', 'inevitably', 'rail', 'versus', 'counterpart', 'infant', 'railroad', 'vertical', 'country', 'infection', 'rain', 'very', 'county', 'inflation', 'raise', 'vessel', 'coup', 'influence', 'rally', 'veteran', 'couple', 'influential', 'ranch', 'via', 'courage', 'inform', 'random', 'victim', 'course', 'informal', 'range', 'victory', 'court', 'information', 'rank', 'video', 'courtroom', 'infrastructure', 'rape', 'view', 'cousin', 'ingredient', 'rapid', 'viewer', 'cover', 'inherent', 'rapidly', 'village', 'coverage', 'inherit', 'rare', 'violate', 'cow', 'initial', 'rarely', 'violation', 'crack', 'initially', 'rat', 'violence', 'craft', 'initiate', 'rate', 'violent', 'crash', 'initiative', 'rather', 'virtual', 'crawl', 'injure', 'rating', 'virtually', 'crazy', 'injury', 'ratio', 'virtue', 'cream', 'inmate', 'rational', 'virus', 'create', 'inner', 'raw', 'visible', 'creation', 'innocent', 're', 'vision', 'creative', 'innovation', 'reach', 'visit', 'creativity', 'innovative', 'react', 'visitor', 'creature', 'input', 'reaction', 'visual', 'credibility', 'inquiry', 'read', 'vital', 'credit', 'insect', 'reader', 'vitamin', 'crew', 'insert', 'readily', 'vocal', 'crime', 'inside', 'reading', 'voice', 'criminal', 'insight', 'ready', 'volume', 'crisis', 'insist', 'real', 'voluntary', 'criteria', 'inspection', 'realistic', 'volunteer', 'critic', 'inspector', 'reality', 'vote', 'critical', 'inspiration', 'realize', 'voter', 'criticism', 'inspire', 'really', 'voting', 'criticize', 'install', 'realm', 'vs', 'crop', 'installation', 'rear', 'vulnerable', 'cross', 'instance', 'reason', 'wage', 'crowd', 'instant', 'reasonable', 'wagon', 'crowded', 'instantly', 'rebel', 'waist', 'crucial', 'instead', 'rebuild', 'wait', 'cruel', 'instinct', 'recall', 'wake', 'cruise', 'institution', 'receive', 'walk', 'crush', 'institutional', 'receiver', 'walking', 'cry', 'instruct', 'recent', 'wall', 'crystal', 'instruction', 'recently', 'wander', 'Cuban', 'instructional', 'reception', 'want', 'cue', 'instructor', 'recession', 'war', 'cultural', 'instrument', 'recipe', 'warehouse', 'culture', 'insurance', 'recipient', 'warm', 'cup', 'intact', 'recognition', 'warmth', 'cure', 'integrate', 'recognize', 'warn', 'curiosity', 'integrated', 'recommend', 'warning', 'curious', 'integration', 'recommendation', 'warrior', 'currency', 'integrity', 'record', 'wash', 'current', 'intellectual', 'recording', 'waste', 'currently', 'intelligence', 'recover', 'watch', 'curriculum', 'intelligent', 'recovery', 'water', 'curtain', 'intend', 'recruit', 'wave', 'curve', 'intense', 'red', 'way', 'custody', 'intensity', 'reduce', 'we', 'custom', 'intent', 'reduction', 'weak', 'customer', 'intention', 'refer', 'weaken', 'cut', 'interact', 'reference', 'weakness', 'cute', 'interaction', 'reflect', 'wealth', 'cycle', 'interest', 'reflection', 'wealthy', 'dad', 'interested', 'reform', 'weapon', 'daily', 'interesting', 'refrigerator', 'wear', 'dam', 'interfere', 'refuge', 'weather', 'damage', 'interior', 'refugee', 'weave', 'damn', 'internal', 'refuse', 'web', 'dance', 'international', 'regain', 'wedding', 'dancer', 'Internet', 'regard', 'weed', 'dancing', 'interpret', 'regarding', 'week', 'danger', 'interpretation', 'regardless', 'weekend', 'dangerous', 'interrupt', 'regime', 'weekly', 'dare', 'interval', 'region', 'weigh', 'dark', 'intervention', 'regional', 'weight', 'darkness', 'interview', 'register', 'weird', 'data', 'intimate', 'regret', 'welcome', 'database', 'into', 'regular', 'welfare', 'date', 'introduce', 'regularly', 'well', 'daughter', 'introduction', 'regulate', 'well-being', 'dawn', 'invade', 'regulation', 'well-known', 'day', 'invasion', 'regulator', 'west', 'dead', 'invent', 'regulatory', 'western', 'deadline', 'invention', 'rehabilitation', 'wet', 'deadly', 'inventory', 'reinforce', 'whale', 'deal', 'invest', 'reject', 'what', 'dealer', 'investigate', 'relate', 'whatever', 'dear', 'investigation', 'related', 'wheat', 'death', 'investigator', 'relation', 'wheel', 'debate', 'investment', 'relationship', 'wheelchair', 'debris', 'investor', 'relative', 'when', 'debt', 'invisible', 'relatively', 'whenever', 'debut', 'invitation', 'relax', 'where', 'decade', 'invite', 'release', 'whereas', 'decent', 'involve', 'relevant', 'wherever', 'decide', 'involved', 'reliability', 'whether', 'decision', 'involvement', 'reliable', 'which', 'deck', 'Iraqi', 'relief', 'while', 'declare', 'Irish', 'relieve', 'whip', 'decline', 'iron', 'religion', 'whisper', 'decorate', 'ironically', 'religious', 'white', 'decrease', 'irony', 'reluctant', 'who', 'dedicate', 'Islam', 'rely', 'whoever', 'deem', 'Islamic', 'remain', 'whole', 'deep', 'island', 'remaining', 'whom', 'deeply', 'isolate', 'remark', 'whose', 'deer', 'isolated', 'remarkable', 'why', 'defeat', 'isolation', 'remember', 'wide', 'defend', 'Israeli', 'remind', 'widely', 'defendant', 'issue', 'reminder', 'widespread', 'defender', 'it', 'remote', 'widow', 'defense', 'Italian', 'removal', 'wife', 'defensive', 'item', 'remove', 'wild', 'deficit', 'its', 'render', 'wilderness', 'define', 'itself', 'rent', 'wildlife', 'definitely', 'jacket', 'rental', 'will', 'definition', 'jail', 'repair', 'willing', 'degree', 'Japanese', 'repeat', 'willingness', 'delay', 'jar', 'repeatedly', 'win', 'deliberately', 'jaw', 'replace', 'wind', 'delicate', 'jazz', 'replacement', 'window', 'delight', 'jeans', 'reply', 'wine', 'deliver', 'jet', 'report', 'wing', 'delivery', 'Jew', 'reportedly', 'winner', 'demand', 'jewelry', 'reporter', 'winter', 'democracy', 'Jewish', 'reporting', 'wipe', 'Democrat', 'job', 'represent', 'wire', 'democratic', 'join', 'representation', 'wisdom', 'demographic', 'joint', 'representative', 'wise', 'demonstrate', 'joke', 'republic', 'wish', 'demonstration', 'journal', 'Republican', 'with', 'denial', 'journalism', 'reputation', 'withdraw', 'dense', 'journalist', 'request', 'withdrawal', 'density', 'journey', 'require', 'within', 'deny', 'joy', 'required', 'without', 'depart', 'judge', 'requirement', 'witness', 'department', 'judgment', 'rescue', 'wolf', 'departure', 'judicial', 'research', 'woman', 'depend', 'juice', 'researcher', 'wonder', 'dependent', 'jump', 'resemble', 'wonderful', 'depending', 'jungle', 'reservation', 'wood', 'depict', 'junior', 'reserve', 'wooden', 'deploy', 'jurisdiction', 'residence', 'word', 'deposit', 'juror', 'resident', 'work', 'depressed', 'jury', 'residential', 'worker', 'depression', 'just', 'resign', 'working', 'depth', 'justice', 'resist', 'workout', 'deputy', 'justify', 'resistance', 'workplace', 'derive', 'keep', 'resolution', 'works', 'descend', 'key', 'resolve', 'workshop', 'describe', 'kick', 'resort', 'world', 'description', 'kid', 'resource', 'worldwide', 'desert', 'kill', 'respect', 'worried', 'deserve', 'killer', 'respectively', 'worry', 'design', 'killing', 'respond', 'worth', 'designer', 'kind', 'respondent', 'would', 'desire', 'king', 'response', 'wound', 'desk', 'kingdom', 'responsibility', 'wow', 'desperate', 'kiss', 'responsible', 'wrap', 'desperately', 'kit', 'rest', 'wrist', 'despite', 'kitchen', 'restaurant', 'write', 'dessert', 'knee', 'restore', 'writer', 'destination', 'kneel', 'restrict', 'writing', 'destroy', 'knife', 'restriction', 'written', 'destruction', 'knock', 'result', 'wrong', 'detail', 'know', 'resume', 'yard', 'detailed', 'knowledge', 'retail', 'yeah', 'detect', 'known', 'retailer', 'year', 'detective', 'Korean', 'retain', 'yell', 'determination', 'lab', 'retire', 'yellow', 'determine', 'label', 'retired', 'yes', 'devastating', 'labor', 'retirement', 'yesterday', 'develop', 'laboratory', 'retreat', 'yet', 'developer', 'lack', 'return', 'yield', 'developing', 'ladder', 'reveal', 'you', 'development', 'lady', 'revelation', 'young', 'developmental', 'lake', 'revenue', 'youngster', 'device', 'lamp', 'reverse', 'your', 'devil', 'land', 'review', 'yours', 'devote', 'landing', 'revolution', 'yourself', 'diabetes', 'landmark', 'revolutionary', 'youth', 'diagnose', 'landscape', 'reward', 'zone', 'diagnosis', 'lane', 'rhetoric', '', '']
false_names=['london','malaria','kenya','twitter','city','name','park','city','north','south','east','west','town','the','se','nw','ne','sw','korea','ma','beach','',"",'"',"'",',','.',' ',';','?','!']
# false_names.extend(list(nouns))
# false_names.extend(list(verbs))
false_names.extend(common_words)
false_names.extend(stop_words_2)
false_names=set(false_names)

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
			if tags[i-1][0].lower() in loc_preposition_list or tags[i-1][0].lower() in dir_list:
				#return_name_list.append(loc_name)
				if ',' in add_val:
					return_name_list.extend(loc_name.split(','))
				else:
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
								if d>0.8:
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

	return_name_list=[i.strip() for i in return_name_list]	
	# print(return_name_list)	
	return return_name_list				


with open('./india_location_dict.p','rb') as handle:
	india_loc_dict=pickle.load(handle)

# false_names=false_names-set([i for i in india_loc_dict])

input_file_dir='./INPUT_FILES/'
outfile_folder='C2'

file_arr=os.listdir('./'+input_file_dir)
count1=0
count2=0

all_lines=0
exception_count=0
geo_in_india=open('./OUTPUT_FILES/'+outfile_folder+'/GEOin.txt','w')
geo_out_india=open('./OUTPUT_FILES/'+outfile_folder+'/GEOout.txt','w')
for file in file_arr:
	outfile_with_location=open('./OUTPUT_FILES/'+outfile_folder+'/'+file,'w')
	outfile_without_location=open('./OUTPUT_FILES/'+outfile_folder+'/'+'_NOT_'+file,'w')

	f=open(input_file_dir+file)	
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

			if obj['lang']!='en':
				continue

			if id_text in unique_tweet_id_dict:
				continue

			hashtag_list=[]
			try:
				for i in obj['entities']['hashtags']:
					hashtag_list.append(i['text'])
				# print(hashtag_list)	
			except:
				# print("Exception in hashtags")
				# print(hashtag_list)
				hashtag_list=[]		

			poss_places=[]
			for hash_elem in hashtag_list:
				if hash_elem not in false_names and hash_elem in india_loc_dict :
					poss_places.append(hash_elem)
			

			tweet_text=obj['text']
			place_text=[]
			lat_long_str=""
			# print(tweet_text) ### to be rmvd

			if str(obj["place"]) != "None": ### for geo-tagged tweets 
				f3,modified_json=modify_json(obj)
				if f3==True:
					outfile_with_location.write(json.dumps(modified_json)+'\n')
					geo_in_india.write(json.dumps(modified_json)+'\n')
					count1+=1
					if count1%10==0:
						print("Count 1= "+ str(count1))
					unique_tweet_id_dict[id_text]=(tweet_text, True)
				else:
					# obj2=empty_json(obj)
					# if poss_places==[]:
					outfile_without_location.write(json.dumps(modified_json)+'\n')
					geo_out_india.write(json.dumps(modified_json)+'\n')
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
				# print("Loc List Spacy")
				#print(time.time()-starttime2)
				org_list=[]
				prev_word=""
				prev_word_type=""
				for word in doc:
					if word.ent_type_ in entity_type_list:
						org_list.append(word.orth_+"<_>"+word.ent_type_)
					else:
						org_list.append("<_>")

				# print(org_list)		
				for i in org_list:
					index=i.index("<_>")
					if i[index+3:]=='GPE' or i[index+3:]=='FACILITY' or i[index+3:]=='LOC':
						poss_places.append(i[:index])
				poss_places.extend(loc_list_spacy)
				# print("Poss Places explained")

				if len(poss_places)==0:
					obj2=empty_json(obj)
					outfile_without_location.write(json.dumps(obj2)+'\n')
					unique_tweet_id_dict[id_text]=(tweet_text,False)
					continue
					
				poss_places=set([i.lower().strip() for i in poss_places])
				# print(poss_places)
				refined_poss_place_list=[]	
				for i in poss_places:
					if i in india_loc_dict and i not in false_names:
						#print("Inside India "+str(i))
						refined_poss_place_list.append((i,india_loc_dict[i]))


				if len(refined_poss_place_list)==0:
					obj2=empty_json(obj)
					outfile_without_location.write(json.dumps(obj2)+'\n')
					unique_tweet_id_dict[id_text]=(tweet_text,False)
					continue
				else:
					#refined_poss_place_list=[i for i in refined_poss_place_list if i[0] not in false_names]
					# if len(refined_poss_place_list)==0:
					# 	obj2=empty_json(obj)
					# 	outfile_without_location.write(json.dumps(obj2)+'\n')
					# 	unique_tweet_id_dict[id_text]=(tweet_text, False)

					# else:
					# random_elem=refined_poss_place_list[0]
					# print("Refined Poss Places")
					# print(refined_poss_place_list)
					for elem in refined_poss_place_list:
						modified_json=modify_json_2(obj,elem[1][0],elem[1][1],elem[0])
						outfile_with_location.write(json.dumps(modified_json)+'\n')
						count2+=1

					unique_tweet_id_dict[id_text]=(tweet_text,True)
					if count2%100==0:
						print("Count 2= "+ str(count2))


		except Exception as e:
			print("EXCEPTION")
			print(e,id_text)
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			# print(obj,obj2)
			exception_count+=1
			continue		

print(count1,count2)
print(exception_count)

print(len(unique_tweet_id_dict))
for i in overall_location_dict:
	print(i,overall_location_dict[i])