import json
import sys

def enlist():
    f = open(sys.argv[1],'r')
    # f = open('xaa','r')
    l = f.readlines()
    f.close()

    outstr = list()
    i = 0
    for each in l:
        if each == '' or each[-2]!='}':
            break
        print(i)
        j = json.loads(each)
        outstr.append('{"index":{"_index":"twitter","_type":"tweet","_id":' + j['_id'] + '}}')

        if 'plt' not in j:
            j['plt'] = j['tlt']
        if 'pln' not in j:
            j['pln'] = ['tln']

        locationstr = ', "t_location": { "lat": ' + str(j['plt']) + ', "lon": '+ str(j['pln']) + '}}'
        outstr.append(each[:3] + 'tweet' + each[3:-2] + locationstr)
        i += 1

    f = open('output.json', 'w')
    # simplejson.dump(outstr, f)
    for each in outstr:
        print>>f, each
    f.close()

 
if __name__ == '__main__':
    enlist()