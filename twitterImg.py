#Use a users tweets + photo to create personalized poetry
#Created for RWET Spring 2015 Final
#ITP - NYU
#By Andrew J. LeVine - www.ajlevine.com

"""
Usage: twitter-img.py <imgfile> [--twitName=<twitName>] [--maxLen=<maxLen>] [--fontSize=<fontSize>] [--ranSamp=<ranSamp>]
"""
#--maxLen= max length of output 
#--fontSize = size of font used in output  
#--ranSamp = amount of different words randomly sampled from 100 most popular words
#--twitName = target users twitter account handle

import sys
import re
from twython import Twython
from docopt import docopt
from PIL import Image
import PIL.ImageOps 
from PIL import ImageEnhance
import random
import operator, time, string
import nltk
from nltk.corpus import stopwords
from string import digits
CONSUMER_KEY = 'dIPhkUCDxW8BNtcmjXgg2HShl'
CONSUMER_SECRET = 'gckJh3v1lnrPGBx5ukuu1isvO1fz0h08COthGHAG72W0ixUHb5'
ACCESS_KEY = '13023742-tPUc0YGNBNcIscEs0ldN8UpnH3xe22raLWVxDJcBb'
ACCESS_SECRET = 'K600tHO9ia0uPTSAklPyjhM8zbUQ6Nf2zv4DSspaWCzQ1'

#DOCOPT COMMAND LINE UX
dct = docopt(__doc__)
imgname = dct['<imgfile>']
maxLen = dct['--maxLen']
fontSize = dct['--fontSize']
ranSamp = dct['--ranSamp']
twitName = dct['--twitName']

try:
    maxLen = float(maxLen)
except:
    maxLen = 14.0 

try:
    fontSize = int(fontSize)
except:
    fontSize = 10

try:
    img = Image.open(imgname)
except IOError:
    exit("File not found: " + imgname)

try:
    ranSamp = int(ranSamp)
except:
    ranSamp = 50

try:
	twitName = twitName
except:
	twitName = "aj701"
#--------

#IMAGING STUFF
width, height = img.size
rate = maxLen / max(width, height)
width = int(rate * width) 
height = int(rate * height)
img = img.resize((width, height))
imgInvert = PIL.ImageOps.invert(img)

pixel = img.load() #get pixels from loaded image - change to imgInvert if image color is too dark/bright
#------------

#TWITTER STUFF
twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
user_timeline = twitter.get_user_timeline(screen_name=twitName, count=200, include_retweets=False)

#Get frequent twitter words
freq = {}
for tweet in user_timeline:
    text = tweet['text']
    words = text.split(' ')
    for word in words:
    	word = word.lower()
    	word = re.sub(r'^https?:\/\/.*[\r\n]*', '', word, flags=re.MULTILINE) #removing url links from tweets
    	wordadj = re.sub('[%s]' % re.escape(string.punctuation), '', word) #removing punctuation from tweets
    	new_words = wordadj.translate(string.digits)
        if new_words in freq:
            freq[new_words] += 1
        else:
            freq[new_words] = 1

sorted_words = sorted(freq, key = freq.get, reverse = True) #sorting frequent words
stop = stopwords.words('english')
stop.append("w") #remove random url w left behind
stop.append("rt") #remove retweets
stop.append("u'\u2026'")
stop.append("u'\u2014'")
stop.append("u'\u2192'") #trying to disregard unicode? not sure if this is working - need help
fwords = [w for w in sorted_words if not w in stop]
finCorpus = fwords[:100]
insert = random.sample(finCorpus, ranSamp)

#Append 10 whitespaces to increase contrast 
insert.append(" ") 
insert.append(" ")
insert.append(" ")
insert.append(" ")
insert.append(" ")
insert.append(" ")
insert.append(" ")
insert.append(" ")
insert.append(" ")
insert.append(" ")

string = ""

for h in xrange(height):
    for w in xrange(width):
        rgb = pixel[w, h]
    	string += insert[int(sum(rgb) / 3.0 / 256.0 * (ranSamp+10))] + " " #adding a space between words
    string += "\n"

#lets template this in some html
template = """<!DOCTYPE HTML>
<html>
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <style type="text/css" media="all">
    pre {
      white-space: pre-wrap;
      font-family: 'Inconsolata', 'Consolas'!important;
      line-height: 1.0;
      font-size: %dpx;
    }
  </style>
</head>
<body>
  <pre>%s</pre>
</body>
<!--By Andrew J. LeVine for ITP 2016 - www.ajlevine.com-->
</html>
"""

html = template % (fontSize, string)
sys.stdout.write(html)




	