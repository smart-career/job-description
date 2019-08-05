# David Son 7/12/19
# This program takes in a field, and a word to search for
# and outputs all similar words or phrases and displays the top 10
# words found within the related descriptions.

import decimal
import nltk
import string
import re
import json
import copy
import pymongo
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
    allDocs = col.find({},no_cursor_timeout=True)

    # User input for search function
    field = string.capwords(input("What is the field you are looking for? "))
    newText = string.capwords(input("What is the text you are looking for? \nType 'All+' for all unique words of that topic.\n"))
    print()

    varSearch(allDocs, field, newText)

# Take each document and find words or phrases similar to it.
# If there are equivalent values, increase the counter for that specific word.
def varSearch(docs, field, newText):
    similarCount = {}
    doClone = copy.deepcopy(docs)
    groupCount = {}
    lineCount = 0

    for i in docs:
        try:
            value = i.get(field)
            if newText in value and newText != "All+" and field != "Location":

                if value in similarCount:
                    similarCount[value] = similarCount.get(value) + 1

                else:
                    similarCount[value] = 1
                    if len(similarCount) > 0:

                        # Check the whole list for similar words and add to the group that is the shortest common subsequence of letters.
                        for key in similarCount.keys():
                            tMatch = SequenceMatcher(None, newText, key).find_longest_match(0, len(newText), 0, len(key))

                        pureName = punctuationRemover(newText[tMatch.a: tMatch.a + tMatch.size])
                        pureName = pureName.strip()

                        if pureName in groupCount:
                            groupCount[pureName] = groupCount[pureName] + 1
                        else:
                            groupCount[pureName] = 1

                    else:
                        continue
                
                lineCount += 1
            
            elif field == "Location":
                if value in similarCount:
                    similarCount[value] = similarCount.get(value) + 1

                else:
                    similarCount[value] = 1
                    if len(similarCount) > 0:

                        pureName = newText

                        if pureName in groupCount:
                            groupCount[pureName] = groupCount[pureName] + 1
                        else:
                            groupCount[pureName] = 1
                
                lineCount += 1
        
            elif newText == "All+":

                if value in similarCount:
                    similarCount[value] = similarCount.get(value) + 1

                else:
                    similarCount[value] = 1
                    if len(similarCount) > 0:

                        # Check the whole list for similar words and add to the group that is the shortest common subsequence of letters.
                        for key in similarCount.keys():
                            tMatch = SequenceMatcher(None, value, key).find_longest_match(0, len(value), 0, len(key))

                        pureName = punctuationRemover(value[tMatch.a: tMatch.a + tMatch.size])
                        pureName = pureName.strip()
                        
                        # For All+, if there's more than one group we have to check through all of them for near-duplicates.
                        if len(groupCount) > 0:

                            # For each key in groupCount, try to get a match.
                            for gKey in groupCount.keys():
                                tMatch = SequenceMatcher(None, pureName, gKey).find_longest_match(0, len(pureName), 0, len(gKey))

                                # If they are exactly equal, add one to the counter of that key.
                                if pureName == gKey:
                                    groupCount[pureName] = groupCount[pureName] + 1

                                # Nearly matching, so it must be like 'Amazon' vs. 'Amazon Web Services'.
                                elif tMatch[2] > 4:

                                    # Take the shorter one and make that the main group. Remove the other longer key and give its value to the new one.
                                    if len(pureName) < len(gKey):
                                        addName = punctuationRemover(pureName[tMatch.a: tMatch.a + tMatch.size])
                                        addName = addName.strip()
                                        groupCount[addName] = groupCount.pop(gKey)
                                    
                                    # Same as above.
                                    else:
                                        addName = punctuationRemover(gKey[tMatch.b: tMatch.b + tMatch.size])
                                        addName = addName.strip()
                                        groupCount[addName] = groupCount[addName] + 1
                               
                        else:
                            groupCount[pureName] = 1

                    else:
                        continue

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
        print()

    docReplacer(doClone, field, groupCount)
    exit()
    
# NLP that removes all punctuation.
def punctuationRemover(description):
    noPunctuation = "".join([char for char in description if char not in string.punctuation])
    return noPunctuation

# NLP that splits words by space.
def tokenize(temp):
    tokens = re.split(r'\W+', temp)
    return tokens

# This method receives all MongoDB documents, the field, and groupCount which holds the standardized name
# and re-uploads a clean standardized dataset to MongoDB.
def docReplacer(doClone, field, groupCount):
    count = 0
    client = MongoClient('34.73.180.107:27017', 27017)
    db = client['smartcareer']
    collection = db['Clean']
    replacement = ' '.join(groupCount.keys())
    match = ' '.join(groupCount.keys())
    updateLine = { "$set": { field: replacement } }

    # Replace all variations with one standardized word or phrase.
    for doc in doClone:

        if field == "Location":
            citySplit = replacement.split(",")
            match = citySplit[0]

        # This document must be standardized.
        try: 
            if match in doc[field]:

                #If the field doesn't exist (older document), then skip it.
                doc[field] = replacement
                toUpdate = doc['_id']
                docUpdate = { '_id': toUpdate}

                # This document is new, but it needed to be standardized.
                try:
                    collection.insert_one(doc)
                    count += 1
                    print("This document was standardized!:", count)

                # This document has already been inserted, but another field needed to be standardized.
                except pymongo.errors.DuplicateKeyError:
                    collection.update_one(docUpdate, updateLine)
                    count += 1
                    print("This document was standardized and updated!:", count)

            # This document does not need to be standardized.
            else:

                #Completely new document being added.
                try:
                    collection.insert_one(doc)
                    count += 1
                    print("This document was newly inserted!:", count)

                # This document is up to date, do not touch.
                except pymongo.errors.DuplicateKeyError:
                    count += 1
                    print("This document is up to date!", count)
                    continue

        except:
            continue

    doClone.close()
    print("Replacement Complete!")


main()