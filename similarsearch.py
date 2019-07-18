# David Son 7/12/19
# This program takes in a MongoDB .json export file, a field, and a word to search for
# and outputs all similar words or phrases and displays the top 10
# words found within the related descriptions.

import decimal
import nltk
import string
import re
from difflib import SequenceMatcher

# Choose a function based on user input.
def main():
    # Take in the 3 user inputs (file, field, word to search for)
    newFile = input("What is the file name? ")
    field = string.capwords(input("What is the field you are looking for? "))
    newText = string.capwords(input("What is the text you are looking for? \nType 'All+' for all unique words of that topic.\n"))
    print()
    fieldText = field + "\"" + ":" + "\"" + newText

    lineCount = 0
    newList = []

    # Open a file and parse all lines and add to list.
    if newText == "All+":
        with open(newFile, encoding="utf8") as thisFile:
            for line in thisFile:
                newList.append(line)
                lineCount += 1
            varSearch(newList, lineCount, field)

    # Open a file and parse through lines, only adding lines that have the key word/phrase included.
    else: 
        with open(newFile, encoding="utf8") as thisFile:
            for line in thisFile:
                if fieldText in line:
                    newList.append(line)
                    lineCount += 1
            varSearch(newList, lineCount, field)

# Take each document and find words or phrases similar to it.
# If there are equivalent values, increase the counter for that specific word.
def varSearch(newList, lineCount, field):
    similarCount = {}
    descCount = {}
    groupCount = {}
    temp4 = []

    for i in newList:
        try :
            subStart = i.index('\"' + field + '\"')
            subEnd = i.find('\",\"', subStart)

            if i[subEnd - 1] == "}":
                compName = i[subStart:subEnd - 2]
            else:
                compName = i[subStart:subEnd]

            cStart = compName.index(':\"')
            cleanName = compName[cStart + 2:]

            if cleanName in similarCount:
                similarCount[cleanName] = similarCount.get(cleanName) + 1
            else:
                similarCount[cleanName] = 1
                if len(similarCount) > 0:
                    match = SequenceMatcher(None, cleanName, list(similarCount.keys())[-2]).find_longest_match(0, len(cleanName), 0, len(list(similarCount.keys())[-2]))

                    # Check the whole list for similar words and add to the group that is the shortest common subsequence of letters.
                    for key in similarCount.keys():
                        tMatch = SequenceMatcher(None, key, list(similarCount.keys())[-2]).find_longest_match(0, len(key), 0, len(list(similarCount.keys())[-2]))
                        if tMatch[2] < match[2]:
                            match = tMatch
                    if match[2] > 5:
                        pureName = punctuationRemover(cleanName[match.a: match.a + match.size])
                        pureName = pureName.strip()

                        if pureName in groupCount:
                            groupCount[pureName] = groupCount[pureName] + 1
                        else:
                            groupCount[pureName] = 2

                    else:
                        continue
            
            temp3 = descriptionParser(i, descCount)
            temp4 = temp3 + temp4
        
        # Skip this document since the field does not exist for it.
        except:
            continue

    print("Results:")
    print("Total Found:", lineCount,"\n")
    print("All similar texts:\n")

    # Print out each dictionary item and how many times it was found/percentage of all
    # documents with that word or phrase.
    for key,val in sorted(similarCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True):
        print("Ratio: {:7s} Count: {:<5d} Text: {:40s}".format(str(round(((val/lineCount)*100),2))+"%",val, key))
    
    print()
    print("The group(s) of similar topics.\n")
    # Print out each topic and how many variations they have each.
    for key,val in sorted(groupCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True):
        print("Group: {:40s} Variations: {:1d}".format(key, val))

    print("\nThese are the top ten words for this topic:\n")

    # Print the top 10 words in the descriptions of a certain job or topic.
    count = 1
    for key,val in sorted(descCount.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)[0:10]:
        print("{:3s} Word: {:20s} Count: {:4d}".format(str(count)+".","\""+key+"\"",val))
        count += 1

    freq = nltk.FreqDist(temp4)
    freq.plot(30, cumulative = False)
    exit()
    
# Use some natural language processing to extract unique words
# from the document's description and insert it into a dictionary.
def descriptionParser(line, descCount):
    descStart = line.index('\"Description\"')
    descEnd = line.find('\",\"', descStart)
    descName = line[descStart:descEnd]
    descFull = descName.index(':\"')
    cleanDesc = descName[descFull + 2:]
    temp = punctuationRemover(cleanDesc)
    splitDesc = tokenize(temp)
    splitDesc = [item.lower() for item in splitDesc]
    temp2 = removeStop(splitDesc)

    # Get a count of important words within each related description.
    for j in temp2:
        if j in descCount:
            descCount[j] = descCount.get(j) + 1
        else :
            descCount[j] = 1
    
    return temp2

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

main()