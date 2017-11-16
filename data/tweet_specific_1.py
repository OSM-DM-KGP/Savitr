from __future__ import print_function
import sys,io
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import os,signal
import sys
import time
import gzip

specific=sys.argv[1]
# use Kaustabh's key

#Variables that contains the user credentials to access Twitter API 
# access_token = "900801909417791488-ayuvoHwGozmSLypO4c43Y0BJYjEWjga"
# access_token_secret = "K21taY7vVl2cJWsIdooARfVP1FfSHWIHrKs13w655UTiP"
# consumer_key = "XEtyr3gSbLyApjkBUigqtP28w"
# consumer_secret =  "bwhi37FkOHSUCbGNeiTdh1oETXDFplwRhy5znMrqG5RWNmFGt0"
access_token="898515053757865984-ZXkbfaHt64RKUEE1q4mOZrmNuwaG8vV"
access_token_secret='vMhaorwHGJOHgTq3EIFBOYTAauywfAdegOlr66ejeADuY'
consumer_key='5m2euOBDU4bF37egHFe5wGlcA'
consumer_secret="X0KKFNvtL2ltSLOqR1HhSArZyNylSmaafXb1F5HTXlVfOl2yBa"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
	
    def __init__(self):
        self.count=0
        StreamListener.__init__(self)

    def on_data(self, data):
        self.count=self.count+1
        print ("Tweet: "+str(self.count))
        day=int((time.time()-start_time)/86400)
        #print(day)
        filename = "All_Stream_tweets_"+specific+"_"+str(day)+"_"+".txt"
        f= open(filename,"a+")
        f.write(data)
        f.write("\n")
        f.close()

        
    def on_error(self, status):
        if status==420:
            print ("Error")
            return False

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    global start_time
    start_time=time.time()
    while True:
        try:
            stream = Stream(auth, l)
            stream.filter(track=[str(specific)])
        except KeyboardInterrupt:
            break
        except Exception as e:
            pass

'''
[[[68.4228514144,7.841615498],[97.6904295394,7.841615498],[97.6904295394,35.5679807149],[68.4228514144,35.5679807149]]]
'''
