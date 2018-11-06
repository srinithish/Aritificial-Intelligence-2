#!/usr/bin/env python3
## -- coding: utf-8 --
#"""
#Created on Fri Oct 12 19:16:21 2018
#
#@author: 18123


"""
The following program has been prototype using the Naive Bayes Classifier, based on the 
conditional independence assumption, given as,
P(Location/Tweet) = P(Tweet/location)*P(Location)
where in the right hand side is computed as follows:
    P(Tweet/location) = P(w1/L)*P(w2/L).....*P(wn-1/L)*P(wn/L)
where w1,w2,w3...,wn-1,wn are the words in the given Tweet.
L being the location
The Naive Bayes Assumption tells us that words in a given tweet are conditionally independent
given Location.
If the given word of the tweet is not present in that particular location of our train set,
P(W/L) = ΣP(W/L) summation over all the locations.
If the word still not found we have assigned a small probability value to it.
Our Data structure for the bag of words is a dictionary of dictionary in the below format:
    {location:{word1 : count,word2 :count}}, where the word1, word2 and so on are the unique words appearing in the tweets.

 

"""

import sys
import re
import pandas as pd
import operator
from collections import Counter 
from collections import defaultdict
import csv

#Taking the input train and test files as commandline arguments
train_file = sys.argv[1]
test_file = sys.argv[2]
output_file = sys.argv[3]


# location and unique word count
locWordDict = {} # {location:{word1 : count,word2 :count}}
LocTweet = {}
#Frequency of locations
locCountDict = defaultdict(int)
exceptionCount = 0
for line in open(train_file, 'r'):
    try:
        LocTweet['City'] = line.split(sep = " ")[0]
        LocTweet['tweet'] = " ".join(line.split(sep = " ")[1:])

    except:
        print(line)
        exceptionCount += 1
    else:
        locCountDict[LocTweet['City']]+=1
        
    if LocTweet['City'] not in locWordDict :
        locWordDict[LocTweet['City']] = re.sub('[^\w\s]|[_]','',LocTweet['tweet']).lower()
        
    else:
        locWordDict[LocTweet['City']] = locWordDict[LocTweet['City']]+ re.sub('[^\w\s]|[_]','',LocTweet['tweet']).lower() #list of teknised words


for location in locWordDict:
    locWordDict[location] = locWordDict[location].split()
    locWordDict[location] = dict(Counter(locWordDict[location]))

#Total Word counts for each location
locTotalWordCount = {key: sum(locWordDict[key].values()) for key in locWordDict.keys()}




#Data Cleaning of the Tweet.
def cleanUpTweet(LocAndTweetAsRawString):
    LocTweetTest = {}
    try:

        LocTweetTest['City'] = LocAndTweetAsRawString.split(sep = " ")[0]
        LocTweetTest['tweet'] = " ".join(LocAndTweetAsRawString.split(sep = " ")[1:])

    except:
        pass
    else:
        LocTweetTest['tweet'] = re.sub('[^\w\s]|[_]','',LocTweetTest['tweet']).lower().split()
    return LocTweetTest   


    
#probability of word given location  
def prob_word_given_location(word,location):
    return locWordDict[location][word] / locTotalWordCount[location]


#Probability of location
def prob_location(location):
    return locCountDict[location]/sum(locCountDict.values())

#Probability of word 
def prob_word(word):
    p = 0
    leastvalue = 1.0969945444546837e-100
    for location in locWordDict:
        try:
            p += (prob_word_given_location(word))*prob_location(location)
        except:
            p += 0
     
    if p == 0:
        return leastvalue
    else: 
        return p
        
#Probability of location given tweet
def prob_all_location_given_tweet(tweetAsListOfWords):
    allLocProb = {}
    for location in locCountDict:
        p = 1
        
        for word in tweetAsListOfWords:
            try:
                p = p*prob_word_given_location(word,location)
                
            except:
                p = p*prob_word(word)
        p = p*prob_location(location)
        allLocProb[location] = p
    return max(allLocProb.items(), key=operator.itemgetter(1))[0]


#Probability of all locations given a word
def prob_all_location_given_oneword(word):
    allLocProb = {}
    for location in locCountDict:
        
        

        try:
            p = prob_word_given_location(word,location)
            
        except:
            p = 0
            
            
        p = p*prob_location(location)
        allLocProb[location] = p
        
    return max(allLocProb.items(), key= operator.itemgetter(1)) 



#
wordLocDf = pd.DataFrame(locWordDict)
wordLocDf["Predicted_Cities"] = wordLocDf.index.map(lambda x : prob_all_location_given_oneword(x)[0])
wordLocDf["Probabilities"] = wordLocDf.index.map(lambda x : prob_all_location_given_oneword(x)[1])


# n most common words in a given location
def most_common_words(n):
    wordLocDfMaxWords = wordLocDf.sort_values(['Predicted_Cities','Probabilities'],ascending = False).groupby('Predicted_Cities').head(n)
    group_by_cities = wordLocDfMaxWords.groupby('Predicted_Cities')
    cities_most_frequent_words_df = group_by_cities.apply(lambda x: x.index.unique().tolist())
    print("The following are the ",n, "most frequent words for a given city","\n")
    for index,values in cities_most_frequent_words_df.iteritems():
        print(index,":\n",values,"\n")

#Output Formatting and accuracy function.
def write_outputto_textfile_and_accuracy(file_name):
    df = pd.read_csv(file_name,sep = "\n",header = None)
    df.rename(columns={0:"tweets"},inplace = True)
    df["cities"] = df["tweets"].apply(lambda x :x.split(sep = " " )[0])
    df["Predicted_Cities"] = df["tweets"].apply(lambda x : prob_all_location_given_tweet(cleanUpTweet(x)['tweet']))
    df["tweets"] = df["tweets"].apply(lambda x : " ".join(x.split(sep = " ")[1:]))
    df = df[["Predicted_Cities","cities","tweets"]]
    df.to_csv(output_file, index=False, header = False, sep='\t',quoting = csv.QUOTE_NONE)
    count_of_lines = sum(1 for line in open(file_name))
    print("Accuracy is","\n", 100*sum(df["Predicted_Cities"] == df["cities"])/count_of_lines)
    

#Calling the necessary functions:  
write_outputto_textfile_and_accuracy(test_file)
most_common_words(5)
