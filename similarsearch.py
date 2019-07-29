# David Son 7/12/19
# This program takes in a field, and a word to search for
# and outputs all similar words or phrases and displays the top 10
# words found within the related descriptions.

import decimal
import nltk
import string
import re
import json
from pymongo import MongoClient
from difflib import SequenceMatcher
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

# Choose a function based on user input.
def main():

    # Connecting to MongoDB for all of the documents.
    client = MongoClient('mongodb://34.73.180.107:27017')
    db = client.smartcareer
    col = db['jobdescription']
    allDocs = col.find()

    # User input for search function
    field = string.capwords(input("What is the field you are looking for? "))
    newText = string.capwords(input("What is the text you are looking for? \nType 'All+' for all unique words of that topic.\n"))
    print()

    varSearch(allDocs, field, newText)

# Take each document and find words or phrases similar to it.
# If there are equivalent values, increase the counter for that specific word.
def varSearch(docs, field, newText):
    similarCount = {}
    descCount = {}
    groupCount = {}
    temp4 = []
    lineCount = 1

    for i in docs:
        try :
            value = i.get(field)
            if newText in value:
                cleanDesc = i.get('Description')

                if value in similarCount:
                    similarCount[value] = similarCount.get(value) + 1

                else:
                    similarCount[value] = 1
                    if len(similarCount) > 0:
                        match = SequenceMatcher(None, value, list(similarCount.keys())[-2]).find_longest_match(0, len(value), 0, len(list(similarCount.keys())[-2]))

                        # Check the whole list for similar words and add to the group that is the shortest common subsequence of letters.
                        for key in similarCount.keys():
                            tMatch = SequenceMatcher(None, key, list(similarCount.keys())[-2]).find_longest_match(0, len(key), 0, len(list(similarCount.keys())[-2]))
                            if tMatch[2] < match[2]:
                                match = tMatch

                        if match[2] > 5:
                            pureName = punctuationRemover(value[match.a: match.a + match.size])
                            pureName = pureName.strip()

                            if pureName in groupCount:
                                groupCount[pureName] = groupCount[pureName] + 1
                            else:
                                groupCount[pureName] = 2

                        else:
                            continue
                
                temp3, descCount = descriptionParser(cleanDesc, descCount)
                temp4 = temp3 + temp4
                lineCount += 1
            
        # Skip this document since the field does not exist for it.
        except:
            continue

    print("Results:")
    print("Total Found:", lineCount,"\n")
    print("All similar texts:\n")

    # Print out each dictionary item and how many times it was found/percentage of all
    # documents with that word or phrase.
    for key,val in sorted(similarCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True):
        print("Ratio: {:7s} Count: {:<5d} Text: {:40s}".format(str(round((val/lineCount*100),2))+"%",val, key))
    
    print()
    print("The group(s) of similar topics.\n")

    # Print out each topic and how many variations they have each.
    for key,val in sorted(groupCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True):
        print("Group: {:40s} Variations: {:1d}".format(key, val))

    print("\nThese are the top ten words for this topic:\n")
    count = 1

    # Print the top 10 words in the descriptions of a certain job or topic.
    for key,val in sorted(descCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)[0:10]:
        print("{:3s} Word: {:20s} Count: {:4d}".format(str(count)+".","\""+key+"\"",val))
        count += 1

    # Frequency plot.
    freq = nltk.FreqDist(temp4)
    freq.plot(30, cumulative = False)
    exit()
    
# Use some natural language processing to extract unique words
# from the document's description and insert it into a dictionary.
def descriptionParser(cleanDesc, descCount):
    temp = punctuationRemover(cleanDesc)
    temp = re.sub(r'\d+', '', temp)
    splitDesc = tokenize(temp)
    splitDesc = [item.lower() for item in splitDesc]
    temp2 = removeStop(splitDesc)
    temp3 = lemmatizer(temp2)

    # Get a count of important words within each related description.
    for j in temp3:
        if j in descCount:
            descCount[j] = descCount.get(j) + 1
        else :
            descCount[j] = 1
    
    return temp3, descCount

# NLP that removes all punctuation.
def punctuationRemover(description):
    noPunctuation = "".join([char for char in description if char not in string.punctuation])
    return noPunctuation

# NLP that splits words by space.
def tokenize(temp):
    tokens = re.split(r'\W+', temp)
    return tokens

# NLP that removes clutter words such as 'by' and 'and'.
def removeStop(splitDesc):
    stopword = nltk.corpus.stopwords.words('english')
    returnText = [word for word in splitDesc if word not in stopword]
    return returnText

# Gets only the root of each word (slower, but better than stemming).
def lemmatizer(temp2):
    wn = WordNetLemmatizer()
    textReturn = []
    textReturn = [wn.lemmatize(word) for word in temp2]
    return textReturn

main()