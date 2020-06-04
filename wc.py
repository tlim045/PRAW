import requests
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import sys, getopt
import json


#base_url = 'https://api.pushshift.io/reddit/search/comment/?q=soundblaster&subreddit=headphones&fields=body&limit=20000'
headphones_url = 'https://api.pushshift.io/reddit/search/comment/?q=soundblaster&subreddit=headphones&after=1d'
soundblaster_url = 'https://api.pushshift.io/reddit/search/comment/?subreddit=soundblasterofficial&after=1d'
headphoneadvice_url = 'https://api.pushshift.io/reddit/search/comment/?q=soundblaster&subreddit=headphoneadvice&after=1d'

#print(base_url)

def processCommand(argv):
    arguments = dict()
    try:
        opts, args = getopt.getopt(argv,"h:o:",["ofile="])
    except getopt.GetoptError:
        print ('wc.py -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('wc.py -o <outputfile>')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            arguments['outputfile'] = arg
    print ('Output file is:', arguments['outputfile'])
    return arguments

def wordCloud(argv):

    res = dict()
    res['headphones'] = requests.get(headphones_url)
    res['soundblasterofficial'] = requests.get(soundblaster_url)
    data_arr = res['headphones'].json()['data'] + res['soundblasterofficial'].json()['data']

    comment_string = " ".join(comment['body'] for comment in data_arr)

    stop = set(STOPWORDS)
    stop.add("soundblaster")
    #stop.add("headphone")
    stop.add("creative")
    stop.add("the")
    stop.add("https")
    stop.add("www")

    wc = WordCloud(height=500,width=1000,background_color='white',stopwords=stop).generate(comment_string)

    print(len(data_arr))

    image = wc.to_file('img2.png')

    with open(argv['outputfile'], 'w+') as fout:
        for entry in data_arr:
            json.dump(entry,fout)
            fout.write("\n")
    fout.close()

if __name__ == "__main__":
    arguments = processCommand(sys.argv[1:])
    print(arguments)
    wordCloud(arguments)